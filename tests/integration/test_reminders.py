from datetime import date

from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import AuditEvent, Cohort, MissionAssignment, ReminderJob
from ai_rollout_os.jobs.delivery import DeliveryResult
from ai_rollout_os.jobs.reminders import (
    ASSIGNMENT_DUE_REMINDER,
    QUEUED_WITHOUT_DELIVERY,
    ReminderScheduler,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_scheduler_creates_due_assignment_reminders(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        assignment_id = add_assignment(session, due_date=date(2026, 5, 21))
        session.commit()

    with Session(migrated_engine) as session:
        reminders = ReminderScheduler(
            session=session,
            settings=Settings(reminder_window_days=3),
            today=lambda: date(2026, 5, 19),
        ).run_once()
        session.commit()

    assert len(reminders) == 1
    with Session(migrated_engine) as session:
        reminder = session.scalar(
            select(ReminderJob).where(ReminderJob.assignment_id == assignment_id)
        )
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "reminder.job_created")
        )
    assert reminder is not None
    assert reminder.reminder_type == ASSIGNMENT_DUE_REMINDER
    assert reminder.recipient_id == "learner-1"
    assert reminder.status == QUEUED_WITHOUT_DELIVERY
    assert audit_event is not None


def test_scheduler_is_idempotent_per_assignment(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        assignment_id = add_assignment(session, due_date=date(2026, 5, 21))
        scheduler = ReminderScheduler(
            session=session,
            settings=Settings(reminder_window_days=3),
            today=lambda: date(2026, 5, 19),
        )
        scheduler.run_once()
        scheduler.run_once()
        session.commit()

    with Session(migrated_engine) as session:
        reminders = session.scalars(
            select(ReminderJob).where(ReminderJob.assignment_id == assignment_id)
        ).all()
    assert len(reminders) == 1
    assert reminders[0].idempotency_key == f"assignment:{assignment_id}:assignment_due"


def test_disabled_delivery_makes_no_external_call(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        assignment_id = add_assignment(session, due_date=date(2026, 5, 21))
        delivery = FailingDelivery()
        ReminderScheduler(
            session=session,
            settings=Settings(
                reminder_window_days=3,
                reminder_delivery_enabled=False,
            ),
            delivery=delivery,
            today=lambda: date(2026, 5, 19),
        ).run_once()
        session.commit()

    assert delivery.calls == 0
    with Session(migrated_engine) as session:
        reminder = session.scalar(
            select(ReminderJob).where(ReminderJob.assignment_id == assignment_id)
        )
    assert reminder is not None
    assert reminder.status == QUEUED_WITHOUT_DELIVERY
    assert reminder.delivery_channel is None


def add_assignment(session: Session, *, due_date: date) -> str:
    cohort = Cohort(
        id="cohort-1",
        workspace_id="ws-1",
        role_pack_id="role-pack-1",
        role_pack_version=1,
        manager_id="manager-1",
        start_date=date(2026, 5, 1),
        due_date=due_date,
        status="launched",
        created_by="operator-1",
    )
    assignment = MissionAssignment(
        id="assignment-1",
        cohort_id=cohort.id,
        workspace_id="ws-1",
        learner_id="learner-1",
        mission_template_id="mission-1",
        role_pack_version=1,
        status="assigned",
    )
    session.add_all([cohort, assignment])
    session.flush()
    return assignment.id


class FailingDelivery:
    calls = 0

    def deliver(self, reminder: ReminderJob) -> DeliveryResult:
        self.calls += 1
        raise AssertionError("external delivery should be disabled")
