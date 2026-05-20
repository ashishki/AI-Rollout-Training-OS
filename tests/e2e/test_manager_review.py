import logging

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import FeedbackResult, ProgressReport, Submission
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from tests.integration.test_dashboard import seed_dashboard_data


def test_manager_approval_and_report_flow(migrated_engine: Engine) -> None:
    seed_manager_review_data(migrated_engine)
    client = manager_client(migrated_engine)

    queue = client.get(
        "/app/manager/review-queue?learner_id=learner-1&risk_flag=privacy",
        headers=manager_headers(),
    )
    assert queue.status_code == 200
    assert 'data-submission-id="submission-1"' in queue.text
    assert 'data-submission-id="submission-2"' not in queue.text
    assert 'data-form="manager-approval"' in queue.text

    approval_note = "Manager note should stay out of UI result metrics."
    approved_change = "Reusable customer-safe reply workflow."
    approval = client.post(
        "/app/manager/submissions/approve",
        headers=manager_headers(),
        data={
            "submission_id": "submission-1",
            "approval_note": approval_note,
            "approved_workflow_change": approved_change,
        },
    )
    assert approval.status_code == 200
    assert 'data-approval-status="approved"' in approval.text
    assert approved_change in approval.text
    assert approval_note not in approval.text

    dashboard = client.get(
        "/app/manager/dashboard?cohort_id=cohort-1",
        headers=manager_headers(),
    )
    assert dashboard.status_code == 200
    assert 'data-dashboard-cohort-id="cohort-1"' in dashboard.text
    assert 'data-approved-workflow-count="1"' in dashboard.text

    report = client.post(
        "/app/manager/reports",
        headers=manager_headers(),
        data={"cohort_id": "cohort-1"},
    )
    assert report.status_code == 201
    assert "data-report-id=" in report.text

    with Session(migrated_engine) as session:
        stored_submission = session.get(Submission, "submission-1")
        stored_report = session.scalar(select(ProgressReport))

    assert stored_submission is not None
    assert stored_submission.approval_status == "approved"
    assert stored_submission.approval_note == approval_note
    assert stored_report is not None
    assert stored_report.cohort_id == "cohort-1"


def test_manager_notes_not_logged(migrated_engine: Engine, caplog) -> None:
    seed_manager_review_data(migrated_engine)
    client = manager_client(migrated_engine)
    caplog.set_level(logging.INFO)
    sensitive_note = "Sensitive manager note about customer escalation."

    response = client.post(
        "/app/manager/submissions/approve",
        headers=manager_headers(),
        data={
            "submission_id": "submission-1",
            "approval_note": sensitive_note,
            "approved_workflow_change": "Reusable workflow.",
        },
    )
    dashboard = client.get(
        "/app/manager/dashboard?cohort_id=cohort-1",
        headers=manager_headers(),
    )

    assert response.status_code == 200
    assert sensitive_note not in response.text
    assert sensitive_note not in dashboard.text
    assert sensitive_note not in caplog.text


def seed_manager_review_data(engine: Engine) -> None:
    with Session(engine) as session:
        seed_dashboard_data(session)
        session.add(
            FeedbackResult(
                id="feedback-result-manager-ui",
                workspace_id="ws-1",
                submission_id="submission-1",
                submission_version=1,
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=["privacy"],
            )
        )
        session.commit()


def manager_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def manager_headers() -> dict[str, str]:
    token = create_token(
        actor_id="manager-1",
        role="manager",
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-manager-ui"}
