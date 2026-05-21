import pytest
from ai_rollout_os.reporting.roi_calculator import (
    CustomerROIInputs,
    ROICalculator,
)


def test_roi_calculator_avoids_guarantees() -> None:
    projection = ROICalculator().calculate(
        CustomerROIInputs(
            active_learners=50,
            manager_reviews_per_month=120,
            approved_workflow_changes_per_month=15,
            assumed_minutes_saved_per_review=6,
            assumed_minutes_saved_per_workflow_change=20,
            fully_loaded_hourly_cost_usd=80,
            monthly_subscription_usd=1500,
        )
    )

    serialized = projection.model_dump_json().lower()

    assert "guarantee" not in serialized
    assert "guaranteed" not in serialized
    assert "productivity" not in serialized
    assert projection.estimate_label == "customer_assumption_based_estimate"
    assert projection.estimated_monthly_minutes_saved == 1020
    assert projection.estimated_monthly_value_usd == 1360
    assert projection.estimated_net_monthly_value_usd == -140
    assert projection.payback_signal == "negative_estimated_net_value"
    assert all(
        assumption.label == "customer_provided_assumption"
        for assumption in projection.assumptions.values()
    )
    assert all(
        assumption.source == "customer"
        for assumption in projection.assumptions.values()
    )


def test_roi_calculator_requires_time_assumption() -> None:
    with pytest.raises(ValueError, match="customer-provided time assumption"):
        CustomerROIInputs(
            active_learners=10,
            manager_reviews_per_month=20,
            approved_workflow_changes_per_month=2,
            assumed_minutes_saved_per_review=0,
            assumed_minutes_saved_per_workflow_change=0,
            fully_loaded_hourly_cost_usd=75,
            monthly_subscription_usd=500,
        )
