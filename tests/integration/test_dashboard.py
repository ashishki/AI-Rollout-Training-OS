from datetime import date
from pathlib import Path

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import (
    Cohort,
    CohortEnrollment,
    FeedbackJob,
    GuardrailQuiz,
    MissionAssignment,
    MissionTemplate,
    QuizResult,
    RolePack,
    Submission,
)
from ai_rollout_os.jobs.models import FeedbackJobStatus
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_dashboard_returns_required_metrics(migrated_engine: Engine) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        session.commit()

    response = client.get(
        "/manager/cohorts/cohort-1/dashboard",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["completion_rate"] == 0.5
    assert payload["submission_rate"] == 1.0
    assert payload["guardrail_pass_rate"] == 0.5
    assert payload["approved_workflow_count"] == 1
    assert payload["feedback_backlog"] == 1
    assert payload["sensitive_data_flag_rate"] == 0.5
    assert payload["assignment_count"] == 2
    assert payload["submission_count"] == 2


def test_dashboard_does_not_call_llm_provider(migrated_engine: Engine) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        session.commit()

    response = client.get(
        "/manager/cohorts/cohort-1/dashboard",
        headers=auth_headers("manager-1", "manager"),
    )
    dashboard_source = Path("ai_rollout_os/reporting/dashboard.py").read_text()

    assert response.status_code == 200
    assert "AI_PROVIDER_API_KEY" not in dashboard_source
    assert "model_" not in dashboard_source
    assert "openai" not in dashboard_source.lower()
    assert "provider" not in dashboard_source.lower()


def test_empty_cohort_dashboard_has_zero_metrics(migrated_engine: Engine) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        session.add(
            Cohort(
                id="cohort-empty",
                workspace_id="ws-1",
                role_pack_id="role-pack-1",
                role_pack_version=1,
                manager_id="manager-1",
                start_date=date(2026, 5, 20),
                due_date=date(2026, 6, 20),
                status="draft",
                created_by="operator-1",
            )
        )
        session.commit()

    response = client.get(
        "/manager/cohorts/cohort-empty/dashboard",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["completion_rate"] == 0
    assert payload["submission_rate"] == 0
    assert payload["guardrail_pass_rate"] == 0
    assert payload["assignment_count"] == 0
    assert payload["enrolled_learner_count"] == 0
    assert payload["guardrail_result_count"] == 0
    assert payload["submission_count"] == 0


def dashboard_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def seed_dashboard_data(session: Session) -> None:
    session.add(
        RolePack(
            id="role-pack-1",
            workspace_id="ws-1",
            role="support",
            title="Support AI rollout",
            version=1,
            launch_status="active",
            created_by="operator-1",
        )
    )
    session.add(
        GuardrailQuiz(
            id="quiz-1",
            workspace_id="ws-1",
            title="Support guardrails",
            version=1,
            pass_threshold=80,
        )
    )
    session.add(
        MissionTemplate(
            id="mission-1",
            role_pack_id="role-pack-1",
            workspace_id="ws-1",
            objective="Draft safe support reply.",
            instructions="Use approved evidence.",
            artifact_type="text_response",
            rubric_id="rubric-1",
            guardrail_quiz_id="quiz-1",
            active=True,
        )
    )
    session.add(
        Cohort(
            id="cohort-1",
            workspace_id="ws-1",
            role_pack_id="role-pack-1",
            role_pack_version=1,
            manager_id="manager-1",
            start_date=date(2026, 5, 20),
            due_date=date(2026, 6, 20),
            status="active",
            created_by="operator-1",
        )
    )
    session.add_all(
        [
            CohortEnrollment(
                id="enroll-1",
                cohort_id="cohort-1",
                workspace_id="ws-1",
                learner_id="learner-1",
            ),
            CohortEnrollment(
                id="enroll-2",
                cohort_id="cohort-1",
                workspace_id="ws-1",
                learner_id="learner-2",
            ),
            MissionAssignment(
                id="assignment-1",
                cohort_id="cohort-1",
                workspace_id="ws-1",
                learner_id="learner-1",
                mission_template_id="mission-1",
                role_pack_version=1,
                status="completed",
            ),
            MissionAssignment(
                id="assignment-2",
                cohort_id="cohort-1",
                workspace_id="ws-1",
                learner_id="learner-2",
                mission_template_id="mission-1",
                role_pack_version=1,
                status="assigned",
            ),
        ]
    )
    session.add_all(
        [
            QuizResult(
                id="quiz-result-1",
                quiz_id="quiz-1",
                workspace_id="ws-1",
                learner_id="learner-1",
                score=100,
                passed=True,
                missed_question_ids=[],
                answers=[],
            ),
            QuizResult(
                id="quiz-result-2",
                quiz_id="quiz-1",
                workspace_id="ws-1",
                learner_id="learner-2",
                score=50,
                passed=False,
                missed_question_ids=["q1"],
                answers=[],
            ),
        ]
    )
    session.add_all(
        [
            Submission(
                id="submission-1",
                workspace_id="ws-1",
                mission_template_id="mission-1",
                assignment_id="assignment-1",
                learner_id="learner-1",
                artifact_text="Draft workflow artifact.",
                policy_snapshot_id="snapshot-1",
                rubric_id="rubric-1",
                version=1,
                review_state="ready_for_feedback",
                redaction_status="clear",
                approval_status="approved",
            ),
            Submission(
                id="submission-2",
                workspace_id="ws-1",
                mission_template_id="mission-1",
                assignment_id="assignment-2",
                learner_id="learner-2",
                artifact_text="Sensitive draft workflow artifact.",
                policy_snapshot_id="snapshot-1",
                rubric_id="rubric-1",
                version=1,
                review_state="blocked_for_review",
                redaction_status="flagged",
                approval_status="not_reviewed",
            ),
        ]
    )
    session.add(
        FeedbackJob(
            id="feedback-job-1",
            workspace_id="ws-1",
            submission_id="submission-1",
            submission_version=1,
            idempotency_key="submission-1:1",
            status=FeedbackJobStatus.QUEUED,
            attempt_count=0,
        )
    )


def auth_headers(actor_id: str, role: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-dashboard"}
