from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.db.models import (
    Cohort,
    CohortEnrollment,
    FeedbackJob,
    MissionAssignment,
    MissionTemplate,
    QuizResult,
    Submission,
)
from ai_rollout_os.jobs.models import FeedbackJobStatus


class DashboardMetrics(BaseModel):
    cohort_id: str
    completion_rate: float
    submission_rate: float
    guardrail_pass_rate: float
    approved_workflow_count: int
    feedback_backlog: int
    sensitive_data_flag_rate: float
    assignment_count: int
    completed_assignment_count: int
    submitted_assignment_count: int
    enrolled_learner_count: int
    guardrail_result_count: int
    guardrail_pass_count: int
    submission_count: int
    sensitive_data_flag_count: int


class DashboardService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def cohort_dashboard(
        self, *, cohort_id: str, workspace_id: str
    ) -> DashboardMetrics:
        cohort = self._session.scalar(
            select(Cohort).where(
                Cohort.id == cohort_id,
                Cohort.workspace_id == workspace_id,
            )
        )
        if cohort is None:
            raise ValueError("Cohort not found")

        assignments = self._session.scalars(
            select(MissionAssignment).where(
                MissionAssignment.cohort_id == cohort.id,
                MissionAssignment.workspace_id == workspace_id,
            )
        ).all()
        assignment_ids = [assignment.id for assignment in assignments]
        submissions = (
            self._session.scalars(
                select(Submission).where(
                    Submission.assignment_id.in_(assignment_ids),
                    Submission.workspace_id == workspace_id,
                )
            ).all()
            if assignment_ids
            else []
        )
        enrollments = self._session.scalars(
            select(CohortEnrollment).where(
                CohortEnrollment.cohort_id == cohort.id,
                CohortEnrollment.workspace_id == workspace_id,
            )
        ).all()
        guardrail_results = self._guardrail_results(assignments, workspace_id)
        feedback_backlog = self._feedback_backlog(submissions, workspace_id)

        assignment_count = len(assignments)
        completed_assignment_count = sum(
            1 for assignment in assignments if assignment.status == "completed"
        )
        submitted_assignment_count = len(
            {submission.assignment_id for submission in submissions}
        )
        submission_count = len(submissions)
        sensitive_data_flag_count = sum(
            1 for submission in submissions if submission.redaction_status == "flagged"
        )
        guardrail_result_count = len(guardrail_results)
        guardrail_pass_count = sum(1 for result in guardrail_results if result.passed)

        return DashboardMetrics(
            cohort_id=cohort.id,
            completion_rate=_rate(completed_assignment_count, assignment_count),
            submission_rate=_rate(submitted_assignment_count, assignment_count),
            guardrail_pass_rate=_rate(guardrail_pass_count, guardrail_result_count),
            approved_workflow_count=sum(
                1
                for submission in submissions
                if submission.approval_status == "approved"
            ),
            feedback_backlog=feedback_backlog,
            sensitive_data_flag_rate=_rate(sensitive_data_flag_count, submission_count),
            assignment_count=assignment_count,
            completed_assignment_count=completed_assignment_count,
            submitted_assignment_count=submitted_assignment_count,
            enrolled_learner_count=len(enrollments),
            guardrail_result_count=guardrail_result_count,
            guardrail_pass_count=guardrail_pass_count,
            submission_count=submission_count,
            sensitive_data_flag_count=sensitive_data_flag_count,
        )

    def _guardrail_results(
        self, assignments: list[MissionAssignment], workspace_id: str
    ) -> list[QuizResult]:
        if not assignments:
            return []
        mission_ids = {assignment.mission_template_id for assignment in assignments}
        learner_ids = {assignment.learner_id for assignment in assignments}
        missions = self._session.scalars(
            select(MissionTemplate).where(
                MissionTemplate.id.in_(mission_ids),
                MissionTemplate.workspace_id == workspace_id,
            )
        ).all()
        quiz_ids = {mission.guardrail_quiz_id for mission in missions}
        if not quiz_ids:
            return []
        return self._session.scalars(
            select(QuizResult).where(
                QuizResult.quiz_id.in_(quiz_ids),
                QuizResult.learner_id.in_(learner_ids),
                QuizResult.workspace_id == workspace_id,
            )
        ).all()

    def _feedback_backlog(
        self, submissions: list[Submission], workspace_id: str
    ) -> int:
        if not submissions:
            return 0
        submission_ids = [submission.id for submission in submissions]
        backlog_statuses = {
            FeedbackJobStatus.QUEUED,
            FeedbackJobStatus.RUNNING,
            FeedbackJobStatus.RETRYABLE_FAILED,
        }
        return len(
            self._session.scalars(
                select(FeedbackJob).where(
                    FeedbackJob.submission_id.in_(submission_ids),
                    FeedbackJob.workspace_id == workspace_id,
                    FeedbackJob.status.in_(backlog_statuses),
                )
            ).all()
        )


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator
