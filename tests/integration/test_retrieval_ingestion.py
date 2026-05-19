from datetime import date

from ai_rollout_os.db.models import (
    RetrievalChunk,
    RetrievalCorpusVersion,
    SourceDocument,
)
from ai_rollout_os.retrieval.ingestion import RetrievalIngestionService
from ai_rollout_os.retrieval.vector_repository import INDEX_SCHEMA_VERSION
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class StubEmbeddingClient:
    model = "test-embedding-model"
    dimensions = 8

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        seed = sum(ord(character) for character in text)
        return [float((seed + index) % 17) / 17.0 for index in range(self.dimensions)]


def test_ingestion_creates_versioned_chunks(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        document = source_document(
            body_text="# Policy\n\n## Customer Data\n\nDo not paste customer data."
        )
        session.add(document)
        session.commit()

        result = RetrievalIngestionService(
            session=session, embedding_client=StubEmbeddingClient()
        ).ingest_source_document(document)
        logical_document_id = document.logical_document_id
        snapshot_id = document.snapshot_id
        session.commit()

        chunks = session.scalars(
            select(RetrievalChunk).where(
                RetrievalChunk.corpus_version_id == result.corpus_version.id
            )
        ).all()

    assert result.corpus_version.version == 1
    assert result.corpus_version.index_schema_version == INDEX_SCHEMA_VERSION
    assert chunks
    assert chunks[0].source_id == logical_document_id
    assert chunks[0].snapshot_id == snapshot_id
    assert chunks[0].section_path == "Policy > Customer Data"
    assert chunks[0].index_schema_version == "v1"
    assert len(chunks[0].embedding) == StubEmbeddingClient.dimensions


def test_reingest_preserves_prior_snapshot(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        original = source_document(
            id="docver-original",
            snapshot_id="snapshot-original",
            body_text="# Policy\n\n## Privacy\n\nOriginal privacy rule.",
            version=1,
        )
        changed = source_document(
            id="docver-changed",
            snapshot_id="snapshot-changed",
            body_text="# Policy\n\n## Privacy\n\nChanged privacy rule.",
            version=2,
        )
        session.add_all([original, changed])
        session.commit()

        service = RetrievalIngestionService(
            session=session, embedding_client=StubEmbeddingClient()
        )
        first = service.ingest_source_document(original)
        second = service.ingest_source_document(changed)
        session.commit()

        original_chunks = session.scalars(
            select(RetrievalChunk).where(
                RetrievalChunk.snapshot_id == original.snapshot_id
            )
        ).all()
        changed_chunks = session.scalars(
            select(RetrievalChunk).where(
                RetrievalChunk.snapshot_id == changed.snapshot_id
            )
        ).all()
        corpus_versions = session.scalars(
            select(RetrievalCorpusVersion).order_by(RetrievalCorpusVersion.version)
        ).all()

    assert first.corpus_version.id != second.corpus_version.id
    assert [corpus.version for corpus in corpus_versions] == [1, 2]
    assert original_chunks
    assert changed_chunks
    assert original_chunks[0].chunk_text != changed_chunks[0].chunk_text


def source_document(
    *,
    id: str = "docver-1",
    snapshot_id: str = "snapshot-1",
    body_text: str,
    version: int = 1,
) -> SourceDocument:
    return SourceDocument(
        id=id,
        logical_document_id="policy-doc",
        workspace_id="ws-1",
        title="AI Use Policy",
        document_type="company_policy",
        body_text=body_text,
        effective_date=date(2026, 5, 19),
        snapshot_id=snapshot_id,
        version=version,
        created_by="operator-1",
    )
