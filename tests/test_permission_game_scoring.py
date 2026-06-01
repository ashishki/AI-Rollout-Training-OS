import json
from pathlib import Path

from ai_rollout_os.permissions.game_schema import PermissionGameScenario
from ai_rollout_os.permissions.game_scoring import (
    score_game_decision,
    summarize_game_session,
)
from ai_rollout_os.permissions.game_session import build_public_game_session_state

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
    assert result.inspected_artifact_ids == ()
    assert result.audit_trail_quality == "blind"
    assert result.marks_player_unsafe is False
    assert result.audit_events == (
        "required_eval_before_deploy",
        "audit_trail_quality:blind",
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


def test_inspection_changes_audit_trail_quality() -> None:
    scenario = load_game_scenario("01-tiny-cleanup.json")

    blind_result = score_game_decision(scenario, "approve")
    inspected_result = score_game_decision(
        scenario,
        "approve",
        inspected_artifact_ids=["artifact-tiny-cleanup-preview"],
    )

    assert blind_result.audit_trail_quality == "blind"
    assert blind_result.inspected_artifact_ids == ()
    assert inspected_result.audit_trail_quality == "inspected"
    assert inspected_result.inspected_artifact_ids == ("artifact-tiny-cleanup-preview",)
    assert "audit_trail_quality:inspected" in inspected_result.audit_events
    assert "inspected:artifact-tiny-cleanup-preview" in inspected_result.audit_events


def test_game_session_accumulates_meters() -> None:
    results = [
        score_game_decision(
            load_game_scenario("01-tiny-cleanup.json"), "restrict_scope"
        ),
        score_game_decision(
            load_game_scenario("06-eval-is-red-demo-is-soon.json"), "require_eval"
        ),
        score_game_decision(
            load_game_scenario("07-not-everything-is-deny.json"), "run_in_sandbox"
        ),
    ]

    summary = summarize_game_session(results)

    assert summary.total_score == 45
    assert summary.safety_score == 30
    assert summary.meter_totals.velocity == 6
    assert summary.meter_totals.blast_radius == 52
    assert summary.meter_totals.trust == -10
    assert summary.meter_totals.eval_confidence == -5
    assert summary.meter_totals.audit_trail == 22
    assert summary.unsafe_approvals == 0
    assert summary.overblocks == 0


def test_badges_and_titles_are_deterministic() -> None:
    safe_results = [
        score_game_decision(
            load_game_scenario("01-tiny-cleanup.json"), "restrict_scope"
        ),
        score_game_decision(
            load_game_scenario("02-one-line-diff.json"), "require_eval"
        ),
        score_game_decision(
            load_game_scenario("06-eval-is-red-demo-is-soon.json"), "require_eval"
        ),
        score_game_decision(
            load_game_scenario("07-not-everything-is-deny.json"), "run_in_sandbox"
        ),
        score_game_decision(
            load_game_scenario("07-not-everything-is-deny.json"), "restrict_scope"
        ),
        score_game_decision(
            load_game_scenario("07-not-everything-is-deny.json"), "require_eval"
        ),
    ]
    unsafe_results = [
        *safe_results,
        score_game_decision(
            load_game_scenario("06-eval-is-red-demo-is-soon.json"), "approve"
        ),
    ]

    safe_summary = summarize_game_session(safe_results)
    unsafe_summary = summarize_game_session(unsafe_results)

    assert safe_summary.badges == (
        "least_privilege_operator",
        "eval_gate_preserved",
        "bounded_execution",
        "clean_approval_trail",
    )
    assert safe_summary.final_title == "Least Privilege Operator"
    assert safe_summary.strongest_habit == "scoped access"
    assert "Least Privilege Operator" in safe_summary.share_text

    assert unsafe_summary.final_title == "Risky Speedrunner"
    assert "clean_approval_trail" not in unsafe_summary.badges
    assert unsafe_summary.unsafe_approvals == 1
    assert unsafe_summary.weakest_risk_area == "eval-is-red-demo-is-soon"


def test_game_session_summary_has_public_safe_fields() -> None:
    results = [
        score_game_decision(
            load_game_scenario("01-tiny-cleanup.json"), "restrict_scope"
        ),
        score_game_decision(
            load_game_scenario("06-eval-is-red-demo-is-soon.json"), "require_eval"
        ),
    ]

    state = build_public_game_session_state(
        session_id="ship-it-demo-session-1",
        scenario_order=["tiny-cleanup", "eval-is-red-demo-is-soon"],
        decision_results=results,
        inspected_artifacts_by_scenario={
            "tiny-cleanup": ["artifact-tiny-cleanup-preview"],
            "eval-is-red-demo-is-soon": ["artifact-eval-bypass"],
        },
        elapsed_seconds=142,
    ).to_public_dict()

    assert state["session_id"] == "ship-it-demo-session-1"
    assert state["scenario_order"] == ["tiny-cleanup", "eval-is-red-demo-is-soon"]
    assert state["elapsed_seconds"] == 142
    assert state["decisions"] == [
        {
            "scenario_id": "tiny-cleanup",
            "selected_decision": "restrict_scope",
            "outcome": "correct",
            "inspected_artifact_ids": ["artifact-tiny-cleanup-preview"],
        },
        {
            "scenario_id": "eval-is-red-demo-is-soon",
            "selected_decision": "require_eval",
            "outcome": "correct",
            "inspected_artifact_ids": ["artifact-eval-bypass"],
        },
    ]
    assert state["meter_totals"]["audit_trail"] == -3
    assert "eval_gate_preserved" in state["badges"]
    assert state["final_report"]["title"]
    assert state["final_report"]["share_text"].startswith("Ship It? Y/N score:")


def test_game_session_summary_excludes_sensitive_fields() -> None:
    result = score_game_decision(
        load_game_scenario("04-the-helpful-issue.json"), "restrict_scope"
    )

    state = build_public_game_session_state(
        session_id="ship-it-demo-session-2",
        scenario_order=["the-helpful-issue"],
        decision_results=[result],
        inspected_artifacts_by_scenario={
            "the-helpful-issue": ["artifact-helpful-issue"]
        },
        elapsed_seconds=39,
    ).to_public_dict()

    serialized = json.dumps(state, sort_keys=True)

    for forbidden in [
        "actor_id",
        "workspace_id",
        "customer",
        "credential",
        "password",
        "raw_prompt",
        "local_file",
        "agent_message",
        "tool_call",
        "content",
        "consequence",
        "lesson",
        "safer_alternative",
    ]:
        assert forbidden not in serialized


def load_game_scenario(filename: str) -> PermissionGameScenario:
    path = GAME_SCENARIO_DIR / filename
    return PermissionGameScenario.model_validate(json.loads(path.read_text()))
