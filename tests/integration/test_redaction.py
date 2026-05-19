import logging

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import AuditEvent, Submission
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_sensitive_submission_blocks_feedback(migrated_engine: Engine) -> None:
    client = redaction_client(migrated_engine)
    mission_id, assignment_id = create_assignment(client)

    response = submit_artifact(
        client,
        mission_id,
        assignment_id,
        "Contact customer@example.com before using CUSTOMER_DATA",
    )

    assert response.status_code == 201
    assert response.json()["redaction_status"] == "flagged"
    assert response.json()["review_state"] == "blocked_for_review"
    assert response.json()["artifact_text"] == "[REDACTED]"
    with Session(migrated_engine) as session:
        stored = session.scalar(
            select(Submission).where(Submission.id == response.json()["id"])
        )
    assert stored is not None
    assert "customer@example.com" in stored.artifact_text


def test_flagged_text_not_exposed_in_observability(
    migrated_engine: Engine, caplog
) -> None:
    client = redaction_client(migrated_engine)
    mission_id, assignment_id = create_assignment(client)
    flagged_text = "Customer marker CUSTOMER_DATA and user person@example.com"

    with caplog.at_level(logging.INFO):
        response = submit_artifact(client, mission_id, assignment_id, flagged_text)

    assert response.status_code == 201
    assert flagged_text not in response.text
    assert "person@example.com" not in response.text
    rendered_logs = "\n".join(record.getMessage() for record in caplog.records)
    assert flagged_text not in rendered_logs
    assert "person@example.com" not in rendered_logs


def test_manager_approval_unblocks_with_audit_event(migrated_engine: Engine) -> None:
    client = redaction_client(migrated_engine)
    mission_id, assignment_id = create_assignment(client)
    flagged = submit_artifact(
        client, mission_id, assignment_id, "Needs review for CUSTOMER_DATA"
    )

    response = client.post(
        f"/submissions/{flagged.json()['id']}/redaction-approval",
        json={"note": "Manager approved synthetic example."},
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 200
    assert response.json()["review_state"] == "approved_for_feedback"
    assert response.json()["redaction_status"] == "approved"
    with Session(migrated_engine) as session:
        audit_event = session.scalar(
            select(AuditEvent).where(
                AuditEvent.action == "submission.redaction_approved"
            )
        )
    assert audit_event is not None
    assert audit_event.resource_id == flagged.json()["id"]
    assert audit_event.details == "Manager approved synthetic example."


def redaction_client(engine: Engine) -> TestClient:
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
    launch = client.post(
        f"/cohorts/{cohort.json()['id']}/launch",
        headers=auth_headers("operator-1", "operator"),
    )
    return mission_id, str(launch.json()[0]["id"])


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
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-redaction"}
