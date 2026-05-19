from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.db.models import AuditEvent
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_append_audit_event_persists_required_fields(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        repository = AuditEventRepository(session)

        event = repository.append(
            actor_id="actor-1",
            action="submission.created",
            resource_type="submission",
            resource_id="submission-1",
            result="success",
            trace_id="trace-1",
        )
        session.commit()

        stored = session.scalar(select(AuditEvent).where(AuditEvent.id == event.id))

    assert stored is not None
    assert stored.timestamp is not None
    assert stored.actor_id == "actor-1"
    assert stored.action == "submission.created"
    assert stored.resource_type == "submission"
    assert stored.resource_id == "submission-1"
    assert stored.result == "success"
    assert stored.trace_id == "trace-1"


def test_audit_repository_has_no_mutation_methods() -> None:
    public_methods = {
        name
        for name in dir(AuditEventRepository)
        if not name.startswith("_") and callable(getattr(AuditEventRepository, name))
    }

    assert public_methods == {"append"}
