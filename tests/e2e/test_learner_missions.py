import re
from datetime import date

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import (
    Cohort,
    CohortEnrollment,
    GuardrailQuestion,
    GuardrailQuiz,
    MissionAssignment,
    MissionTemplate,
    QuizResult,
    RolePack,
    Submission,
)
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_learner_completes_mission_flow(migrated_engine: Engine) -> None:
    seed_learner_mission(migrated_engine)
    client = learner_client(migrated_engine)

    assignments = client.get(
        "/app/learner/assignments", headers=learner_headers("learner-ui-1")
    )
    assert assignments.status_code == 200
    assert 'data-assignment-id="assignment-ui-1"' in assignments.text
    assert 'data-form="guardrail-submit"' in assignments.text
    assert 'data-form="artifact-submit"' in assignments.text

    quiz = client.post(
        "/app/learner/guardrail-submissions",
        headers=learner_headers("learner-ui-1"),
        data={
            "quiz_id": "quiz-ui",
            "question_id": "safe-data",
            "answer_ids": "safe",
        },
    )
    assert quiz.status_code == 201
    assert 'data-passed="true"' in quiz.text

    submission = client.post(
        "/app/learner/submissions",
        headers=learner_headers("learner-ui-1"),
        data={
            "mission_id": "mission-ui",
            "assignment_id": "assignment-ui-1",
            "artifact_text": "Draft response using sanitized ticket context.",
            "policy_snapshot_id": "snapshot-ui",
            "rubric_id": "rubric-ui",
        },
    )
    assert submission.status_code == 201
    assert 'data-review-state="submitted"' in submission.text
    assert 'data-redaction-status="clear"' in submission.text

    with Session(migrated_engine) as session:
        quiz_result = session.scalar(select(QuizResult))
        stored_submission = session.scalar(select(Submission))

    assert quiz_result is not None
    assert quiz_result.passed is True
    assert stored_submission is not None
    assert stored_submission.redaction_status == "clear"


def test_flagged_submission_is_redacted(migrated_engine: Engine) -> None:
    seed_learner_mission(migrated_engine)
    client = learner_client(migrated_engine)
    sensitive_artifact = "CUSTOMER: Jane jane@example.com needs help."

    response = client.post(
        "/app/learner/submissions",
        headers=learner_headers("learner-ui-1"),
        data={
            "mission_id": "mission-ui",
            "assignment_id": "assignment-ui-1",
            "artifact_text": sensitive_artifact,
            "policy_snapshot_id": "snapshot-ui",
            "rubric_id": "rubric-ui",
        },
    )

    assert response.status_code == 201
    assert "[REDACTED]" in response.text
    assert sensitive_artifact not in response.text
    assert "jane@example.com" not in response.text
    assert 'data-redaction-status="flagged"' in response.text


def seed_learner_mission(engine: Engine) -> None:
    with Session(engine) as session:
        session.add(
            RolePack(
                id="role-pack-ui",
                workspace_id="ws-ui",
                role="support",
                title="Support role pack",
                version=1,
                launch_status="active",
                created_by="operator-ui",
            )
        )
        session.add(
            GuardrailQuiz(
                id="quiz-ui",
                workspace_id="ws-ui",
                title="Support guardrails",
                version=1,
                pass_threshold=80,
            )
        )
        session.flush()
        session.add(
            GuardrailQuestion(
                id="safe-data",
                quiz_id="quiz-ui",
                workspace_id="ws-ui",
                question_text="Which data is safe?",
                answer_choices=[
                    {"id": "safe", "text": "Sanitized ticket context"},
                    {"id": "unsafe", "text": "Payment details"},
                ],
                correct_answer_ids=["safe"],
                explanation="Only sanitized context is allowed.",
            )
        )
        session.add(
            MissionTemplate(
                id="mission-ui",
                role_pack_id="role-pack-ui",
                workspace_id="ws-ui",
                objective="Draft a safe support reply.",
                instructions="Use approved evidence.",
                artifact_type="text_response",
                rubric_id="rubric-ui",
                guardrail_quiz_id="quiz-ui",
                active=True,
            )
        )
        session.add(
            Cohort(
                id="cohort-ui",
                workspace_id="ws-ui",
                role_pack_id="role-pack-ui",
                role_pack_version=1,
                manager_id="manager-ui",
                start_date=date(2026, 5, 20),
                due_date=date(2026, 6, 20),
                status="active",
                created_by="operator-ui",
            )
        )
        session.add(
            CohortEnrollment(
                id="enroll-ui-1",
                cohort_id="cohort-ui",
                workspace_id="ws-ui",
                learner_id="learner-ui-1",
            )
        )
        session.add(
            MissionAssignment(
                id="assignment-ui-1",
                cohort_id="cohort-ui",
                workspace_id="ws-ui",
                learner_id="learner-ui-1",
                mission_template_id="mission-ui",
                role_pack_version=1,
                status="assigned",
            )
        )
        session.commit()


def learner_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def learner_headers(actor_id: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role="learner",
        workspace_id="ws-ui",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-learner-ui"}


def data_attr(html: str, name: str) -> str:
    match = re.search(rf'data-{name}="([^"]+)"', html)
    assert match is not None
    return match.group(1)
