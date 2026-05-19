from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent, MissionAssignment
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_launched_role_pack_update_creates_new_version(
    migrated_engine: Engine,
) -> None:
    client = version_client(migrated_engine)
    role_pack_id, mission_id, assignment_id = launched_role_pack(client)

    response = client.post(
        f"/role-packs/{role_pack_id}/versions",
        json=version_payload(mission_id),
        headers=auth_headers(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["role_pack"]["version"] == 2
    with Session(migrated_engine) as session:
        assignment = session.scalar(
            select(MissionAssignment).where(MissionAssignment.id == assignment_id)
        )
    assert assignment is not None
    assert assignment.role_pack_version == 1


def test_role_pack_version_diff_lists_changes(migrated_engine: Engine) -> None:
    client = version_client(migrated_engine)
    role_pack_id, mission_id, _assignment_id = launched_role_pack(client)
    update_response = client.post(
        f"/role-packs/{role_pack_id}/versions",
        json=version_payload(mission_id),
        headers=auth_headers(),
    )
    assert update_response.status_code == 200

    response = client.get(
        f"/role-packs/{role_pack_id}/versions/compare",
        headers=auth_headers(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["previous_version"] == 1
    assert payload["new_version"] == 2
    assert payload["changed_missions"] == [mission_id]
    assert payload["changed_rubric_ids"] == ["rubric-2"]
    assert payload["changed_guardrail_quiz_ids"] == ["quiz-2"]
    assert payload["unchanged_missions"] == []


def test_role_pack_version_edit_audited(migrated_engine: Engine) -> None:
    client = version_client(migrated_engine)
    role_pack_id, mission_id, _assignment_id = launched_role_pack(client)

    response = client.post(
        f"/role-packs/{role_pack_id}/versions",
        json=version_payload(mission_id),
        headers=auth_headers(),
    )

    assert response.status_code == 200
    with Session(migrated_engine) as session:
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "role_pack.version_created")
        )
    assert audit_event is not None
    assert '"previous_version":1' in (audit_event.details or "")
    assert '"new_version":2' in (audit_event.details or "")


def version_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def launched_role_pack(client: TestClient) -> tuple[str, str, str]:
    role_pack = client.post(
        "/role-packs",
        json={"role": "support", "title": "Support AI rollout"},
        headers=auth_headers(),
    )
    assert role_pack.status_code == 201
    role_pack_id = role_pack.json()["id"]
    mission = client.post(
        f"/role-packs/{role_pack_id}/missions",
        json={
            "objective": "Draft a safe reply.",
            "instructions": "Use approved evidence.",
            "artifact_type": "text_response",
            "rubric_id": "rubric-1",
            "guardrail_quiz_id": "quiz-1",
        },
        headers=auth_headers(),
    )
    assert mission.status_code == 200
    mission_id = mission.json()["id"]
    launch = client.post(f"/role-packs/{role_pack_id}/launch", headers=auth_headers())
    assert launch.status_code == 200
    cohort = client.post(
        "/cohorts",
        json={
            "role_pack_id": role_pack_id,
            "role_pack_version": 1,
            "manager_id": "manager-1",
            "learner_ids": ["learner-1"],
            "start_date": "2026-05-20",
            "due_date": "2026-06-20",
        },
        headers=auth_headers(),
    )
    assert cohort.status_code == 201
    launched = client.post(
        f"/cohorts/{cohort.json()['id']}/launch",
        headers=auth_headers(),
    )
    assert launched.status_code == 200
    return role_pack_id, mission_id, launched.json()[0]["id"]


def version_payload(mission_id: str) -> dict:
    return {
        "role": "support",
        "title": "Support AI rollout v2",
        "missions": [
            {
                "id": mission_id,
                "objective": "Draft a safer reply.",
                "instructions": "Use approved evidence and cite policy.",
                "artifact_type": "text_response",
                "rubric_id": "rubric-2",
                "guardrail_quiz_id": "quiz-2",
            }
        ],
    }


def auth_headers() -> dict[str, str]:
    token = create_token(
        actor_id="operator-1",
        role="operator",
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-versioning"}
