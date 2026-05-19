from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent, MissionAssignment, Submission
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_create_submission_records_snapshot_and_rubric(
    migrated_engine: Engine,
) -> None:
    client = submission_client(migrated_engine)
    mission_id, assignment_id = create_assignment(client)

    response = submit_artifact(client, mission_id, assignment_id, "Workflow draft v1")

    assert response.status_code == 201
    payload = response.json()
    assert payload["artifact_text"] == "Workflow draft v1"
    assert payload["assignment_id"] == assignment_id
    assert payload["policy_snapshot_id"] == "snapshot-1"
    assert payload["rubric_id"] == "rubric-1"
    assert payload["review_state"] == "submitted"


def test_revision_preserves_submission_history(migrated_engine: Engine) -> None:
    client = submission_client(migrated_engine)
    mission_id, assignment_id = create_assignment(client)

    first = submit_artifact(client, mission_id, assignment_id, "Workflow draft v1")
    second = submit_artifact(client, mission_id, assignment_id, "Workflow draft v2")

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["version"] == 1
    assert second.json()["version"] == 2
    with Session(migrated_engine) as session:
        stored = session.scalars(
            select(Submission)
            .where(Submission.assignment_id == assignment_id)
            .order_by(Submission.version)
        ).all()
    assert [submission.artifact_text for submission in stored] == [
        "Workflow draft v1",
        "Workflow draft v2",
    ]


def test_submission_create_emits_audit_event(migrated_engine: Engine) -> None:
    client = submission_client(migrated_engine)
    mission_id, assignment_id = create_assignment(client)

    response = submit_artifact(client, mission_id, assignment_id, "Workflow draft v1")

    assert response.status_code == 201
    with Session(migrated_engine) as session:
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "submission.created")
        )
    assert audit_event is not None
    assert audit_event.resource_id == response.json()["id"]


def submission_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def create_assignment(client: TestClient) -> tuple[str, str]:
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
    mission_id = str(mission.json()["id"])
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
        headers=auth_headers("operator-1", "operator"),
    )
    assert cohort.status_code == 201
    launch = client.post(
        f"/cohorts/{cohort.json()['id']}/launch",
        headers=auth_headers("operator-1", "operator"),
    )
    assert launch.status_code == 200
    assignment_id = str(launch.json()[0]["id"])
    with Session(client.app.state.session_factory.kw["bind"]) as session:
        assignment = session.scalar(
            select(MissionAssignment).where(MissionAssignment.id == assignment_id)
        )
    assert assignment is not None
    assert assignment.mission_template_id == mission_id
    return mission_id, assignment_id


def submit_artifact(
    client: TestClient, mission_id: str, assignment_id: str, artifact_text: str
):
    return client.post(
        f"/missions/{mission_id}/submissions",
        json={
            "assignment_id": assignment_id,
            "artifact_text": artifact_text,
            "policy_snapshot_id": "snapshot-1",
            "rubric_id": "rubric-1",
        },
        headers=auth_headers("learner-1", "learner"),
    )


def auth_headers(actor_id: str, role: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-submissions"}
