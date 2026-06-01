import json
from pathlib import Path

from ai_rollout_os.permissions.game_schema import PermissionGameScenario
from ai_rollout_os.permissions.game_scoring import score_game_decision

GAME_SCENARIO_DIR = Path("ai_rollout_os/permissions/game_scenarios")


def test_game_scoring_returns_decision_result() -> None:
    scenario = load_game_scenario("06-eval-is-red-demo-is-soon.json")

    result = score_game_decision(scenario, "require_eval")

    assert result.scenario_id == "eval-is-red-demo-is-soon"
    assert result.level == 6
    assert result.selected_decision == "require_eval"
    assert result.outcome == "correct"
    assert result.consequence == (
        "The rollout paused until the regression was understood."
    )
    assert result.lesson == "Demo pressure is not a release policy."
    assert result.safer_alternative == (
        "Run the eval, fix the issue, then retry the gate."
    )
    assert result.meter_deltas.eval_confidence == -35
    assert result.score_delta == 15
    assert result.safety_score_delta == 10
    assert result.marks_player_unsafe is False
    assert result.audit_events == (
        "required_eval_before_deploy",
        "decision:require_eval",
        "outcome:correct",
    )


def test_overblock_penalty_preserves_safety_score() -> None:
    scenario = load_game_scenario("07-not-everything-is-deny.json")

    result = score_game_decision(scenario, "deny")

    assert result.outcome == "overblock"
    assert result.score_delta < 0
    assert result.safety_score_delta == 0
    assert result.marks_player_unsafe is False
    assert result.meter_deltas.velocity < 0
    assert result.meter_deltas.blast_radius <= 0
    assert "bounded execution" in result.lesson


def load_game_scenario(filename: str) -> PermissionGameScenario:
    path = GAME_SCENARIO_DIR / filename
    return PermissionGameScenario.model_validate(json.loads(path.read_text()))
