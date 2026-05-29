from pathlib import Path

from ai_rollout_os.permissions import load_scenarios
from ai_rollout_os.permissions.scenarios import CHOICE_IDS, PERMISSION_BOUNDARIES

SCENARIO_FIXTURE = Path("tests/fixtures/permission_scenarios.json")

REQUIRED_RISK_CATEGORIES = {
    "secrets",
    "command_surfaces",
    "test_output_injection",
    "package_scripts",
    "ci_edits",
    "out_of_scope_refactors",
    "network_calls",
    "deletes",
    "dependency_install",
    "log_exposure",
}


def test_seed_scenarios_cover_required_risk_categories() -> None:
    scenarios = load_scenarios(SCENARIO_FIXTURE)
    categories = {scenario.risk_category for scenario in scenarios}

    assert len(scenarios) >= 10
    assert categories >= REQUIRED_RISK_CATEGORIES


def test_scenarios_have_required_fields() -> None:
    scenarios = load_scenarios(SCENARIO_FIXTURE)

    for scenario in scenarios:
        assert scenario.id
        assert scenario.request
        assert scenario.context
        assert scenario.choices
        assert set(scenario.choices) <= CHOICE_IDS
        assert scenario.correct_decision in scenario.choices
        assert scenario.permission_boundary in PERMISSION_BOUNDARIES
        assert scenario.risk_category
        assert scenario.safer_alternative
        assert scenario.lesson_text
