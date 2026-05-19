from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.db.models import Submission


@dataclass(frozen=True)
class FeedbackRecord:
    submission_id: str
    feedback_status: str
    learner_feedback: str | None
    validation_status: str
    missing_evidence_reason: str | None = None


class FeedbackRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def store_needs_human_review(
        self,
        *,
        submission_id: str,
        reason: str | None,
        actor_id: str,
        trace_id: str,
    ) -> FeedbackRecord:
        submission = self._require_submission(submission_id)
        submission.review_state = "needs_human_review"
        AuditEventRepository(self._session).append(
            actor_id=actor_id,
            action="feedback.needs_human_review",
            resource_type="submission",
            resource_id=submission.id,
            result="success",
            trace_id=trace_id,
            details=reason,
        )
        self._session.flush()
        return FeedbackRecord(
            submission_id=submission.id,
            feedback_status="needs_human_review",
            learner_feedback=None,
            validation_status="insufficient_evidence",
            missing_evidence_reason=reason,
        )

    def _require_submission(self, submission_id: str) -> Submission:
        submission = self._session.scalar(
            select(Submission).where(Submission.id == submission_id)
        )
        if submission is None:
            raise ValueError("Submission not found")
        return submission
