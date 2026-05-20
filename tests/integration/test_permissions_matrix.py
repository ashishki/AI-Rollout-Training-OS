from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_denied_permission_is_audited(migrated_engine: Engine) -> None:
    session_factory = sessionmaker(bind=migrated_engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    response = TestClient(app).post(
        "/documents",
        headers={
            "authorization": f"Bearer {learner_token()}",
            "x-trace-id": "trace-permission-denied",
        },
        json={
            "title": "Policy",
            "document_type": "company_policy",
            "body_text": "Use approved tools only.",
            "effective_date": "2026-05-20",
        },
    )

    assert response.status_code == 403
    with Session(migrated_engine) as session:
        events = session.scalars(select(AuditEvent).order_by(AuditEvent.id)).all()
    assert [
        {
            "actor_id": event.actor_id,
            "action": event.action,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "result": event.result,
            "trace_id": event.trace_id,
        }
        for event in events
    ] == [
        {
            "actor_id": "learner-1",
            "action": "denied_access",
            "resource_type": "permission",
            "resource_id": "documents.create",
            "result": "denied",
            "trace_id": "trace-permission-denied",
        }
    ]


def learner_token() -> str:
    return create_token(
        actor_id="learner-1",
        role="learner",
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
