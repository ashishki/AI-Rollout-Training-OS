import json
from dataclasses import dataclass
from typing import Any, Protocol
from urllib import request

from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import ReminderJob

SENT = "sent"
SUPPORTED_REMINDER_CHANNELS = {"slack", "teams"}


@dataclass(frozen=True)
class DeliveryResult:
    channel: str
    status: str


class WebhookTransport(Protocol):
    def post_json(
        self, *, url: str, payload: dict[str, Any], idempotency_key: str
    ) -> None:
        pass


class ReminderDeliveryAdapter(Protocol):
    def deliver(self, reminder: ReminderJob) -> DeliveryResult:
        pass


class DisabledReminderDelivery:
    def deliver(self, reminder: ReminderJob) -> DeliveryResult:
        raise RuntimeError("Reminder delivery is disabled")


class WebhookReminderDelivery:
    def __init__(
        self, *, channel: str, webhook_url: str, transport: WebhookTransport
    ) -> None:
        if channel not in SUPPORTED_REMINDER_CHANNELS:
            raise ValueError("Unsupported reminder delivery channel")
        self._channel = channel
        self._webhook_url = webhook_url
        self._transport = transport

    def deliver(self, reminder: ReminderJob) -> DeliveryResult:
        self._transport.post_json(
            url=self._webhook_url,
            payload=_safe_payload(reminder),
            idempotency_key=reminder.idempotency_key,
        )
        return DeliveryResult(channel=self._channel, status=SENT)


class UrlLibWebhookTransport:
    def post_json(
        self, *, url: str, payload: dict[str, Any], idempotency_key: str
    ) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        req = request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Idempotency-Key": idempotency_key,
            },
            method="POST",
        )
        with request.urlopen(req, timeout=10) as response:
            response.read()


def build_reminder_delivery(
    settings: Settings, *, transport: WebhookTransport | None = None
) -> ReminderDeliveryAdapter:
    if not settings.reminder_delivery_enabled:
        return DisabledReminderDelivery()
    channel = settings.reminder_delivery_channel
    webhook_url = (
        settings.slack_webhook_url if channel == "slack" else settings.teams_webhook_url
    )
    if channel is None or webhook_url is None:
        raise RuntimeError(
            "Reminder delivery requires explicit channel and webhook URL"
        )
    return WebhookReminderDelivery(
        channel=channel,
        webhook_url=webhook_url,
        transport=transport or UrlLibWebhookTransport(),
    )


def _safe_payload(reminder: ReminderJob) -> dict[str, Any]:
    return {
        "reminder_id": reminder.id,
        "reminder_type": reminder.reminder_type,
        "recipient_id": reminder.recipient_id,
        "assignment_id": reminder.assignment_id,
        "submission_id": reminder.submission_id,
        "feedback_job_id": reminder.feedback_job_id,
        "due_date": reminder.due_date.isoformat() if reminder.due_date else None,
    }
