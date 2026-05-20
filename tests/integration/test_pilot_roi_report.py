from datetime import UTC, datetime

from ai_rollout_os.db.models import Submission
from ai_rollout_os.reporting.pilot_roi import PilotROIService
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import seed_dashboard_data


def test_roi_report_avoids_productivity_claims(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        seed_roi_data(session)

        report = PilotROIService(session).create_report(
            cohort_id="cohort-1",
            workspace_id="ws-1",
            assumed_minutes_saved_per_manager_review=12,
        )

    serialized = report.model_dump_json().lower()
    assert "guarantee" not in serialized
    assert report.manual_review_savings["label"] == "assumption"
    assert report.manual_review_savings["estimated_saved_minutes"] == 12
    assert any("assumption" in item for item in report.assumptions)


def test_roi_report_includes_metric_denominators(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        seed_roi_data(session)

        report = PilotROIService(session).create_report(
            cohort_id="cohort-1",
            workspace_id="ws-1",
        )

    assert report.metric_source == "database"
    assert report.metric_denominators == {
        "enrolled_learner_count": 2,
        "assignment_count": 2,
        "submission_count": 2,
        "manager_reviewed_submission_count": 1,
    }
    assert report.adoption_summary["activation_rate"] == 0.5
    assert report.approved_workflow_changes["count"] == 1
    assert report.risk_reduction_signals["risk_submission_count"] == 1


def seed_roi_data(session: Session) -> None:
    seed_dashboard_data(session)
    approved_submission = session.scalar(
        select(Submission).where(Submission.id == "submission-1")
    )
    assert approved_submission is not None
    approved_submission.created_at = datetime(2026, 5, 21, 12, tzinfo=UTC)
    approved_submission.approved_at = datetime(2026, 5, 22, 18, tzinfo=UTC)
    approved_submission.approved_workflow_change = (
        "Reuse sanitized support reply workflow."
    )
    session.commit()
