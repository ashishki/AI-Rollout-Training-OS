from datetime import UTC, datetime

from ai_rollout_os.db.models import Submission
from ai_rollout_os.integrations.lms_export import (
    LMS_EXPORT_VERSION,
    LMSCompletionExportService,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import seed_dashboard_data


def test_lms_export_excludes_artifacts(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        submission = session.scalar(
            select(Submission).where(Submission.id == "submission-1")
        )
        assert submission is not None
        submission.created_at = datetime(2026, 5, 21, 15, 30, tzinfo=UTC)
        session.commit()

        export = LMSCompletionExportService(session).export_for_cohort(
            cohort_id="cohort-1",
            workspace_id="ws-1",
        )

    assert export.version == LMS_EXPORT_VERSION
    assert export.row_count == 2
    rows_by_assignment = {row.assignment_id: row for row in export.rows}
    assert rows_by_assignment["assignment-1"].learner_id == "learner-1"
    assert rows_by_assignment["assignment-1"].assignment_status == "completed"
    assert rows_by_assignment["assignment-1"].completed is True
    assert rows_by_assignment["assignment-1"].completion_date == (
        "2026-05-21T15:30:00+00:00"
    )
    assert rows_by_assignment["assignment-1"].evidence_submission_id == "submission-1"
    assert rows_by_assignment["assignment-1"].evidence_submission_version == 1
    assert rows_by_assignment["assignment-2"].completed is False
    assert rows_by_assignment["assignment-2"].completion_date is None

    serialized = export.model_dump_json()
    assert "Draft workflow artifact." not in serialized
    assert "Sensitive draft workflow artifact." not in serialized
    assert "artifact_text" not in serialized
