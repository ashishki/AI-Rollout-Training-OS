from ai_rollout_os.auth.dependencies import authenticate_request
from ai_rollout_os.auth.permissions import require_role, require_workspace_match
from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent, Workspace
from ai_rollout_os.main import create_app
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_authenticated_request_sets_actor_context(migrated_engine: Engine) -> None:
    app = auth_test_app(migrated_engine)
    token = bearer_token(actor_id="learner-1", role="learner", workspace_id="ws-1")

    response = TestClient(app).get(
        "/auth-context",
        headers={"authorization": f"Bearer {token}", "x-trace-id": "trace-auth"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "actor_id": "learner-1",
        "role": "learner",
        "workspace_id": "ws-1",
        "trace_id": "trace-auth",
    }


def test_role_denial_returns_403_and_audits(migrated_engine: Engine) -> None:
    app = auth_test_app(migrated_engine)
    token = bearer_token(actor_id="learner-1", role="learner", workspace_id="ws-1")

    response = TestClient(app).post(
        "/operator-only",
        headers={"authorization": f"Bearer {token}", "x-trace-id": "trace-denied"},
    )

    assert response.status_code == 403
    assert audit_events(migrated_engine) == [
        {
            "actor_id": "learner-1",
            "action": "denied_access",
            "resource_type": "route",
            "resource_id": "/operator-only",
            "result": "denied",
            "trace_id": "trace-denied",
        }
    ]


def test_workspace_mismatch_denied_before_mutation(migrated_engine: Engine) -> None:
    app = auth_test_app(migrated_engine)
    token = bearer_token(actor_id="operator-1", role="operator", workspace_id="ws-1")

    response = TestClient(app).post(
        "/workspaces/ws-2/mutate",
        headers={
            "authorization": f"Bearer {token}",
            "x-trace-id": "trace-workspace-denied",
        },
    )

    assert response.status_code == 403
    with Session(migrated_engine) as session:
        workspace_ids = set(session.scalars(select(Workspace.id)).all())
    assert "ws-2" not in workspace_ids
    assert audit_events(migrated_engine) == [
        {
            "actor_id": "operator-1",
            "action": "denied_access",
            "resource_type": "workspace",
            "resource_id": "ws-2",
            "result": "denied",
            "trace_id": "trace-workspace-denied",
        }
    ]


def auth_test_app(migrated_engine: Engine) -> FastAPI:
    session_factory = sessionmaker(bind=migrated_engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    operator_dependency = require_role("operator")
    workspace_dependency = require_workspace_match()

    @app.get("/auth-context", dependencies=[Depends(authenticate_request)])
    def auth_context(request: Request) -> dict[str, str]:
        return {
            "actor_id": request.state.actor_id,
            "role": request.state.role,
            "workspace_id": request.state.workspace_id,
            "trace_id": request.state.trace_id,
        }

    @app.post("/operator-only", dependencies=[Depends(operator_dependency)])
    def operator_only() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/workspaces/{workspace_id}/mutate",
        dependencies=[Depends(operator_dependency), Depends(workspace_dependency)],
    )
    def mutate_workspace(workspace_id: str) -> dict[str, str]:
        with session_factory() as session:
            session.add(Workspace(id=workspace_id, name="mutated workspace"))
            session.commit()
        return {"status": "mutated"}

    return app


def bearer_token(*, actor_id: str, role: str, workspace_id: str) -> str:
    return create_token(
        actor_id=actor_id,
        role=role,
        workspace_id=workspace_id,
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )


def audit_events(engine: Engine) -> list[dict[str, str | None]]:
    with Session(engine) as session:
        events = session.scalars(select(AuditEvent).order_by(AuditEvent.id)).all()

    return [
        {
            "actor_id": event.actor_id,
            "action": event.action,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "result": event.result,
            "trace_id": event.trace_id,
        }
        for event in events
    ]
