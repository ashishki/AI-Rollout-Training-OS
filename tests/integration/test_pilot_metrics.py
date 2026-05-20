from datetime import UTC, datetime
from pathlib import Path

from ai_rollout_os.db.models import FeedbackResult, Submission
from ai_rollout_os.reporting.pilot_metrics import PilotMetricsService
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import seed_dashboard_data


def test_pilot_metrics_are_database_derived(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        approved_submission = session.scalar(
            select(Submission).where(Submission.id == "submission-1")
        )
        risky_submission = session.scalar(
            select(Submission).where(Submission.id == "submission-2")
        )
        assert approved_submission is not None
        assert risky_submission is not None
        approved_submission.created_at = datetime(2026, 5, 21, 12, tzinfo=UTC)
        approved_submission.approved_at = datetime(2026, 5, 22, 18, tzinfo=UTC)
        approved_submission.approved_workflow_change = (
            "Reuse sanitized support reply workflow."
        )
        risky_submission.created_at = datetime(2026, 5, 22, 9, tzinfo=UTC)
        session.add(
            FeedbackResult(
                id="feedback-result-risk",
                workspace_id="ws-1",
                submission_id="submission-2",
                submission_version=1,
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=["sensitive_data_detected"],
            )
        )
        session.commit()

        metrics = PilotMetricsService(session).outcome_metrics(
            cohort_id="cohort-1",
            workspace_id="ws-1",
        )

    assert metrics.metric_source == "database"
    assert metrics.activation_rate == 0.5
    assert metrics.completion_rate == 0.5
    assert metrics.approved_workflow_change_count == 1
    assert metrics.average_manager_review_time_hours == 30
    assert metrics.risk_rate == 0.5
    assert metrics.time_to_first_safe_use_hours == 36
    assert metrics.enrolled_learner_count == 2
    assert metrics.activated_learner_count == 1
    assert metrics.assignment_count == 2
    assert metrics.completed_assignment_count == 1
    assert metrics.submission_count == 2
    assert metrics.risk_submission_count == 1
    assert metrics.manager_reviewed_submission_count == 1

    source = Path("ai_rollout_os/reporting/pilot_metrics.py").read_text()
    assert "AI_PROVIDER_API_KEY" not in source
    assert "openai" not in source.lower()
