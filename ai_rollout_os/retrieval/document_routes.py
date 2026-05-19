from collections.abc import Generator

from ai_rollout_os.auth.permissions import require_role
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.retrieval.document_models import (
    DocumentCreate,
    DocumentRead,
    DocumentUpdate,
)
from ai_rollout_os.retrieval.document_service import DocumentService
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

router = APIRouter()
OPERATOR_ACTOR = Depends(require_role("operator"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.post("/documents", response_model=DocumentRead, status_code=201)
def create_document(
    payload: DocumentCreate,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> DocumentRead:
    document = DocumentService(session).create_document(payload, actor)
    session.commit()
    return document_read(document)


@router.put("/documents/{logical_document_id}", response_model=DocumentRead)
def update_document(
    logical_document_id: str,
    payload: DocumentUpdate,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> DocumentRead:
    document = DocumentService(session).update_document(
        logical_document_id, payload, actor
    )
    session.commit()
    return document_read(document)


@router.get(
    "/documents/{logical_document_id}/snapshots/{snapshot_id}",
    response_model=DocumentRead,
)
def get_document_snapshot(
    logical_document_id: str,
    snapshot_id: str,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> DocumentRead:
    document = DocumentService(session).get_snapshot(
        logical_document_id, snapshot_id, actor
    )
    return document_read(document)


def document_read(document) -> DocumentRead:
    return DocumentRead(
        id=document.id,
        logical_document_id=document.logical_document_id,
        workspace_id=document.workspace_id,
        title=document.title,
        document_type=document.document_type,
        body_text=document.body_text,
        effective_date=document.effective_date,
        snapshot_id=document.snapshot_id,
        version=document.version,
    )
