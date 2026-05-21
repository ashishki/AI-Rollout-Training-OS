from pydantic import BaseModel, Field, model_validator


class CustomerROIInputs(BaseModel):
    active_learners: int = Field(ge=0)
    manager_reviews_per_month: int = Field(ge=0)
    approved_workflow_changes_per_month: int = Field(ge=0)
    assumed_minutes_saved_per_review: float = Field(ge=0)
    assumed_minutes_saved_per_workflow_change: float = Field(ge=0)
    fully_loaded_hourly_cost_usd: float = Field(ge=0)
    monthly_subscription_usd: float = Field(ge=0)

    @model_validator(mode="after")
    def require_customer_assumption_source(self) -> "CustomerROIInputs":
        if (
            self.assumed_minutes_saved_per_review == 0
            and self.assumed_minutes_saved_per_workflow_change == 0
        ):
            raise ValueError(
                "At least one customer-provided time assumption is required"
            )
        return self


class LabeledAssumption(BaseModel):
    label: str
    value: float | int
    unit: str
    source: str


class ROIProjection(BaseModel):
    estimate_label: str
    assumptions: dict[str, LabeledAssumption]
    estimated_monthly_minutes_saved: float
    estimated_monthly_value_usd: float
    estimated_net_monthly_value_usd: float
    payback_signal: str
    disclaimer: str


class ROICalculator:
    def calculate(self, inputs: CustomerROIInputs) -> ROIProjection:
        review_minutes = (
            inputs.manager_reviews_per_month * inputs.assumed_minutes_saved_per_review
        )
        workflow_minutes = (
            inputs.approved_workflow_changes_per_month
            * inputs.assumed_minutes_saved_per_workflow_change
        )
        total_minutes = review_minutes + workflow_minutes
        estimated_value = (total_minutes / 60) * inputs.fully_loaded_hourly_cost_usd
        net_value = estimated_value - inputs.monthly_subscription_usd

        return ROIProjection(
            estimate_label="customer_assumption_based_estimate",
            assumptions=_labeled_assumptions(inputs),
            estimated_monthly_minutes_saved=total_minutes,
            estimated_monthly_value_usd=estimated_value,
            estimated_net_monthly_value_usd=net_value,
            payback_signal=_payback_signal(net_value),
            disclaimer=(
                "Estimate only. Use observed pilot metrics and customer-provided "
                "assumptions before making a buying decision."
            ),
        )


def _labeled_assumptions(
    inputs: CustomerROIInputs,
) -> dict[str, LabeledAssumption]:
    return {
        "active_learners": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.active_learners,
            unit="learners",
            source="customer",
        ),
        "manager_reviews_per_month": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.manager_reviews_per_month,
            unit="reviews/month",
            source="customer",
        ),
        "approved_workflow_changes_per_month": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.approved_workflow_changes_per_month,
            unit="workflow_changes/month",
            source="customer",
        ),
        "assumed_minutes_saved_per_review": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.assumed_minutes_saved_per_review,
            unit="minutes/review",
            source="customer",
        ),
        "assumed_minutes_saved_per_workflow_change": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.assumed_minutes_saved_per_workflow_change,
            unit="minutes/workflow_change",
            source="customer",
        ),
        "fully_loaded_hourly_cost_usd": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.fully_loaded_hourly_cost_usd,
            unit="usd/hour",
            source="customer",
        ),
        "monthly_subscription_usd": LabeledAssumption(
            label="customer_provided_assumption",
            value=inputs.monthly_subscription_usd,
            unit="usd/month",
            source="customer",
        ),
    }


def _payback_signal(net_value: float) -> str:
    if net_value > 0:
        return "positive_estimated_net_value"
    if net_value == 0:
        return "break_even_estimated_net_value"
    return "negative_estimated_net_value"
