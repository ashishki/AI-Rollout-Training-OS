from ai_rollout_os.db.models import (
    AuditEvent,
    FeedbackResult,
    ProgressReport,
    Submission,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import (
    auth_headers,
    dashboard_client,
    seed_dashboard_data,
)


def test_create_report_version_with_required_metadata(
    migrated_engine: Engine,
) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        session.commit()

    response = client.post(
        "/manager/cohorts/cohort-1/reports",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["cohort_id"] == "cohort-1"
    assert payload["version"] == 1
    assert payload["role_pack_version"] == 1
    assert payload["policy_snapshot_id"] == "snapshot-1"
    assert payload["dashboard_metrics"]["completion_rate"] == 0.5

    with Session(migrated_engine) as session:
        report = session.scalar(select(ProgressReport))
    assert report is not None
    assert report.version == 1
    assert report.dashboard_metrics["submission_rate"] == 1.0


def test_markdown_report_excludes_submission_body_text(
    migrated_engine: Engine,
) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        submission = session.scalar(
            select(Submission).where(Submission.id == "submission-1")
        )
        assert submission is not None
        submission.approved_workflow_change = "Reusable customer-safe reply workflow."
        session.add(
            FeedbackResult(
                id="feedback-result-1",
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

    response = client.post(
        "/manager/cohorts/cohort-1/reports",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 201
    markdown = response.json()["markdown_body"]
    assert "Reusable customer-safe reply workflow." in markdown
    assert "privacy" in markdown
    assert "Draft workflow artifact." not in markdown
    assert "Sensitive draft workflow artifact." not in markdown


def test_report_generation_emits_audit_event(migrated_engine: Engine) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        session.commit()

    response = client.post(
        "/manager/cohorts/cohort-1/reports",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 201
    with Session(migrated_engine) as session:
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "report.created")
        )
    assert audit_event is not None
    assert audit_event.resource_id == response.json()["id"]
