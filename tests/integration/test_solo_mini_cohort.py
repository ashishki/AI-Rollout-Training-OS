from pathlib import Path

from ai_rollout_os.db.models import (
    FeedbackResult,
    MissionAssignment,
    ProgressReport,
    Submission,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.fixtures.pilot_data import seed_solo_mini_cohort


def test_solo_mini_cohort_fixture_creates_demo_flow(
    migrated_engine: Engine,
) -> None:
    with Session(migrated_engine) as session:
        mini = seed_solo_mini_cohort(session)
        session.commit()

    with Session(migrated_engine) as session:
        assignments = session.scalars(
            select(MissionAssignment).where(
                MissionAssignment.cohort_id == mini.cohort_id
            )
        ).all()
        submissions = session.scalars(
            select(Submission).where(Submission.workspace_id == mini.workspace_id)
        ).all()
        feedback_results = session.scalars(
            select(FeedbackResult).where(
                FeedbackResult.workspace_id == mini.workspace_id
            )
        ).all()
        approved_submission = session.get(Submission, mini.approved_submission_id)
        report = session.get(ProgressReport, mini.report_id)

    assert mini.learner_id == "learner-solo"
    assert mini.reviewer_id == "reviewer-solo"
    assert len(assignments) == 4
    assert len(submissions) == 2
    assert len(feedback_results) == 2
    assert approved_submission is not None
    assert approved_submission.approval_status == "approved"
    assert report is not None
    assert report.json_body["demo_data"] is True
    assert "unsupported_claims" in report.json_body


def test_solo_mini_cohort_report_labels_demo_limits() -> None:
    content = Path("docs/solo_showcase_artifacts/mini_cohort_replay.md").read_text()

    for required in [
        "Status: demo artifact",
        "public-demo-corpus-v1",
        "synthetic learner",
        "Source Citations",
        "Limitations",
        "Unsupported Claims",
        "Productivity lift is unsupported",
        "Compliance readiness is unsupported",
        "Enterprise readiness is unsupported",
        "GA readiness is unsupported",
    ]:
        assert required in content
