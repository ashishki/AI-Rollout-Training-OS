from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import MissionTemplate, RolePack
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_create_draft_role_pack(migrated_engine: Engine) -> None:
    client = role_pack_client(migrated_engine)

    response = client.post(
        "/role-packs",
        json={"role": "support", "title": "Support AI rollout"},
        headers=auth_headers(),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["role"] == "support"
    assert payload["title"] == "Support AI rollout"
    assert payload["version"] == 1
    assert payload["launch_status"] == "inactive"

    with Session(migrated_engine) as session:
        stored = session.scalar(select(RolePack).where(RolePack.id == payload["id"]))
    assert stored is not None
    assert stored.workspace_id == "ws-1"


def test_add_mission_to_role_pack(migrated_engine: Engine) -> None:
    client = role_pack_client(migrated_engine)
    role_pack_id = create_role_pack(client)

    response = client.post(
        f"/role-packs/{role_pack_id}/missions",
        json={
            "objective": "Draft a customer-safe support reply.",
            "instructions": "Use the approved workflow and cite the policy.",
            "artifact_type": "text_response",
            "rubric_id": "rubric-1",
            "guardrail_quiz_id": "quiz-1",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["role_pack_id"] == role_pack_id
    assert payload["objective"] == "Draft a customer-safe support reply."
    assert payload["instructions"] == "Use the approved workflow and cite the policy."
    assert payload["artifact_type"] == "text_response"
    assert payload["rubric_id"] == "rubric-1"
    assert payload["guardrail_quiz_id"] == "quiz-1"

    with Session(migrated_engine) as session:
        stored = session.scalar(
            select(MissionTemplate).where(MissionTemplate.id == payload["id"])
        )
    assert stored is not None
    assert stored.active is True


def test_launch_requires_active_mission(migrated_engine: Engine) -> None:
    client = role_pack_client(migrated_engine)
    role_pack_id = create_role_pack(client)

    response = client.post(
        f"/role-packs/{role_pack_id}/launch",
        headers=auth_headers(),
    )

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "role_pack_has_no_missions"


def role_pack_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def create_role_pack(client: TestClient) -> str:
    response = client.post(
        "/role-packs",
        json={"role": "support", "title": "Support AI rollout"},
        headers=auth_headers(),
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def auth_headers() -> dict[str, str]:
    token = create_token(
        actor_id="operator-1",
        role="operator",
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-role-pack"}
