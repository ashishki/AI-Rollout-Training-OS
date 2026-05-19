from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import (
    Cohort,
    FeedbackJob,
    MissionAssignment,
    ReminderJob,
    Submission,
)
from ai_rollout_os.jobs.delivery import (
    DisabledReminderDelivery,
    ReminderDeliveryAdapter,
)

ASSIGNMENT_DUE_REMINDER = "assignment_due"
MANAGER_REVIEW_BACKLOG_REMINDER = "manager_review_backlog"
STALE_FEEDBACK_JOB_REMINDER = "stale_feedback_job"
QUEUED_WITHOUT_DELIVERY = "queued_without_delivery"
QUEUED_FOR_DELIVERY = "queued"

DateProvider = Callable[[], date]


class ReminderScheduler:
    def __init__(
        self,
        *,
        session: Session,
        settings: Settings,
        delivery: ReminderDeliveryAdapter | None = None,
        today: DateProvider | None = None,
    ) -> None:
        self._session = session
        self._settings = settings
        self._delivery = delivery or DisabledReminderDelivery()
        self._today = today or (lambda: datetime.now(UTC).date())

    def run_once(
        self, *, trace_id: str = "trace-reminder-scheduler"
    ) -> list[ReminderJob]:
        reminders: list[ReminderJob] = []
        reminders.extend(self._schedule_assignment_due_reminders(trace_id))
        reminders.extend(self._schedule_manager_review_backlog_reminders(trace_id))
        reminders.extend(self._schedule_stale_feedback_job_reminders(trace_id))
        self._session.flush()
        return reminders

    def _schedule_assignment_due_reminders(self, trace_id: str) -> list[ReminderJob]:
        today = self._today()
        latest_due_date = today + timedelta(days=self._settings.reminder_window_days)
        rows = self._session.execute(
            select(MissionAssignment, Cohort)
            .join(Cohort, MissionAssignment.cohort_id == Cohort.id)
            .where(
                Cohort.due_date >= today,
                Cohort.due_date <= latest_due_date,
                MissionAssignment.status != "completed",
            )
            .order_by(MissionAssignment.created_at, MissionAssignment.id)
        ).all()

        reminders: list[ReminderJob] = []
        for assignment, cohort in rows:
            reminders.append(
                self._get_or_create(
                    reminder_type=ASSIGNMENT_DUE_REMINDER,
                    workspace_id=assignment.workspace_id,
                    recipient_id=assignment.learner_id,
                    trace_id=trace_id,
                    assignment_id=assignment.id,
                    due_date=cohort.due_date,
                )
            )
        return reminders

    def _schedule_manager_review_backlog_reminders(
        self, trace_id: str
    ) -> list[ReminderJob]:
        rows = self._session.execute(
            select(Submission, Cohort)
            .join(MissionAssignment, Submission.assignment_id == MissionAssignment.id)
            .join(Cohort, MissionAssignment.cohort_id == Cohort.id)
            .where(Submission.review_state == "needs_human_review")
            .order_by(Submission.created_at, Submission.id)
        ).all()

        reminders: list[ReminderJob] = []
        for submission, cohort in rows:
            reminders.append(
                self._get_or_create(
                    reminder_type=MANAGER_REVIEW_BACKLOG_REMINDER,
                    workspace_id=submission.workspace_id,
                    recipient_id=cohort.manager_id,
                    trace_id=trace_id,
                    submission_id=submission.id,
                    due_date=cohort.due_date,
                )
            )
        return reminders

    def _schedule_stale_feedback_job_reminders(
        self, trace_id: str
    ) -> list[ReminderJob]:
        rows = self._session.execute(
            select(FeedbackJob, Submission, Cohort)
            .join(Submission, FeedbackJob.submission_id == Submission.id)
            .join(MissionAssignment, Submission.assignment_id == MissionAssignment.id)
            .join(Cohort, MissionAssignment.cohort_id == Cohort.id)
            .where(FeedbackJob.status.in_(["queued", "retryable_failed", "running"]))
            .order_by(FeedbackJob.created_at, FeedbackJob.id)
        ).all()

        reminders: list[ReminderJob] = []
        for feedback_job, _submission, cohort in rows:
            reminders.append(
                self._get_or_create(
                    reminder_type=STALE_FEEDBACK_JOB_REMINDER,
                    workspace_id=feedback_job.workspace_id,
                    recipient_id=cohort.manager_id,
                    trace_id=trace_id,
                    feedback_job_id=feedback_job.id,
                    due_date=cohort.due_date,
                )
            )
        return reminders

    def _get_or_create(
        self,
        *,
        reminder_type: str,
        workspace_id: str,
        recipient_id: str,
        trace_id: str,
        assignment_id: str | None = None,
        submission_id: str | None = None,
        feedback_job_id: str | None = None,
        due_date: date | None = None,
    ) -> ReminderJob:
        key = reminder_idempotency_key(
            reminder_type=reminder_type,
            assignment_id=assignment_id,
            submission_id=submission_id,
            feedback_job_id=feedback_job_id,
        )
        existing = self._session.scalar(
            select(ReminderJob).where(ReminderJob.idempotency_key == key)
        )
        if existing is not None:
            return existing

        reminder = ReminderJob(
            id=f"reminder_job_{uuid4().hex}",
            workspace_id=workspace_id,
            reminder_type=reminder_type,
            idempotency_key=key,
            recipient_id=recipient_id,
            assignment_id=assignment_id,
            submission_id=submission_id,
            feedback_job_id=feedback_job_id,
            status=QUEUED_WITHOUT_DELIVERY,
            delivery_channel=None,
            due_date=due_date,
        )
        self._session.add(reminder)
        if self._settings.reminder_delivery_enabled:
            result = self._delivery.deliver(reminder)
            reminder.delivery_channel = result.channel
            reminder.status = result.status or QUEUED_FOR_DELIVERY
        AuditEventRepository(self._session).append(
            actor_id="system",
            action="reminder.job_created",
            resource_type="reminder_job",
            resource_id=reminder.id,
            result="success",
            trace_id=trace_id,
            details=reminder_type,
        )
        self._session.flush()
        return reminder


def reminder_idempotency_key(
    *,
    reminder_type: str,
    assignment_id: str | None = None,
    submission_id: str | None = None,
    feedback_job_id: str | None = None,
) -> str:
    if assignment_id is not None:
        return f"assignment:{assignment_id}:{reminder_type}"
    if submission_id is not None:
        return f"submission:{submission_id}:{reminder_type}"
    if feedback_job_id is not None:
        return f"feedback_job:{feedback_job_id}:{reminder_type}"
    raise ValueError("Reminder idempotency key requires a resource id")
