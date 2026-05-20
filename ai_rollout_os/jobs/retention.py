from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.db.models import (
    FeedbackResult,
    RetrievalChunk,
    SourceDocument,
    Submission,
)

REDACTED_BY_RETENTION = "[REDACTED_BY_RETENTION]"


@dataclass(frozen=True)
class RetentionResult:
    submissions_redacted: int
    feedback_results_redacted: int
    source_documents_redacted: int
    retrieval_chunks_redacted: int


class RetentionJob:
    def __init__(self, session: Session) -> None:
        self._session = session

    def redact_expired_artifacts(
        self,
        *,
        workspace_id: str,
        retention_days: int,
        actor_id: str = "system",
        trace_id: str,
        now: datetime | None = None,
    ) -> RetentionResult:
        cutoff = (now or datetime.now(UTC)) - timedelta(days=retention_days)
        submissions = self._expired_submissions(workspace_id, cutoff)
        feedback_results = self._expired_feedback_results(workspace_id, cutoff)
        source_documents = self._expired_source_documents(workspace_id, cutoff)
        retrieval_chunks = self._expired_retrieval_chunks(workspace_id, cutoff)

        for submission in submissions:
            submission.artifact_text = REDACTED_BY_RETENTION
            submission.approval_note = None
            submission.approved_workflow_change = None
            submission.rejection_reason = None
            submission.redaction_status = "retention_redacted"
            self._audit_retention(
                actor_id=actor_id,
                resource_type="submission",
                resource_id=submission.id,
                trace_id=trace_id,
            )

        for feedback_result in feedback_results:
            feedback_result.learner_feedback = REDACTED_BY_RETENTION
            self._audit_retention(
                actor_id=actor_id,
                resource_type="feedback_result",
                resource_id=feedback_result.id,
                trace_id=trace_id,
            )

        for source_document in source_documents:
            source_document.body_text = REDACTED_BY_RETENTION
            self._audit_retention(
                actor_id=actor_id,
                resource_type="source_document",
                resource_id=source_document.id,
                trace_id=trace_id,
            )

        for retrieval_chunk in retrieval_chunks:
            retrieval_chunk.chunk_text = REDACTED_BY_RETENTION
            self._audit_retention(
                actor_id=actor_id,
                resource_type="retrieval_chunk",
                resource_id=retrieval_chunk.id,
                trace_id=trace_id,
            )

        self._session.flush()
        return RetentionResult(
            submissions_redacted=len(submissions),
            feedback_results_redacted=len(feedback_results),
            source_documents_redacted=len(source_documents),
            retrieval_chunks_redacted=len(retrieval_chunks),
        )

    def _expired_submissions(
        self, workspace_id: str, cutoff: datetime
    ) -> list[Submission]:
        return list(
            self._session.scalars(
                select(Submission).where(
                    Submission.workspace_id == workspace_id,
                    Submission.created_at < cutoff,
                    Submission.artifact_text != REDACTED_BY_RETENTION,
                )
            )
        )

    def _expired_feedback_results(
        self, workspace_id: str, cutoff: datetime
    ) -> list[FeedbackResult]:
        return list(
            self._session.scalars(
                select(FeedbackResult).where(
                    FeedbackResult.workspace_id == workspace_id,
                    FeedbackResult.created_at < cutoff,
                    FeedbackResult.learner_feedback.is_not(None),
                    FeedbackResult.learner_feedback != REDACTED_BY_RETENTION,
                )
            )
        )

    def _expired_source_documents(
        self, workspace_id: str, cutoff: datetime
    ) -> list[SourceDocument]:
        return list(
            self._session.scalars(
                select(SourceDocument).where(
                    SourceDocument.workspace_id == workspace_id,
                    SourceDocument.created_at < cutoff,
                    SourceDocument.body_text != REDACTED_BY_RETENTION,
                )
            )
        )

    def _expired_retrieval_chunks(
        self, workspace_id: str, cutoff: datetime
    ) -> list[RetrievalChunk]:
        return list(
            self._session.scalars(
                select(RetrievalChunk).where(
                    RetrievalChunk.workspace_id == workspace_id,
                    RetrievalChunk.created_at < cutoff,
                    RetrievalChunk.chunk_text != REDACTED_BY_RETENTION,
                )
            )
        )

    def _audit_retention(
        self,
        *,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        trace_id: str,
    ) -> None:
        AuditEventRepository(self._session).append(
            actor_id=actor_id,
            action="retention.redacted",
            resource_type=resource_type,
            resource_id=resource_id,
            result="success",
            trace_id=trace_id,
        )
