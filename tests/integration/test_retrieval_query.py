from datetime import date

from ai_rollout_os.db.models import (
    RetrievalChunk,
    RetrievalCorpusVersion,
    SourceDocument,
)
from ai_rollout_os.retrieval.query import RetrievalQueryService
from sqlalchemy.orm import Session


class MapEmbeddingClient:
    model = "test-embedding-model"
    dimensions = 8

    def __init__(self, vectors: dict[str, list[float]]) -> None:
        self._vectors = vectors

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._vectors[text] for text in texts]


def test_query_filters_by_workspace_snapshot_and_score(migrated_engine) -> None:
    query_text = "customer data allowed"
    with Session(migrated_engine) as session:
        seed_chunk(
            session,
            chunk_id="chunk-target",
            workspace_id="ws-1",
            snapshot_id="snapshot-active",
            document_type="company_policy",
            chunk_text="Support reps may not paste customer data into AI tools.",
            embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        )
        seed_chunk(
            session,
            chunk_id="chunk-other-workspace",
            workspace_id="ws-2",
            snapshot_id="snapshot-other-workspace",
            document_type="company_policy",
            chunk_text="Wrong workspace customer data text.",
            embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        )
        seed_chunk(
            session,
            chunk_id="chunk-other-snapshot",
            workspace_id="ws-1",
            snapshot_id="snapshot-old",
            document_type="company_policy",
            chunk_text="Old snapshot customer data text.",
            embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        )
        seed_chunk(
            session,
            chunk_id="chunk-other-type",
            workspace_id="ws-1",
            snapshot_id="snapshot-other-type",
            document_type="support_sop",
            chunk_text="Support SOP customer data text.",
            embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        )
        session.commit()

        result = RetrievalQueryService(
            session=session,
            embedding_client=MapEmbeddingClient(
                {query_text: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
            ),
        ).retrieve(
            query_text=query_text,
            workspace_id="ws-1",
            snapshot_id="snapshot-active",
            document_type="company_policy",
            min_score=0.5,
        )

    assert result.status == "evidence_found"
    assert [block.chunk_id for block in result.evidence] == ["chunk-target"]
    assert result.evidence[0].score >= 0.5


def test_query_returns_insufficient_evidence_below_threshold(migrated_engine) -> None:
    query_text = "regulated medical certification"
    with Session(migrated_engine) as session:
        seed_chunk(
            session,
            chunk_id="chunk-low-score",
            workspace_id="ws-1",
            snapshot_id="snapshot-active",
            document_type="company_policy",
            chunk_text="General AI usage policy.",
            embedding=[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        )
        session.commit()

        result = RetrievalQueryService(
            session=session,
            embedding_client=MapEmbeddingClient(
                {query_text: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
            ),
        ).retrieve(
            query_text=query_text,
            workspace_id="ws-1",
            snapshot_id="snapshot-active",
            document_type="company_policy",
            min_score=1.1,
        )

    assert result.status == "insufficient_evidence"
    assert result.evidence == []
    assert result.generated_answer is None


def test_evidence_blocks_include_required_citation_fields(migrated_engine) -> None:
    query_text = "manager approval"
    with Session(migrated_engine) as session:
        seed_chunk(
            session,
            chunk_id="chunk-approval",
            workspace_id="ws-1",
            snapshot_id="snapshot-active",
            document_type="company_policy",
            source_id="policy-approval",
            section_path="Policy > Approval",
            chunk_text="Manager approval is required before workflow reuse.",
            embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        )
        session.commit()

        result = RetrievalQueryService(
            session=session,
            embedding_client=MapEmbeddingClient(
                {query_text: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
            ),
        ).retrieve(
            query_text=query_text,
            workspace_id="ws-1",
            snapshot_id="snapshot-active",
            document_type="company_policy",
            min_score=0.01,
        )

    block = result.evidence[0]
    assert block.source_id == "policy-approval"
    assert block.section_path == "Policy > Approval"
    assert block.chunk_id == "chunk-approval"
    assert block.score > 0
    assert block.snippet == "Manager approval is required before workflow reuse."


def seed_chunk(
    session: Session,
    *,
    chunk_id: str,
    workspace_id: str,
    snapshot_id: str,
    document_type: str,
    chunk_text: str,
    embedding: list[float],
    source_id: str = "policy-doc",
    section_path: str = "Policy > Customer Data",
) -> None:
    document = SourceDocument(
        id=f"docver-{chunk_id}",
        logical_document_id=source_id,
        workspace_id=workspace_id,
        title="AI Use Policy",
        document_type=document_type,
        body_text=chunk_text,
        effective_date=date(2026, 5, 19),
        snapshot_id=snapshot_id,
        version=1,
        created_by="operator-1",
        approval_status="approved",
        approved_by="operator-1",
    )
    corpus = RetrievalCorpusVersion(
        id=f"corpus-{chunk_id}",
        workspace_id=workspace_id,
        source_id=source_id,
        source_document_id=document.id,
        snapshot_id=snapshot_id,
        version=1,
        index_schema_version="v1",
        embedding_model="test-embedding-model",
        embedding_dimensions=8,
        chunk_count=1,
    )
    chunk = RetrievalChunk(
        id=chunk_id,
        corpus_version_id=corpus.id,
        workspace_id=workspace_id,
        source_id=source_id,
        source_document_id=document.id,
        snapshot_id=snapshot_id,
        section_path=section_path,
        chunk_index=0,
        chunk_text=chunk_text,
        content_hash=f"hash-{chunk_id}",
        token_count=8,
        index_schema_version="v1",
        embedding_model="test-embedding-model",
        embedding=embedding,
    )
    session.add_all([document, corpus, chunk])
