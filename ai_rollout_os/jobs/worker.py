import time
from collections.abc import Callable
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import FeedbackJob, FeedbackResult, Submission
from ai_rollout_os.jobs.models import FeedbackJobStatus, GeneratedFeedback


class TransientFeedbackError(RuntimeError):
    pass


FeedbackEvaluator = Callable[[FeedbackJob], GeneratedFeedback]
Clock = Callable[[], float]


class FeedbackWorker:
    def __init__(
        self,
        *,
        session: Session,
        settings: Settings,
        evaluator: FeedbackEvaluator,
        clock: Clock = time.monotonic,
    ) -> None:
        self._session = session
        self._settings = settings
        self._evaluator = evaluator
        self._clock = clock

    def run_one(self) -> FeedbackJob | None:
        job = self._next_job()
        if job is None:
            return None

        job.status = FeedbackJobStatus.RUNNING
        job.attempt_count += 1
        started_at = self._clock()
        try:
            generated = self._evaluator(job)
        except TransientFeedbackError as exc:
            job.status = FeedbackJobStatus.RETRYABLE_FAILED
            job.last_error = exc.__class__.__name__
            self._audit(job, "feedback.job_retryable_failed")
            self._session.flush()
            return job

        elapsed_seconds = self._clock() - started_at
        if elapsed_seconds > self._settings.feedback_timeout_seconds:
            job.status = FeedbackJobStatus.TIMED_OUT
            self._route_submission_to_review(job)
            self._audit(job, "feedback.job_timed_out")
            self._session.flush()
            return job

        self._store_feedback_result(job, generated)
        job.status = FeedbackJobStatus.COMPLETED
        job.last_error = None
        self._audit(job, "feedback.job_completed")
        self._session.flush()
        return job

    def _next_job(self) -> FeedbackJob | None:
        return self._session.scalar(
            select(FeedbackJob)
            .where(
                FeedbackJob.status.in_(
                    [
                        FeedbackJobStatus.QUEUED,
                        FeedbackJobStatus.RETRYABLE_FAILED,
                    ]
                )
            )
            .order_by(FeedbackJob.created_at, FeedbackJob.id)
            .limit(1)
        )

    def _store_feedback_result(
        self, job: FeedbackJob, generated: GeneratedFeedback
    ) -> FeedbackResult:
        existing = self._session.scalar(
            select(FeedbackResult).where(
                FeedbackResult.submission_id == job.submission_id,
                FeedbackResult.submission_version == job.submission_version,
            )
        )
        if existing is None:
            result = FeedbackResult(
                id=f"feedback_result_{uuid4().hex}",
                workspace_id=job.workspace_id,
                submission_id=job.submission_id,
                submission_version=job.submission_version,
                feedback_status=generated.feedback_status,
                learner_feedback=generated.learner_feedback,
                validation_status=generated.validation_status,
                risk_flags=generated.risk_flags or [],
            )
            self._session.add(result)
            return result

        existing.feedback_status = generated.feedback_status
        existing.learner_feedback = generated.learner_feedback
        existing.validation_status = generated.validation_status
        existing.risk_flags = generated.risk_flags or []
        return existing

    def _route_submission_to_review(self, job: FeedbackJob) -> None:
        submission = self._session.scalar(
            select(Submission).where(Submission.id == job.submission_id)
        )
        if submission is not None:
            submission.review_state = "needs_human_review"

    def _audit(self, job: FeedbackJob, action: str) -> None:
        AuditEventRepository(self._session).append(
            actor_id="system",
            action=action,
            resource_type="feedback_job",
            resource_id=job.id,
            result="success",
            trace_id="trace-feedback-worker",
        )
