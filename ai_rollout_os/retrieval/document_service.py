import logging
from uuid import uuid4

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import SourceDocument
from ai_rollout_os.retrieval.document_models import (
    DOCUMENT_TYPES,
    DocumentCreate,
    DocumentUpdate,
)
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_document(
        self, payload: DocumentCreate, actor: ActorContext
    ) -> SourceDocument:
        self._validate_document_type(payload.document_type)
        logical_document_id = f"doc_{uuid4().hex}"
        document = SourceDocument(
            id=f"docver_{uuid4().hex}",
            logical_document_id=logical_document_id,
            workspace_id=actor.workspace_id,
            title=payload.title,
            document_type=payload.document_type,
            body_text=payload.body_text,
            effective_date=payload.effective_date,
            snapshot_id=f"snapshot_{uuid4().hex}",
            version=1,
            created_by=actor.actor_id,
        )
        self._session.add(document)
        self._session.flush()
        self._audit_document_change(document, actor, "document.created")
        logger.info(
            "source_document_created",
            extra={
                "operation": "documents.create",
                "result": "success",
                "workspace_id": actor.workspace_id,
                "document_type": payload.document_type,
                "snapshot_id": document.snapshot_id,
            },
        )
        return document

    def update_document(
        self,
        logical_document_id: str,
        payload: DocumentUpdate,
        actor: ActorContext,
    ) -> SourceDocument:
        self._validate_document_type(payload.document_type)
        latest = self._latest_document(logical_document_id, actor)
        document = SourceDocument(
            id=f"docver_{uuid4().hex}",
            logical_document_id=latest.logical_document_id,
            workspace_id=actor.workspace_id,
            title=payload.title,
            document_type=payload.document_type,
            body_text=payload.body_text,
            effective_date=payload.effective_date,
            snapshot_id=f"snapshot_{uuid4().hex}",
            version=latest.version + 1,
            created_by=actor.actor_id,
        )
        self._session.add(document)
        self._session.flush()
        self._audit_document_change(document, actor, "document.updated")
        logger.info(
            "source_document_updated",
            extra={
                "operation": "documents.update",
                "result": "success",
                "workspace_id": actor.workspace_id,
                "document_type": payload.document_type,
                "snapshot_id": document.snapshot_id,
            },
        )
        return document

    def get_snapshot(
        self, logical_document_id: str, snapshot_id: str, actor: ActorContext
    ) -> SourceDocument:
        document = self._session.scalar(
            select(SourceDocument).where(
                SourceDocument.logical_document_id == logical_document_id,
                SourceDocument.snapshot_id == snapshot_id,
                SourceDocument.workspace_id == actor.workspace_id,
            )
        )
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
            )
        return document

    def _latest_document(
        self, logical_document_id: str, actor: ActorContext
    ) -> SourceDocument:
        document = self._session.scalar(
            select(SourceDocument)
            .where(
                SourceDocument.logical_document_id == logical_document_id,
                SourceDocument.workspace_id == actor.workspace_id,
            )
            .order_by(SourceDocument.version.desc())
            .limit(1)
        )
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
            )
        return document

    def _validate_document_type(self, document_type: str) -> None:
        if document_type not in DOCUMENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Unsupported document type",
            )

    def _audit_document_change(
        self, document: SourceDocument, actor: ActorContext, action: str
    ) -> None:
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action=action,
            resource_type="source_document",
            resource_id=document.snapshot_id,
            result="success",
            trace_id=actor.trace_id,
        )
