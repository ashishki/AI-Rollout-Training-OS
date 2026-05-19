from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent, MissionAssignment
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_create_draft_cohort(migrated_engine: Engine) -> None:
    client = cohort_client(migrated_engine)
    role_pack_id = create_role_pack_with_mission(client)

    response = client.post(
        "/cohorts",
        json=cohort_payload(role_pack_id, learner_ids=["learner-1"]),
        headers=auth_headers("operator-1", "operator"),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["role_pack_id"] == role_pack_id
    assert payload["role_pack_version"] == 1
    assert payload["manager_id"] == "manager-1"
    assert payload["start_date"] == "2026-05-20"
    assert payload["due_date"] == "2026-06-20"
    assert payload["status"] == "draft"


def test_launch_creates_assignments_for_each_learner(migrated_engine: Engine) -> None:
    client = cohort_client(migrated_engine)
    role_pack_id = create_role_pack_with_mission(client)
    cohort_id = create_cohort(client, role_pack_id, ["learner-1", "learner-2"])

    first_response = client.post(
        f"/cohorts/{cohort_id}/launch",
        headers=auth_headers("operator-1", "operator"),
    )
    second_response = client.post(
        f"/cohorts/{cohort_id}/launch",
        headers=auth_headers("operator-1", "operator"),
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert len(first_response.json()) == 2
    assert {item["learner_id"] for item in first_response.json()} == {
        "learner-1",
        "learner-2",
    }
    with Session(migrated_engine) as session:
        stored_count = len(session.scalars(select(MissionAssignment)).all())
    assert stored_count == 2


def test_unenrolled_learner_cannot_read_assignments(migrated_engine: Engine) -> None:
    client = cohort_client(migrated_engine)
    role_pack_id = create_role_pack_with_mission(client)
    cohort_id = create_cohort(client, role_pack_id, ["learner-1"])

    response = client.get(
        f"/cohorts/{cohort_id}/assignments",
        headers=auth_headers("learner-2", "learner"),
    )

    assert response.status_code == 403
    with Session(migrated_engine) as session:
        audit_event = session.scalar(select(AuditEvent))
    assert audit_event is not None
    assert audit_event.action == "denied_access"
    assert audit_event.resource_type == "cohort"
    assert audit_event.resource_id == cohort_id


def cohort_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def create_role_pack_with_mission(client: TestClient) -> str:
    role_pack = client.post(
        "/role-packs",
        json={"role": "support", "title": "Support AI rollout"},
        headers=auth_headers("operator-1", "operator"),
    )
    assert role_pack.status_code == 201
    role_pack_id = str(role_pack.json()["id"])
    mission = client.post(
        f"/role-packs/{role_pack_id}/missions",
        json={
            "objective": "Draft a customer-safe support reply.",
            "instructions": "Use approved workflow.",
            "artifact_type": "text_response",
            "rubric_id": "rubric-1",
            "guardrail_quiz_id": "quiz-1",
        },
        headers=auth_headers("operator-1", "operator"),
    )
    assert mission.status_code == 200
    return role_pack_id


def create_cohort(client: TestClient, role_pack_id: str, learner_ids: list[str]) -> str:
    response = client.post(
        "/cohorts",
        json=cohort_payload(role_pack_id, learner_ids=learner_ids),
        headers=auth_headers("operator-1", "operator"),
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def cohort_payload(role_pack_id: str, *, learner_ids: list[str]) -> dict:
    return {
        "role_pack_id": role_pack_id,
        "role_pack_version": 1,
        "manager_id": "manager-1",
        "learner_ids": learner_ids,
        "start_date": "2026-05-20",
        "due_date": "2026-06-20",
    }


def auth_headers(actor_id: str, role: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-cohorts"}
