from dataclasses import dataclass

from ai_rollout_os.db.models import (
    RetrievalChunk,
    RetrievalCorpusVersion,
    SourceDocument,
)
from ai_rollout_os.retrieval.chunking import chunk_source_text
from ai_rollout_os.retrieval.embeddings import EmbeddingClient, validate_embeddings
from ai_rollout_os.retrieval.vector_repository import (
    RetrievalVectorRepository,
)
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class IngestionResult:
    corpus_version: RetrievalCorpusVersion
    chunks: list[RetrievalChunk]


class RetrievalIngestionService:
    def __init__(self, session: Session, embedding_client: EmbeddingClient) -> None:
        self._session = session
        self._embedding_client = embedding_client
        self._repository = RetrievalVectorRepository(session)

    def ingest_source_document(self, document: SourceDocument) -> IngestionResult:
        chunks = chunk_source_text(document.body_text)
        embeddings = self._embedding_client.embed_texts(
            [chunk.text for chunk in chunks]
        )
        validate_embeddings(
            embeddings,
            expected_count=len(chunks),
            dimensions=self._embedding_client.dimensions,
        )
        corpus_version = self._repository.create_corpus_version(
            document=document,
            embedding_model=self._embedding_client.model,
            embedding_dimensions=self._embedding_client.dimensions,
            chunk_count=len(chunks),
        )
        stored_chunks = self._repository.add_chunks(
            document=document,
            corpus_version=corpus_version,
            chunks=chunks,
            embeddings=embeddings,
            embedding_model=self._embedding_client.model,
        )
        self._session.flush()
        return IngestionResult(corpus_version=corpus_version, chunks=stored_chunks)
