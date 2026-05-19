from dataclasses import dataclass
from typing import Protocol

from ai_rollout_os.db.models import ReminderJob


@dataclass(frozen=True)
class DeliveryResult:
    channel: str
    status: str


class ReminderDeliveryAdapter(Protocol):
    def deliver(self, reminder: ReminderJob) -> DeliveryResult:
        pass


class DisabledReminderDelivery:
    def deliver(self, reminder: ReminderJob) -> DeliveryResult:
        raise RuntimeError("Reminder delivery is disabled")
