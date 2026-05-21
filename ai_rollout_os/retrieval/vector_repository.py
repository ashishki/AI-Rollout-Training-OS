from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import uuid4

from ai_rollout_os.db.models import (
    RetrievalChunk,
    RetrievalCorpusVersion,
    SourceDocument,
)
from ai_rollout_os.retrieval.constants import INDEX_SCHEMA_VERSION
from ai_rollout_os.retrieval.document_approval import APPROVED_DOCUMENT_STATUS
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from ai_rollout_os.retrieval.chunking import TextChunk

_RRF_K = 60
_QUERY_RANK_LIMIT = 20


@dataclass(frozen=True)
class RetrievalCandidate:
    chunk: RetrievalChunk
    score: float


class RetrievalVectorRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_corpus_version(
        self,
        *,
        document: SourceDocument,
        embedding_model: str,
        embedding_dimensions: int,
        chunk_count: int,
    ) -> RetrievalCorpusVersion:
        next_version = self._next_version(document)
        corpus_version = RetrievalCorpusVersion(
            id=f"corpus_{uuid4().hex}",
            workspace_id=document.workspace_id,
            source_id=document.logical_document_id,
            source_document_id=document.id,
            snapshot_id=document.snapshot_id,
            version=next_version,
            index_schema_version=INDEX_SCHEMA_VERSION,
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
            chunk_count=chunk_count,
        )
        self._session.add(corpus_version)
        self._session.flush()
        return corpus_version

    def add_chunks(
        self,
        *,
        document: SourceDocument,
        corpus_version: RetrievalCorpusVersion,
        chunks: Sequence[TextChunk],
        embeddings: Sequence[Sequence[float]],
        embedding_model: str,
    ) -> list[RetrievalChunk]:
        stored_chunks = [
            RetrievalChunk(
                id=f"chunk_{uuid4().hex}",
                corpus_version_id=corpus_version.id,
                workspace_id=document.workspace_id,
                source_id=document.logical_document_id,
                source_document_id=document.id,
                snapshot_id=document.snapshot_id,
                section_path=chunk.section_path,
                chunk_index=chunk.chunk_index,
                chunk_text=chunk.text,
                content_hash=_content_hash(chunk.text),
                token_count=chunk.token_count,
                index_schema_version=INDEX_SCHEMA_VERSION,
                embedding_model=embedding_model,
                embedding=list(embedding),
            )
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        self._session.add_all(stored_chunks)
        self._session.flush()
        return stored_chunks

    def _next_version(self, document: SourceDocument) -> int:
        current = self._session.scalar(
            select(func.max(RetrievalCorpusVersion.version)).where(
                RetrievalCorpusVersion.workspace_id == document.workspace_id,
                RetrievalCorpusVersion.source_id == document.logical_document_id,
                RetrievalCorpusVersion.index_schema_version == INDEX_SCHEMA_VERSION,
            )
        )
        return int(current or 0) + 1


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class RetrievalQueryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def hybrid_search(
        self,
        *,
        query_text: str,
        query_embedding: Sequence[float],
        workspace_id: str,
        snapshot_id: str,
        document_type: str,
        min_score: float,
        limit: int,
    ) -> list[RetrievalCandidate]:
        vector_distance = RetrievalChunk.embedding.cosine_distance(
            list(query_embedding)
        )
        vector_rows = self._session.execute(
            select(RetrievalChunk, (1 - vector_distance).label("vector_score"))
            .join(
                SourceDocument,
                RetrievalChunk.source_document_id == SourceDocument.id,
            )
            .where(
                RetrievalChunk.workspace_id == workspace_id,
                RetrievalChunk.snapshot_id == snapshot_id,
                RetrievalChunk.index_schema_version == INDEX_SCHEMA_VERSION,
                SourceDocument.document_type == document_type,
                SourceDocument.approval_status == APPROVED_DOCUMENT_STATUS,
            )
            .order_by(vector_distance)
            .limit(_QUERY_RANK_LIMIT)
        ).all()

        text_vector = func.to_tsvector("english", RetrievalChunk.chunk_text)
        text_query = func.plainto_tsquery("english", query_text)
        text_rank = func.ts_rank_cd(text_vector, text_query)
        fts_rows = self._session.execute(
            select(RetrievalChunk, text_rank.label("text_rank"))
            .join(
                SourceDocument,
                RetrievalChunk.source_document_id == SourceDocument.id,
            )
            .where(
                RetrievalChunk.workspace_id == workspace_id,
                RetrievalChunk.snapshot_id == snapshot_id,
                RetrievalChunk.index_schema_version == INDEX_SCHEMA_VERSION,
                SourceDocument.document_type == document_type,
                SourceDocument.approval_status == APPROVED_DOCUMENT_STATUS,
                text_vector.op("@@")(text_query),
            )
            .order_by(desc(text_rank))
            .limit(_QUERY_RANK_LIMIT)
        ).all()

        scores: dict[str, tuple[RetrievalChunk, float]] = {}
        for rank, row in enumerate(vector_rows, start=1):
            chunk = row[0]
            vector_score = float(row.vector_score or 0.0)
            score = max(vector_score, 0.0) + _reciprocal_rank_score(rank)
            scores[chunk.id] = (chunk, score)

        for rank, row in enumerate(fts_rows, start=1):
            chunk = row[0]
            text_score = float(row.text_rank or 0.0)
            rrf_score = _reciprocal_rank_score(rank)
            existing = scores.get(chunk.id)
            if existing is None:
                scores[chunk.id] = (chunk, text_score + rrf_score)
            else:
                scores[chunk.id] = (existing[0], existing[1] + rrf_score)

        candidates = [
            RetrievalCandidate(chunk=chunk, score=score)
            for chunk, score in scores.values()
            if score >= min_score
        ]
        candidates.sort(key=lambda candidate: candidate.score, reverse=True)
        return candidates[:limit]


def _reciprocal_rank_score(rank: int) -> float:
    return 1.0 / (_RRF_K + rank)
