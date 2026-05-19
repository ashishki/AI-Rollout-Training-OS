from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent, FeedbackJob, FeedbackResult, Submission
from ai_rollout_os.feedback.jobs import FeedbackJobService
from ai_rollout_os.jobs.models import FeedbackJobStatus, GeneratedFeedback
from ai_rollout_os.jobs.worker import FeedbackWorker, TransientFeedbackError
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_submission_enqueues_one_feedback_job(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        submission = ready_submission()
        session.add(submission)
        session.commit()

        service = FeedbackJobService(session)
        first = service.enqueue_ready_submission(submission_id=submission.id)
        second = service.enqueue_ready_submission(submission_id=submission.id)
        session.commit()

        jobs = session.scalars(select(FeedbackJob)).all()
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "feedback.job_enqueued")
        )

    assert first.id == second.id
    assert len(jobs) == 1
    assert jobs[0].idempotency_key == "submission-1:1"
    assert jobs[0].status == FeedbackJobStatus.QUEUED
    assert audit_event is not None
    assert audit_event.resource_id == "submission-1"


def test_retry_does_not_duplicate_feedback(migrated_engine: Engine) -> None:
    evaluator = FlakyEvaluator()
    with Session(migrated_engine) as session:
        submission = ready_submission()
        session.add(submission)
        session.commit()
        FeedbackJobService(session).enqueue_ready_submission(
            submission_id=submission.id
        )
        session.commit()

        worker = FeedbackWorker(
            session=session,
            settings=get_settings({"APP_ENV": "test"}),
            evaluator=evaluator,
        )
        failed = worker.run_one()
        assert failed is not None
        failed_status = failed.status
        failed_id = failed.id
        session.commit()
        completed = worker.run_one()
        assert completed is not None
        completed_id = completed.id
        completed_status = completed.status
        completed_attempt_count = completed.attempt_count
        session.commit()

        results = session.scalars(select(FeedbackResult)).all()

    assert failed_status == FeedbackJobStatus.RETRYABLE_FAILED
    assert completed_status == FeedbackJobStatus.COMPLETED
    assert completed_id == failed_id
    assert completed_attempt_count == 2
    assert len(results) == 1
    assert results[0].submission_id == "submission-1"


def test_timeout_routes_submission_to_review(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        submission = ready_submission()
        session.add(submission)
        session.commit()
        FeedbackJobService(session).enqueue_ready_submission(
            submission_id=submission.id
        )
        session.commit()

        worker = FeedbackWorker(
            session=session,
            settings=get_settings({"APP_ENV": "test", "FEEDBACK_TIMEOUT_SECONDS": "1"}),
            evaluator=lambda _job: GeneratedFeedback(
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
            ),
            clock=SequenceClock([0.0, 2.0]),
        )
        job = worker.run_one()
        assert job is not None
        job_status = job.status
        session.commit()

        stored = session.scalar(
            select(Submission).where(Submission.id == submission.id)
        )
        results = session.scalars(select(FeedbackResult)).all()
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "feedback.job_timed_out")
        )

    assert job_status == FeedbackJobStatus.TIMED_OUT
    assert stored is not None
    assert stored.review_state == "needs_human_review"
    assert results == []
    assert audit_event is not None


class FlakyEvaluator:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, _job: FeedbackJob) -> GeneratedFeedback:
        self.calls += 1
        if self.calls == 1:
            raise TransientFeedbackError("temporary provider failure")
        return GeneratedFeedback(
            feedback_status="ready_for_manager_review",
            learner_feedback="Use approved evidence.",
            validation_status="valid",
        )


class SequenceClock:
    def __init__(self, values: list[float]) -> None:
        self._values = values

    def __call__(self) -> float:
        return self._values.pop(0)


def ready_submission() -> Submission:
    return Submission(
        id="submission-1",
        workspace_id="ws-1",
        mission_template_id="mission-1",
        assignment_id="assignment-1",
        learner_id="learner-1",
        artifact_text="Draft workflow artifact.",
        policy_snapshot_id="snapshot-1",
        rubric_id="rubric-1",
        version=1,
        review_state="ready_for_feedback",
        redaction_status="clear",
    )
