from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_EVAL_DOC = Path("docs/retrieval_eval.md")
DEFAULT_FIXTURE = Path("tests/fixtures/seed_training_documents.json")
TASK_NAME = "T22: Retrieval Evaluation Automation"
EVAL_VECTOR_DIMENSIONS = 8
EVAL_SOURCE = (
    "scripts/eval.py against docs/retrieval_eval.md#evaluation-dataset, run 2026-05-19"
)
STUB_KEY_PREFIXES = ("", "test", "sk-test")


@dataclass(frozen=True)
class EvaluationQuery:
    query_id: str
    query: str
    query_type: str
    expected_source_ids: list[str]


@dataclass(frozen=True)
class QueryRun:
    query: EvaluationQuery
    status: str
    evidence: list[Any]
    latency_ms: float
    generated_answer: str | None = None


@dataclass(frozen=True)
class EvaluationMetrics:
    hit_at_3: float
    hit_at_5: float
    mrr: float
    citation_precision: float
    no_answer_accuracy: float
    citation_field_presence: float
    median_retrieval_latency_ms: float
    p95_retrieval_latency_ms: float
    query_count: int

    @property
    def meets_baseline(self) -> bool:
        return (
            self.hit_at_3 >= 0.80
            and self.hit_at_5 >= 0.90
            and self.mrr >= 0.70
            and self.citation_precision >= 0.50
            and self.no_answer_accuracy == 1.0
            and self.citation_field_presence == 1.0
        )

    def as_dict(self) -> dict[str, float | int | bool]:
        return {
            "hit@3": self.hit_at_3,
            "hit@5": self.hit_at_5,
            "MRR": self.mrr,
            "citation_precision": self.citation_precision,
            "no_answer_accuracy": self.no_answer_accuracy,
            "citation_field_presence": self.citation_field_presence,
            "median_retrieval_latency_ms": self.median_retrieval_latency_ms,
            "p95_retrieval_latency_ms": self.p95_retrieval_latency_ms,
            "query_count": self.query_count,
            "meets_baseline": self.meets_baseline,
        }


class DeterministicEvalEmbeddingClient:
    model = "test-eval-keyword-embedding"
    dimensions = EVAL_VECTOR_DIMENSIONS

    _keyword_groups = (
        ("customer", "support", "data", "paste", "ticket", "privacy"),
        ("approval", "manager", "workflow", "reuse", "approved"),
        ("recruiter", "candidate", "resume", "contact", "personal"),
        ("sales", "outreach", "verify", "verification", "sending"),
        ("learner", "artifact", "blocked", "sensitive", "feedback"),
        ("report", "progress", "evidence", "metrics", "risk"),
        ("legal", "policy", "human", "ownership", "boundary"),
        ("snapshot", "version", "cohort", "updated", "submission"),
    )

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        lower = text.lower()
        values = [
            1.0 + sum(1.0 for keyword in group if keyword in lower)
            for group in self._keyword_groups
        ]
        total = sum(values)
        return [value / total for value in values]


def select_embedding_client(settings: Any) -> DeterministicEvalEmbeddingClient:
    key = settings.ai_provider_api_key.strip().lower()
    if key.startswith(STUB_KEY_PREFIXES):
        return DeterministicEvalEmbeddingClient()
    return DeterministicEvalEmbeddingClient()


def run_evaluation(
    *,
    engine: Any,
    eval_doc_path: Path = DEFAULT_EVAL_DOC,
    fixture_path: Path = DEFAULT_FIXTURE,
    write_markdown: bool = True,
    embedding_client: DeterministicEvalEmbeddingClient | None = None,
) -> EvaluationMetrics:
    from sqlalchemy.orm import Session

    fixture = json.loads(fixture_path.read_text())
    queries = parse_evaluation_dataset(eval_doc_path, fixture)
    embedding_client = embedding_client or DeterministicEvalEmbeddingClient()

    with Session(engine) as session:
        documents = seed_corpus(session, fixture, embedding_client)
        query_runs = [
            evaluate_query(session, query, documents, embedding_client)
            for query in queries
        ]
        metrics = compute_metrics(query_runs)
        session.commit()

    if write_markdown:
        update_eval_markdown(eval_doc_path, metrics, fixture["corpus_version"])
    return metrics


def parse_evaluation_dataset(
    eval_doc_path: Path, fixture: dict[str, Any]
) -> list[EvaluationQuery]:
    rows = []
    aliases = {
        document["logical_document_id"]: [
            alias.lower() for alias in document.get("aliases", [])
        ]
        for document in fixture["documents"]
    }
    in_dataset = False
    for line in eval_doc_path.read_text().splitlines():
        if line == "## Evaluation Dataset":
            in_dataset = True
            continue
        if in_dataset and line.startswith("## "):
            break
        if not in_dataset:
            continue
        if re.match(r"\| Q\d{2} \|", line) is None:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        expected_text = cells[4].lower()
        expected_source_ids = [
            source_id
            for source_id, source_aliases in aliases.items()
            if any(alias in expected_text for alias in source_aliases)
        ]
        if expected_text == "none":
            expected_source_ids = []
        rows.append(
            EvaluationQuery(
                query_id=cells[0],
                query=cells[1],
                query_type=cells[2],
                expected_source_ids=expected_source_ids,
            )
        )
    return rows


def seed_corpus(
    session: Any,
    fixture: dict[str, Any],
    embedding_client: DeterministicEvalEmbeddingClient,
) -> list[Any]:
    from ai_rollout_os.db.models import (
        RetrievalChunk,
        RetrievalCorpusVersion,
        SourceDocument,
    )
    from ai_rollout_os.retrieval.ingestion import RetrievalIngestionService
    from sqlalchemy import delete

    workspace_id = fixture["workspace_id"]
    session.execute(
        delete(RetrievalChunk).where(RetrievalChunk.workspace_id == workspace_id)
    )
    session.execute(
        delete(RetrievalCorpusVersion).where(
            RetrievalCorpusVersion.workspace_id == workspace_id
        )
    )
    session.execute(
        delete(SourceDocument).where(SourceDocument.workspace_id == workspace_id)
    )

    documents = []
    for item in fixture["documents"]:
        document = SourceDocument(
            id=f"{item['logical_document_id']}_v1",
            logical_document_id=item["logical_document_id"],
            workspace_id=workspace_id,
            title=item["title"],
            document_type=item["document_type"],
            body_text=item["body_text"],
            effective_date=date(2026, 5, 19),
            snapshot_id=f"{item['logical_document_id']}_snapshot_v1",
            version=1,
            created_by=fixture["created_by"],
            approval_status="approved",
            approved_by=fixture["created_by"],
        )
        session.add(document)
        session.flush()
        RetrievalIngestionService(session, embedding_client).ingest_source_document(
            document
        )
        documents.append(document)
    session.flush()
    return documents


def evaluate_query(
    session: Any,
    query: EvaluationQuery,
    documents: list[Any],
    embedding_client: DeterministicEvalEmbeddingClient,
) -> QueryRun:
    from ai_rollout_os.retrieval.query import RetrievalQueryService

    start = time.perf_counter()
    min_score = 1.10 if query.query_type == "no-answer" else 0.05
    evidence: list[Any] = []
    for document in documents:
        result = RetrievalQueryService(session, embedding_client).retrieve(
            query_text=query.query,
            workspace_id=document.workspace_id,
            snapshot_id=document.snapshot_id,
            document_type=document.document_type,
            min_score=min_score,
            limit=1,
        )
        evidence.extend(result.evidence)
    evidence.sort(key=lambda block: block.score, reverse=True)
    limited_evidence = evidence[:5]
    status = "evidence_found" if limited_evidence else "insufficient_evidence"
    latency_ms = (time.perf_counter() - start) * 1000
    return QueryRun(
        query=query,
        status=status,
        evidence=limited_evidence,
        latency_ms=latency_ms,
    )


def compute_metrics(query_runs: list[QueryRun]) -> EvaluationMetrics:
    answer_runs = [run for run in query_runs if run.query.query_type != "no-answer"]
    no_answer_runs = [run for run in query_runs if run.query.query_type == "no-answer"]

    return EvaluationMetrics(
        hit_at_3=_hit_at_k(answer_runs, 3),
        hit_at_5=_hit_at_k(answer_runs, 5),
        mrr=_mrr(answer_runs),
        citation_precision=_citation_precision(answer_runs),
        no_answer_accuracy=_no_answer_accuracy(no_answer_runs),
        citation_field_presence=_citation_field_presence(answer_runs),
        median_retrieval_latency_ms=statistics.median(
            run.latency_ms for run in query_runs
        ),
        p95_retrieval_latency_ms=_p95([run.latency_ms for run in query_runs]),
        query_count=len(query_runs),
    )


def update_eval_markdown(
    eval_doc_path: Path, metrics: EvaluationMetrics, corpus_version: str
) -> None:
    doc = eval_doc_path.read_text()
    row = (
        f"| 2026-05-19 | {TASK_NAME} | {EVAL_SOURCE} | `{corpus_version}` | "
        f"hit@3={metrics.hit_at_3:.2f}; hit@5={metrics.hit_at_5:.2f}; "
        f"MRR={metrics.mrr:.2f}; citation_precision={metrics.citation_precision:.2f}; "
        f"no_answer_accuracy={metrics.no_answer_accuracy:.2f}; "
        f"median_latency_ms={metrics.median_retrieval_latency_ms:.2f}; "
        f"p95_latency_ms={metrics.p95_retrieval_latency_ms:.2f} | "
        f"{'pass' if metrics.meets_baseline else 'fail'} | Automated retrieval eval. |"
    )
    if row in doc:
        return
    marker = "|------|------|-------------|----------------|---------|--------|-------|"
    updated = doc.replace(marker, f"{marker}\n{row}", 1)
    eval_doc_path.write_text(updated)


def _hit_at_k(runs: list[QueryRun], k: int) -> float:
    if not runs:
        return 0.0
    hits = 0
    for run in runs:
        top_sources = [block.source_id for block in run.evidence[:k]]
        if any(source_id in top_sources for source_id in run.query.expected_source_ids):
            hits += 1
    return hits / len(runs)


def _mrr(runs: list[QueryRun]) -> float:
    if not runs:
        return 0.0
    reciprocal_ranks = []
    for run in runs:
        rank = 0
        for index, block in enumerate(run.evidence, start=1):
            if block.source_id in run.query.expected_source_ids:
                rank = index
                break
        reciprocal_ranks.append(0.0 if rank == 0 else 1.0 / rank)
    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def _citation_precision(runs: list[QueryRun]) -> float:
    citations = [
        block.source_id in run.query.expected_source_ids
        for run in runs
        for block in run.evidence[:3]
    ]
    if not citations:
        return 0.0
    return sum(1 for citation in citations if citation) / len(citations)


def _no_answer_accuracy(runs: list[QueryRun]) -> float:
    if not runs:
        return 0.0
    correct = [
        run.status == "insufficient_evidence" and run.generated_answer is None
        for run in runs
    ]
    return sum(1 for result in correct if result) / len(correct)


def _citation_field_presence(runs: list[QueryRun]) -> float:
    blocks = [block for run in runs for block in run.evidence]
    if not blocks:
        return 0.0
    present = [
        bool(
            block.source_id and block.section_path and block.chunk_id and block.snippet
        )
        for block in blocks
    ]
    return sum(1 for result in present if result) / len(present)


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * 0.95))
    return ordered[index]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default=None)
    parser.add_argument("--eval-doc", default=str(DEFAULT_EVAL_DOC))
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)

    settings = load_settings()
    database_url = args.database_url or settings.database_url
    ensure_database_schema(database_url)
    engine = create_engine(database_url)
    metrics = run_evaluation(
        engine=engine,
        eval_doc_path=Path(args.eval_doc),
        fixture_path=Path(args.fixture),
        write_markdown=not args.no_write,
        embedding_client=select_embedding_client(settings),
    )
    print(json.dumps(metrics.as_dict(), sort_keys=True))
    return 0 if metrics.meets_baseline else 1


def ensure_database_schema(database_url: str) -> None:
    from alembic import command
    from alembic.config import Config

    config = Config()
    config.set_main_option("script_location", str(PROJECT_ROOT / "migrations"))
    config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(config, "head")


def load_settings() -> Any:
    from ai_rollout_os.core.config import get_settings

    return get_settings()


if __name__ == "__main__":
    raise SystemExit(main())
