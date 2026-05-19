from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.db.models import FeedbackJob, Submission
from ai_rollout_os.jobs.models import FeedbackJobStatus

READY_FOR_FEEDBACK_STATES = {"ready_for_feedback", "approved_for_feedback"}


class FeedbackJobService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def enqueue_ready_submission(
        self,
        *,
        submission_id: str,
        trace_id: str = "trace-feedback-job",
    ) -> FeedbackJob:
        submission = self._require_submission(submission_id)
        if submission.review_state not in READY_FOR_FEEDBACK_STATES:
            raise ValueError("Submission is not ready for feedback")

        key = idempotency_key(submission.id, submission.version)
        existing = self._session.scalar(
            select(FeedbackJob).where(FeedbackJob.idempotency_key == key)
        )
        if existing is not None:
            return existing

        job = FeedbackJob(
            id=f"feedback_job_{uuid4().hex}",
            workspace_id=submission.workspace_id,
            submission_id=submission.id,
            submission_version=submission.version,
            idempotency_key=key,
            status=FeedbackJobStatus.QUEUED,
            attempt_count=0,
        )
        self._session.add(job)
        AuditEventRepository(self._session).append(
            actor_id="system",
            action="feedback.job_enqueued",
            resource_type="submission",
            resource_id=submission.id,
            result="success",
            trace_id=trace_id,
        )
        self._session.flush()
        return job

    def _require_submission(self, submission_id: str) -> Submission:
        submission = self._session.scalar(
            select(Submission).where(Submission.id == submission_id)
        )
        if submission is None:
            raise ValueError("Submission not found")
        return submission


def idempotency_key(submission_id: str, submission_version: int) -> str:
    return f"{submission_id}:{submission_version}"
