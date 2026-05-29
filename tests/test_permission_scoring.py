from pathlib import Path

from ai_rollout_os.permissions import (
    load_scenarios,
    permission_fatigue_warning,
    score_decision,
)

SCENARIO_FIXTURE = Path("tests/fixtures/permission_scenarios.json")


def test_decision_scoring_returns_expected_outcomes() -> None:
    scenarios = {scenario.id: scenario for scenario in load_scenarios(SCENARIO_FIXTURE)}

    secret_score = score_decision(scenarios["secrets-env-read"], "deny")
    assert secret_score.outcome == "correct"
    assert secret_score.risk_category == "secrets"
    assert "Secret files are blocked input" in secret_score.feedback

    package_score = score_decision(scenarios["package-script-change"], "run_in_sandbox")
    assert package_score.outcome == "partial"
    assert package_score.correct_decision == "escalate_to_reviewer"
    assert "package_scripts" in package_score.feedback

    ci_score = score_decision(scenarios["ci-workflow-edit"], "approve")
    assert ci_score.outcome == "unsafe"
    assert ci_score.permission_boundary == "blocked"
    assert "ci_edits boundary" in ci_score.feedback


def test_permission_fatigue_warning() -> None:
    scenarios = load_scenarios(SCENARIO_FIXTURE)
    risky_approval_scenarios = [
        scenario
        for scenario in scenarios
        if scenario.risk_category in {"secrets", "network_calls"}
    ]

    assert (
        permission_fatigue_warning(risky_approval_scenarios, ["approve", "deny"])
        is None
    )

    warning = permission_fatigue_warning(
        risky_approval_scenarios, ["approve", "approve"]
    )

    assert warning is not None
    assert "Permission fatigue warning" in warning
    assert "network_calls" in warning
    assert "secrets" in warning
