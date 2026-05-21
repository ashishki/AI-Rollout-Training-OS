from datetime import date

import pytest
from ai_rollout_os.auth.tokens import ActorContext, create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import (
    AuditEvent,
    RetrievalChunk,
    RetrievalCorpusVersion,
    SourceDocument,
)
from ai_rollout_os.main import create_app
from ai_rollout_os.retrieval.document_approval import DocumentApprovalService
from ai_rollout_os.retrieval.query import RetrievalQueryService
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class MapEmbeddingClient:
    model = "test-embedding-model"
    dimensions = 8

    def __init__(self, vectors: dict[str, list[float]]) -> None:
        self._vectors = vectors

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._vectors[text] for text in texts]


def test_unapproved_policy_not_retrieved(migrated_engine: Engine) -> None:
    query_text = "approved policy retrieval"
    with Session(migrated_engine) as session:
        seed_policy_chunk(session, approval_status="pending")
        session.commit()

        pending_result = RetrievalQueryService(
            session=session,
            embedding_client=MapEmbeddingClient(
                {query_text: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
            ),
        ).retrieve(
            query_text=query_text,
            workspace_id="ws-1",
            snapshot_id="snapshot-policy-v1",
            document_type="company_policy",
            min_score=0.01,
        )

    assert pending_result.status == "insufficient_evidence"
    assert pending_result.evidence == []

    client = policy_client(migrated_engine)
    approval = client.post(
        "/documents/policy-1/snapshots/snapshot-policy-v1/approval",
        headers=auth_headers("operator-1", "operator"),
    )
    assert approval.status_code == 200
    assert approval.json()["approval_status"] == "approved"

    with Session(migrated_engine) as session:
        approved_result = RetrievalQueryService(
            session=session,
            embedding_client=MapEmbeddingClient(
                {query_text: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
            ),
        ).retrieve(
            query_text=query_text,
            workspace_id="ws-1",
            snapshot_id="snapshot-policy-v1",
            document_type="company_policy",
            min_score=0.01,
        )

    assert approved_result.status == "evidence_found"
    assert [block.chunk_id for block in approved_result.evidence] == ["chunk-policy"]


def test_policy_approval_is_human_owned(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        seed_policy_chunk(session, approval_status="pending")
        session.commit()

        with pytest.raises(HTTPException) as exc_info:
            DocumentApprovalService(session).approve_snapshot(
                logical_document_id="policy-1",
                snapshot_id="snapshot-policy-v1",
                actor=ActorContext(
                    actor_id="system",
                    role="system",
                    workspace_id="ws-1",
                    trace_id="trace-ai-approval",
                ),
            )

        document = session.scalar(
            select(SourceDocument).where(
                SourceDocument.snapshot_id == "snapshot-policy-v1"
            )
        )
        events = session.scalars(select(AuditEvent)).all()

    assert exc_info.value.status_code == 403
    assert document is not None
    assert document.approval_status == "pending"
    assert events == []


def seed_policy_chunk(session: Session, *, approval_status: str) -> None:
    document = SourceDocument(
        id="docver-policy-v1",
        logical_document_id="policy-1",
        workspace_id="ws-1",
        title="AI Use Policy",
        document_type="company_policy",
        body_text="Approved policy retrieval requires human approval.",
        effective_date=date(2026, 5, 21),
        snapshot_id="snapshot-policy-v1",
        version=1,
        created_by="operator-1",
        approval_status=approval_status,
    )
    corpus = RetrievalCorpusVersion(
        id="corpus-policy-v1",
        workspace_id="ws-1",
        source_id="policy-1",
        source_document_id=document.id,
        snapshot_id=document.snapshot_id,
        version=1,
        index_schema_version="v1",
        embedding_model="test-embedding-model",
        embedding_dimensions=8,
        chunk_count=1,
    )
    chunk = RetrievalChunk(
        id="chunk-policy",
        corpus_version_id=corpus.id,
        workspace_id="ws-1",
        source_id="policy-1",
        source_document_id=document.id,
        snapshot_id=document.snapshot_id,
        section_path="Policy > Approval",
        chunk_index=0,
        chunk_text="Approved policy retrieval requires human approval.",
        content_hash="hash-policy",
        token_count=8,
        index_schema_version="v1",
        embedding_model="test-embedding-model",
        embedding=[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    )
    session.add_all([document, corpus, chunk])


def policy_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}),
        session_factory=session_factory,
    )
    return TestClient(app)


def auth_headers(actor_id: str, role: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-policy-approval"}
