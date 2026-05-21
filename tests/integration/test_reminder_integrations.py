from datetime import date
from typing import Any

import pytest
from ai_rollout_os.core.config import ConfigError, Settings, get_settings
from ai_rollout_os.db.models import ReminderJob
from ai_rollout_os.jobs.delivery import build_reminder_delivery
from ai_rollout_os.jobs.reminders import (
    RETRYABLE_DELIVERY_FAILED,
    ReminderScheduler,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_reminders import add_assignment


def test_reminder_adapters_disabled_by_default(migrated_engine: Engine) -> None:
    transport = RecordingTransport()
    settings = get_settings({"APP_ENV": "test"})

    with Session(migrated_engine) as session:
        assignment_id = add_assignment(session, due_date=date(2026, 5, 21))
        ReminderScheduler(
            session=session,
            settings=settings,
            delivery=build_reminder_delivery(settings, transport=transport),
            today=lambda: date(2026, 5, 19),
        ).run_once()
        session.commit()

    assert transport.calls == []
    with Session(migrated_engine) as session:
        reminder = session.scalar(
            select(ReminderJob).where(ReminderJob.assignment_id == assignment_id)
        )
    assert reminder is not None
    assert reminder.delivery_channel is None

    with pytest.raises(ConfigError, match="REMINDER_DELIVERY_CHANNEL"):
        get_settings(
            {
                "APP_ENV": "test",
                "REMINDER_DELIVERY_ENABLED": "true",
            }
        )


def test_reminder_delivery_failure_is_retryable(migrated_engine: Engine) -> None:
    transport = FailingTransport()
    settings = Settings(
        reminder_window_days=3,
        reminder_delivery_enabled=True,
        reminder_delivery_channel="slack",
        slack_webhook_url="https://hooks.slack.test/reminder",
    )

    with Session(migrated_engine) as session:
        assignment_id = add_assignment(session, due_date=date(2026, 5, 21))
        scheduler = ReminderScheduler(
            session=session,
            settings=settings,
            delivery=build_reminder_delivery(settings, transport=transport),
            today=lambda: date(2026, 5, 19),
        )
        scheduler.run_once()
        scheduler.run_once()
        session.commit()

    assert len(transport.calls) == 1
    with Session(migrated_engine) as session:
        reminders = session.scalars(
            select(ReminderJob).where(ReminderJob.assignment_id == assignment_id)
        ).all()
    assert len(reminders) == 1
    assert reminders[0].status == RETRYABLE_DELIVERY_FAILED
    assert reminders[0].delivery_channel == "slack"


class RecordingTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def post_json(
        self, *, url: str, payload: dict[str, Any], idempotency_key: str
    ) -> None:
        self.calls.append(
            {"url": url, "payload": payload, "idempotency_key": idempotency_key}
        )


class FailingTransport(RecordingTransport):
    def post_json(
        self, *, url: str, payload: dict[str, Any], idempotency_key: str
    ) -> None:
        super().post_json(url=url, payload=payload, idempotency_key=idempotency_key)
        raise RuntimeError("transient webhook failure")
