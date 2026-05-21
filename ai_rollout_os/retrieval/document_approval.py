from datetime import UTC, datetime

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import SourceDocument
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

APPROVED_DOCUMENT_STATUS = "approved"
PENDING_DOCUMENT_STATUS = "pending"
HUMAN_POLICY_APPROVER_ROLES = frozenset({"operator", "manager"})


class DocumentApprovalService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def approve_snapshot(
        self,
        *,
        logical_document_id: str,
        snapshot_id: str,
        actor: ActorContext,
    ) -> SourceDocument:
        if actor.role not in HUMAN_POLICY_APPROVER_ROLES or actor.actor_id == "system":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
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
        document.approval_status = APPROVED_DOCUMENT_STATUS
        document.approved_by = actor.actor_id
        document.approved_at = datetime.now(UTC)
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="document.approved",
            resource_type="source_document",
            resource_id=document.snapshot_id,
            result="success",
            trace_id=actor.trace_id,
        )
        self._session.flush()
        return document
