import json
from pathlib import Path

from ai_rollout_os.permissions.game_schema import (
    GameMeterDeltas,
    PermissionGameScenario,
)
from ai_rollout_os.permissions.game_scoring import (
    GameDecisionResult,
    score_game_decision,
)
from ai_rollout_os.permissions.game_summary import build_team_game_summary

GAME_SCENARIO_DIR = Path("ai_rollout_os/permissions/game_scenarios")


def test_team_summary_aggregates_without_personal_ranking() -> None:
    results = [
        score_game_decision(
            load_game_scenario("06-eval-is-red-demo-is-soon.json"), "approve"
        ),
        score_game_decision(
            load_game_scenario("07-not-everything-is-deny.json"), "deny"
        ),
        score_game_decision(
            load_game_scenario("01-tiny-cleanup.json"), "restrict_scope"
        ),
    ]

    summary = build_team_game_summary(
        results,
        scenario_risk_categories={
            "eval-is-red-demo-is-soon": "eval_bypass",
            "not-everything-is-deny": "dependency_install",
            "tiny-cleanup": "destructive_filesystem",
        },
    ).to_public_dict()

    assert summary["total_decisions"] == 3
    assert summary["risk_hotspots"] == [
        {
            "risk_area": "dependency_install",
            "decision_count": 1,
            "unsafe_approvals": 0,
            "overblocks": 1,
        },
        {
            "risk_area": "eval_bypass",
            "decision_count": 1,
            "unsafe_approvals": 1,
            "overblocks": 0,
        },
    ]
    assert summary["common_unsafe_approvals"] == ["eval_bypass"]
    assert summary["common_overblocks"] == ["dependency_install"]
    assert "inspect before broad approval" in summary["recommended_habits"]
    assert (
        "state what evidence would make safe work approvable"
        in summary["recommended_habits"]
    )
    serialized = json.dumps(summary, sort_keys=True)
    for forbidden in ["learner", "player", "ranking", "rank", "name", "email"]:
        assert forbidden not in serialized


def test_team_summary_excludes_sensitive_data() -> None:
    result = GameDecisionResult(
        scenario_id="customer-acme-raw-prompt",
        level=1,
        selected_decision="approve",
        outcome="unsafe",
        consequence="raw prompt from alice@example.com with API_KEY=sk-live-secret",
        lesson="```python\nprint('secret customer code')\n```",
        safer_alternative="Read /Users/alice/private/customer.txt",
        meter_deltas=GameMeterDeltas(
            velocity=1,
            blast_radius=20,
            trust=-10,
            eval_confidence=-10,
            audit_trail=-10,
        ),
        score_delta=-25,
        safety_score_delta=-20,
        inspected_artifact_ids=("secret-file",),
        audit_trail_quality="blind",
        audit_events=("raw_prompt:alice@example.com", "credential:sk-live-secret"),
    )

    summary = build_team_game_summary(
        [result],
        scenario_risk_categories={
            "customer-acme-raw-prompt": (
                "customer alice@example.com API_KEY=sk-live-secret raw_prompt code"
            )
        },
    ).to_public_dict()
    serialized = json.dumps(summary, sort_keys=True)

    assert "redacted_risk" in serialized
    for forbidden in [
        "alice",
        "example.com",
        "api_key",
        "sk-live",
        "raw_prompt",
        "customer",
        "secret",
        "private",
        "code",
        "credential",
        "artifact",
    ]:
        assert forbidden not in serialized.lower()


def load_game_scenario(filename: str) -> PermissionGameScenario:
    import json

    path = GAME_SCENARIO_DIR / filename
    return PermissionGameScenario.model_validate(json.loads(path.read_text()))
