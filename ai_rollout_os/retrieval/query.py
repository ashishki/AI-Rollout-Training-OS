from ai_rollout_os.retrieval.embeddings import EmbeddingClient, validate_embeddings
from ai_rollout_os.retrieval.evidence import (
    EvidenceBlock,
    RetrievalResult,
    citation_snippet,
)
from ai_rollout_os.retrieval.vector_repository import RetrievalQueryRepository
from sqlalchemy.orm import Session


class RetrievalQueryService:
    def __init__(self, session: Session, embedding_client: EmbeddingClient) -> None:
        self._embedding_client = embedding_client
        self._repository = RetrievalQueryRepository(session)

    def retrieve(
        self,
        *,
        query_text: str,
        workspace_id: str,
        snapshot_id: str,
        document_type: str,
        min_score: float,
        limit: int = 5,
    ) -> RetrievalResult:
        embeddings = self._embedding_client.embed_texts([query_text])
        validate_embeddings(
            embeddings,
            expected_count=1,
            dimensions=self._embedding_client.dimensions,
        )
        candidates = self._repository.hybrid_search(
            query_text=query_text,
            query_embedding=embeddings[0],
            workspace_id=workspace_id,
            snapshot_id=snapshot_id,
            document_type=document_type,
            min_score=min_score,
            limit=limit,
        )
        if not candidates:
            return RetrievalResult(
                status="insufficient_evidence",
                evidence=[],
                generated_answer=None,
                reason="no_chunk_above_threshold",
            )

        evidence = [
            EvidenceBlock(
                source_id=candidate.chunk.source_id,
                section_path=candidate.chunk.section_path,
                chunk_id=candidate.chunk.id,
                score=candidate.score,
                snippet=citation_snippet(candidate.chunk.chunk_text),
            )
            for candidate in candidates
        ]
        return RetrievalResult(status="evidence_found", evidence=evidence)
