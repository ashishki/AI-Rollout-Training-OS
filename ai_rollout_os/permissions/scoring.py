from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from ai_rollout_os.permissions.scenarios import CHOICE_IDS, PermissionScenario

ScoreOutcome = Literal["correct", "partial", "unsafe"]

SAFE_FALLBACK_CHOICES = {
    "ask_for_clarification",
    "run_in_sandbox",
    "escalate_to_reviewer",
}


@dataclass(frozen=True)
class DecisionScore:
    scenario_id: str
    selected_decision: str
    correct_decision: str
    outcome: ScoreOutcome
    risk_category: str
    permission_boundary: str
    feedback: str
    safer_alternative: str


def score_decision(
    scenario: PermissionScenario, selected_decision: str
) -> DecisionScore:
    if selected_decision not in CHOICE_IDS:
        raise ValueError(f"unknown permission decision: {selected_decision}")

    outcome = _classify_decision(scenario, selected_decision)
    feedback = _feedback_for_outcome(scenario, selected_decision, outcome)

    return DecisionScore(
        scenario_id=scenario.id,
        selected_decision=selected_decision,
        correct_decision=scenario.correct_decision,
        outcome=outcome,
        risk_category=scenario.risk_category,
        permission_boundary=scenario.permission_boundary,
        feedback=feedback,
        safer_alternative=scenario.safer_alternative,
    )


def permission_fatigue_warning(
    scenarios: Sequence[PermissionScenario],
    selected_decisions: Sequence[str],
    *,
    unsafe_approval_threshold: int = 2,
) -> str | None:
    unsafe_approvals = [
        scenario.risk_category
        for scenario, decision in zip(scenarios, selected_decisions, strict=True)
        if decision == "approve" and scenario.permission_boundary != "allowed"
    ]
    if len(unsafe_approvals) < unsafe_approval_threshold:
        return None

    categories = ", ".join(sorted(set(unsafe_approvals)))
    return (
        "Permission fatigue warning: repeated risky approvals detected for "
        f"{categories}. Slow down and choose clarification, sandbox, or reviewer "
        "escalation when the boundary is not clearly allowed."
    )


def _classify_decision(
    scenario: PermissionScenario, selected_decision: str
) -> ScoreOutcome:
    if selected_decision == scenario.correct_decision:
        return "correct"
    if selected_decision == "approve" and scenario.permission_boundary != "allowed":
        return "unsafe"
    if (
        scenario.permission_boundary == "allowed"
        and selected_decision not in SAFE_FALLBACK_CHOICES
    ):
        return "unsafe"
    return "partial"


def _feedback_for_outcome(
    scenario: PermissionScenario, selected_decision: str, outcome: ScoreOutcome
) -> str:
    if outcome == "correct":
        prefix = "Correct decision."
    elif outcome == "partial":
        prefix = (
            "Partially safe decision, but not the best permission judgment for "
            f"{scenario.risk_category}."
        )
    else:
        prefix = (
            "Unsafe decision: approving or forcing this action crosses the "
            f"{scenario.risk_category} boundary."
        )

    return (
        f"{prefix} Selected {selected_decision}; expected "
        f"{scenario.correct_decision}. {scenario.lesson_text}"
    )
