from datetime import UTC, datetime, time

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.db.models import (
    Cohort,
    CohortEnrollment,
    FeedbackResult,
    MissionAssignment,
    MissionTemplate,
    QuizResult,
    Submission,
)


class PilotOutcomeMetrics(BaseModel):
    cohort_id: str
    metric_source: str
    activation_rate: float
    completion_rate: float
    approved_workflow_change_count: int
    average_manager_review_time_hours: float | None
    risk_rate: float
    time_to_first_safe_use_hours: float | None
    enrolled_learner_count: int
    activated_learner_count: int
    assignment_count: int
    completed_assignment_count: int
    submission_count: int
    risk_submission_count: int
    manager_reviewed_submission_count: int


class PilotMetricsService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def outcome_metrics(
        self, *, cohort_id: str, workspace_id: str
    ) -> PilotOutcomeMetrics:
        cohort = self._session.scalar(
            select(Cohort).where(
                Cohort.id == cohort_id,
                Cohort.workspace_id == workspace_id,
            )
        )
        if cohort is None:
            raise ValueError("Cohort not found")

        enrollments = self._session.scalars(
            select(CohortEnrollment).where(
                CohortEnrollment.cohort_id == cohort.id,
                CohortEnrollment.workspace_id == workspace_id,
            )
        ).all()
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
        mission_quiz_ids = self._mission_quiz_ids(assignments, workspace_id)
        passed_quiz_pairs = self._passed_quiz_pairs(
            learner_ids={enrollment.learner_id for enrollment in enrollments},
            quiz_ids=set(mission_quiz_ids.values()),
            workspace_id=workspace_id,
        )
        risk_submission_ids = self._risk_submission_ids(submissions, workspace_id)

        activated_learner_ids = {
            learner_id for _quiz_id, learner_id in passed_quiz_pairs
        }
        completed_assignment_count = sum(
            1 for assignment in assignments if assignment.status == "completed"
        )
        approved_submissions = [
            submission
            for submission in submissions
            if submission.approval_status == "approved"
            and submission.approved_workflow_change
        ]
        manager_review_durations = [
            _hours_between(submission.created_at, submission.approved_at)
            for submission in approved_submissions
            if submission.approved_at is not None
        ]

        return PilotOutcomeMetrics(
            cohort_id=cohort.id,
            metric_source="database",
            activation_rate=_rate(len(activated_learner_ids), len(enrollments)),
            completion_rate=_rate(completed_assignment_count, len(assignments)),
            approved_workflow_change_count=len(approved_submissions),
            average_manager_review_time_hours=_average(manager_review_durations),
            risk_rate=_rate(len(risk_submission_ids), len(submissions)),
            time_to_first_safe_use_hours=self._time_to_first_safe_use_hours(
                cohort=cohort,
                assignments=assignments,
                submissions=submissions,
                mission_quiz_ids=mission_quiz_ids,
                passed_quiz_pairs=passed_quiz_pairs,
            ),
            enrolled_learner_count=len(enrollments),
            activated_learner_count=len(activated_learner_ids),
            assignment_count=len(assignments),
            completed_assignment_count=completed_assignment_count,
            submission_count=len(submissions),
            risk_submission_count=len(risk_submission_ids),
            manager_reviewed_submission_count=len(manager_review_durations),
        )

    def _mission_quiz_ids(
        self, assignments: list[MissionAssignment], workspace_id: str
    ) -> dict[str, str]:
        mission_ids = {assignment.mission_template_id for assignment in assignments}
        if not mission_ids:
            return {}
        missions = self._session.scalars(
            select(MissionTemplate).where(
                MissionTemplate.id.in_(mission_ids),
                MissionTemplate.workspace_id == workspace_id,
            )
        ).all()
        return {mission.id: mission.guardrail_quiz_id for mission in missions}

    def _passed_quiz_pairs(
        self, *, learner_ids: set[str], quiz_ids: set[str], workspace_id: str
    ) -> set[tuple[str, str]]:
        if not learner_ids or not quiz_ids:
            return set()
        results = self._session.scalars(
            select(QuizResult).where(
                QuizResult.quiz_id.in_(quiz_ids),
                QuizResult.learner_id.in_(learner_ids),
                QuizResult.workspace_id == workspace_id,
                QuizResult.passed.is_(True),
            )
        ).all()
        return {(result.quiz_id, result.learner_id) for result in results}

    def _risk_submission_ids(
        self, submissions: list[Submission], workspace_id: str
    ) -> set[str]:
        if not submissions:
            return set()
        submission_ids = [submission.id for submission in submissions]
        risk_submission_ids = {
            submission.id
            for submission in submissions
            if submission.redaction_status == "flagged"
        }
        current_versions = {
            (submission.id, submission.version) for submission in submissions
        }
        results = self._session.scalars(
            select(FeedbackResult).where(
                FeedbackResult.submission_id.in_(submission_ids),
                FeedbackResult.workspace_id == workspace_id,
            )
        ).all()
        risk_submission_ids.update(
            result.submission_id
            for result in results
            if result.risk_flags
            and (result.submission_id, result.submission_version) in current_versions
        )
        return risk_submission_ids

    def _time_to_first_safe_use_hours(
        self,
        *,
        cohort: Cohort,
        assignments: list[MissionAssignment],
        submissions: list[Submission],
        mission_quiz_ids: dict[str, str],
        passed_quiz_pairs: set[tuple[str, str]],
    ) -> float | None:
        assignments_by_id = {assignment.id: assignment for assignment in assignments}
        safe_submission_times = []
        for submission in submissions:
            assignment = assignments_by_id.get(submission.assignment_id)
            if assignment is None:
                continue
            quiz_id = mission_quiz_ids.get(assignment.mission_template_id)
            has_passed_guardrail = (quiz_id, submission.learner_id) in passed_quiz_pairs
            if submission.redaction_status == "clear" and has_passed_guardrail:
                safe_submission_times.append(_as_utc(submission.created_at))
        if not safe_submission_times:
            return None
        cohort_start = datetime.combine(cohort.start_date, time.min).replace(tzinfo=UTC)
        return _hours_between(cohort_start, min(safe_submission_times))


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _hours_between(start: datetime, end: datetime) -> float:
    return (_as_utc(end) - _as_utc(start)).total_seconds() / 3600


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
