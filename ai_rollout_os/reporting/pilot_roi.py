from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_rollout_os.reporting.pilot_metrics import (
    PilotMetricsService,
    PilotOutcomeMetrics,
)


class PilotROIReport(BaseModel):
    cohort_id: str
    metric_source: str
    metric_denominators: dict[str, int]
    adoption_summary: dict[str, float | None]
    approved_workflow_changes: dict[str, int]
    risk_reduction_signals: dict[str, float | int]
    manual_review_savings: dict[str, float | int | str | None]
    assumptions: list[str]


class PilotROIService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_report(
        self,
        *,
        cohort_id: str,
        workspace_id: str,
        assumed_minutes_saved_per_manager_review: float | None = None,
    ) -> PilotROIReport:
        metrics = PilotMetricsService(self._session).outcome_metrics(
            cohort_id=cohort_id,
            workspace_id=workspace_id,
        )
        return _roi_report(
            metrics,
            assumed_minutes_saved_per_manager_review=(
                assumed_minutes_saved_per_manager_review
            ),
        )


def _roi_report(
    metrics: PilotOutcomeMetrics,
    *,
    assumed_minutes_saved_per_manager_review: float | None,
) -> PilotROIReport:
    assumptions = [
        "Manual review savings require a customer-provided baseline.",
        "Expansion value requires observed buyer and procurement evidence.",
    ]
    estimated_saved_minutes = None
    if assumed_minutes_saved_per_manager_review is not None:
        estimated_saved_minutes = (
            metrics.manager_reviewed_submission_count
            * assumed_minutes_saved_per_manager_review
        )
        assumptions.append(
            "Manual review savings use an explicit per-review time assumption."
        )

    return PilotROIReport(
        cohort_id=metrics.cohort_id,
        metric_source=metrics.metric_source,
        metric_denominators={
            "enrolled_learner_count": metrics.enrolled_learner_count,
            "assignment_count": metrics.assignment_count,
            "submission_count": metrics.submission_count,
            "manager_reviewed_submission_count": (
                metrics.manager_reviewed_submission_count
            ),
        },
        adoption_summary={
            "activation_rate": metrics.activation_rate,
            "completion_rate": metrics.completion_rate,
            "time_to_first_safe_use_hours": metrics.time_to_first_safe_use_hours,
        },
        approved_workflow_changes={
            "count": metrics.approved_workflow_change_count,
        },
        risk_reduction_signals={
            "risk_rate": metrics.risk_rate,
            "risk_submission_count": metrics.risk_submission_count,
        },
        manual_review_savings={
            "label": "assumption",
            "assumed_minutes_saved_per_review": (
                assumed_minutes_saved_per_manager_review
            ),
            "estimated_saved_minutes": estimated_saved_minutes,
            "review_count": metrics.manager_reviewed_submission_count,
        },
        assumptions=assumptions,
    )
