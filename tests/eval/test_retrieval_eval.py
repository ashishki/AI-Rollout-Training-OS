from ai_rollout_os.retrieval.evidence import EvidenceBlock
from scripts.eval import (
    DEFAULT_EVAL_DOC,
    DEFAULT_FIXTURE,
    EvaluationQuery,
    QueryRun,
    compute_metrics,
    run_evaluation,
)
from sqlalchemy.engine import Engine


def test_retrieval_quality_metrics_meet_baseline(migrated_engine: Engine) -> None:
    metrics = run_evaluation(
        engine=migrated_engine,
        eval_doc_path=DEFAULT_EVAL_DOC,
        fixture_path=DEFAULT_FIXTURE,
        write_markdown=False,
    )

    assert metrics.meets_baseline
    assert metrics.hit_at_3 >= 0.80
    assert metrics.hit_at_5 >= 0.90
    assert metrics.mrr >= 0.70
    assert metrics.citation_precision >= 0.50
    assert metrics.no_answer_accuracy == 1.0
    assert metrics.median_retrieval_latency_ms > 0
    assert metrics.p95_retrieval_latency_ms >= metrics.median_retrieval_latency_ms


def test_no_answer_queries_require_insufficient_evidence() -> None:
    metrics = compute_metrics(
        [
            QueryRun(
                query=EvaluationQuery(
                    query_id="Q09",
                    query="What are the allowed uses of regulated certification?",
                    query_type="no-answer",
                    expected_source_ids=[],
                ),
                status="evidence_found",
                evidence=[
                    EvidenceBlock(
                        source_id="company_ai_policy",
                        section_path="Policy",
                        chunk_id="chunk-1",
                        score=1.0,
                        snippet="Generated guidance would be unsafe here.",
                    )
                ],
                latency_ms=1.0,
                generated_answer="Use AI for regulated certification.",
            )
        ]
    )

    assert metrics.no_answer_accuracy == 0.0
    assert not metrics.meets_baseline
