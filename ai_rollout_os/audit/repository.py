from sqlalchemy.orm import Session

from ai_rollout_os.db.models import AuditEvent


class AuditEventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def append(
        self,
        *,
        actor_id: str | None,
        action: str,
        resource_type: str,
        resource_id: str,
        result: str,
        trace_id: str,
        details: str | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            result=result,
            trace_id=trace_id,
            details=details,
        )
        self._session.add(event)
        self._session.flush()
        return event
