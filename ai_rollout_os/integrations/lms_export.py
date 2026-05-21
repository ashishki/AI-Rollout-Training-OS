from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.db.models import Cohort, MissionAssignment, Submission

LMS_EXPORT_VERSION = "lms-completion-export-v1"


class LMSCompletionRow(BaseModel):
    learner_id: str
    assignment_id: str
    mission_template_id: str
    assignment_status: str
    completed: bool
    completion_date: str | None
    evidence_submission_id: str | None
    evidence_submission_version: int | None


class LMSCompletionExport(BaseModel):
    version: str
    workspace_id: str
    cohort_id: str
    row_count: int
    rows: list[LMSCompletionRow]


class LMSCompletionExportService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def export_for_cohort(
        self, *, cohort_id: str, workspace_id: str
    ) -> LMSCompletionExport:
        cohort = self._session.scalar(
            select(Cohort).where(
                Cohort.id == cohort_id,
                Cohort.workspace_id == workspace_id,
            )
        )
        if cohort is None:
            raise ValueError("Cohort not found")

        assignments = self._session.scalars(
            select(MissionAssignment)
            .where(
                MissionAssignment.cohort_id == cohort.id,
                MissionAssignment.workspace_id == workspace_id,
            )
            .order_by(MissionAssignment.learner_id, MissionAssignment.id)
        ).all()
        submissions_by_assignment = self._latest_submissions(
            assignments=assignments,
            workspace_id=workspace_id,
        )
        rows = [
            _completion_row(
                assignment=assignment,
                submission=submissions_by_assignment.get(assignment.id),
            )
            for assignment in assignments
        ]
        return LMSCompletionExport(
            version=LMS_EXPORT_VERSION,
            workspace_id=workspace_id,
            cohort_id=cohort.id,
            row_count=len(rows),
            rows=rows,
        )

    def _latest_submissions(
        self, *, assignments: list[MissionAssignment], workspace_id: str
    ) -> dict[str, Submission]:
        assignment_ids = [assignment.id for assignment in assignments]
        if not assignment_ids:
            return {}
        submissions = self._session.scalars(
            select(Submission)
            .where(
                Submission.assignment_id.in_(assignment_ids),
                Submission.workspace_id == workspace_id,
            )
            .order_by(
                Submission.assignment_id,
                Submission.version.desc(),
                Submission.created_at.desc(),
                Submission.id,
            )
        ).all()
        latest: dict[str, Submission] = {}
        for submission in submissions:
            latest.setdefault(submission.assignment_id, submission)
        return latest


def _completion_row(
    *, assignment: MissionAssignment, submission: Submission | None
) -> LMSCompletionRow:
    completed = assignment.status == "completed"
    return LMSCompletionRow(
        learner_id=assignment.learner_id,
        assignment_id=assignment.id,
        mission_template_id=assignment.mission_template_id,
        assignment_status=assignment.status,
        completed=completed,
        completion_date=(
            submission.created_at.isoformat()
            if completed and submission is not None
            else None
        ),
        evidence_submission_id=submission.id if completed and submission else None,
        evidence_submission_version=(
            submission.version if completed and submission else None
        ),
    )
