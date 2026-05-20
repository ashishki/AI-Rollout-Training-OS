import logging
import re

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import Cohort, MissionAssignment, RolePack, SourceDocument
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_operator_launches_cohort(migrated_engine: Engine) -> None:
    client = operator_client(migrated_engine)

    admin_page = client.get("/app/operator/policies", headers=operator_headers())
    assert admin_page.status_code == 200
    assert 'data-form="document"' in admin_page.text
    assert 'data-form="cohort-launch"' in admin_page.text

    policy_body = "Internal support SOP body must stay out of UI responses."
    document = client.post(
        "/app/operator/documents",
        headers=operator_headers(),
        data={
            "title": "Support AI Policy",
            "document_type": "company_policy",
            "body_text": policy_body,
            "effective_date": "2026-05-20",
        },
    )
    assert document.status_code == 201
    assert policy_body not in document.text

    quiz = client.post(
        "/app/operator/guardrail-quizzes",
        headers=operator_headers(),
        data={
            "title": "Support guardrails",
            "pass_threshold": "80",
            "question_id": "safe-data",
            "question_text": "Which data is safe for AI use?",
            "safe_choice_text": "Sanitized ticket context",
            "unsafe_choice_text": "Payment details",
            "correct_answer_id": "safe",
            "explanation": "Only sanitized context is allowed.",
        },
    )
    assert quiz.status_code == 201
    quiz_id = data_attr(quiz.text, "quiz-id")

    role_pack = client.post(
        "/app/operator/role-packs",
        headers=operator_headers(),
        data={"role": "support", "title": "Support pilot role pack"},
    )
    assert role_pack.status_code == 201
    role_pack_id = data_attr(role_pack.text, "role-pack-id")

    mission = client.post(
        "/app/operator/missions",
        headers=operator_headers(),
        data={
            "role_pack_id": role_pack_id,
            "objective": "Draft a safe support reply.",
            "instructions": "Use approved evidence and avoid sensitive data.",
            "artifact_type": "text_response",
            "rubric_id": "rubric-support",
            "guardrail_quiz_id": quiz_id,
        },
    )
    assert mission.status_code == 201

    launch_role_pack = client.post(
        "/app/operator/role-packs/launch",
        headers=operator_headers(),
        data={"role_pack_id": role_pack_id},
    )
    assert launch_role_pack.status_code == 200
    assert "active" in launch_role_pack.text

    cohort = client.post(
        "/app/operator/cohorts",
        headers=operator_headers(),
        data={
            "role_pack_id": role_pack_id,
            "role_pack_version": "1",
            "manager_id": "manager-ui",
            "learner_ids": "learner-ui-1, learner-ui-2",
            "start_date": "2026-05-20",
            "due_date": "2026-06-20",
        },
    )
    assert cohort.status_code == 201
    cohort_id = data_attr(cohort.text, "cohort-id")

    launched = client.post(
        "/app/operator/cohorts/launch",
        headers=operator_headers(),
        data={"cohort_id": cohort_id},
    )
    assert launched.status_code == 200
    assert 'data-assignment-count="2"' in launched.text

    with Session(migrated_engine) as session:
        stored_role_pack = session.get(RolePack, role_pack_id)
        stored_cohort = session.get(Cohort, cohort_id)
        assignments = session.scalars(
            select(MissionAssignment).where(MissionAssignment.cohort_id == cohort_id)
        ).all()
        document_count = len(session.scalars(select(SourceDocument)).all())

    assert stored_role_pack is not None
    assert stored_role_pack.launch_status == "active"
    assert stored_cohort is not None
    assert stored_cohort.status == "active"
    assert len(assignments) == 2
    assert document_count == 1


def test_policy_errors_do_not_leak_body_text(migrated_engine: Engine, caplog) -> None:
    client = operator_client(migrated_engine)
    caplog.set_level(logging.INFO)
    sensitive_body = "Sensitive SOP workflow body must never appear in errors."

    response = client.post(
        "/app/operator/documents",
        headers=operator_headers(),
        data={
            "title": "Support SOP",
            "document_type": "unsupported_type",
            "body_text": sensitive_body,
            "effective_date": "2026-05-20",
        },
    )

    assert response.status_code == 422
    assert "Unsupported document type" in response.text
    assert sensitive_body not in response.text
    assert sensitive_body not in caplog.text


def operator_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def operator_headers() -> dict[str, str]:
    token = create_token(
        actor_id="operator-ui",
        role="operator",
        workspace_id="ws-ui",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-operator-ui"}


def data_attr(html: str, name: str) -> str:
    match = re.search(rf'data-{name}="([^"]+)"', html)
    assert match is not None
    return match.group(1)
