import json
from copy import deepcopy
from pathlib import Path

import pytest
from ai_rollout_os.permissions.game_schema import PermissionGameScenario
from pydantic import ValidationError

GAME_SCENARIO_DIR = Path("ai_rollout_os/permissions/game_scenarios")
EXPECTED_STARTER_LEVELS = {
    1: "Tiny Cleanup",
    2: "One-Line Diff",
    3: "Flaky Tests Must Go",
    4: "The Helpful Issue",
    5: "One Permission To Rule Them All",
    6: "Eval Is Red, Demo Is Soon",
    7: "Not Everything Is Deny",
}


def test_game_scenario_schema_validates_required_fields() -> None:
    scenario = PermissionGameScenario.model_validate(valid_game_scenario_record())

    assert scenario.id == "eval-bypass-before-demo"
    assert scenario.level == 6
    assert scenario.title == "Eval Is Red, Demo Is Soon"
    assert scenario.agent_message
    assert scenario.tool_call.permission_request == "write"
    assert scenario.context[0].trusted is True
    assert scenario.inspect_artifacts[0].reveals_risk == "eval_bypass"
    assert scenario.choices == [
        "approve",
        "deny",
        "inspect_diff",
        "require_eval",
        "run_in_sandbox",
        "restrict_scope",
        "escalate_reviewer",
    ]
    assert scenario.best_choices == ["require_eval"]
    assert scenario.feedback["approve"].outcome == "unsafe"
    assert scenario.meters.eval_confidence == -35
    assert scenario.badges == ["eval_gate_preserved"]
    assert scenario.facilitator_notes


@pytest.mark.parametrize(
    ("mutation", "error_match"),
    [
        (
            lambda record: record["choices"].append("approve"),
            "choices must be unique",
        ),
        (
            lambda record: record["choices"].append("ship_without_review"),
            "choices.7",
        ),
        (
            lambda record: record.update({"risk_category": "unsupported_claim"}),
            "risk_category",
        ),
        (
            lambda record: record["feedback"].pop("approve"),
            "feedback missing choices",
        ),
        (
            lambda record: record.update({"level": 8}),
            "level",
        ),
    ],
)
def test_game_scenario_schema_rejects_invalid_records(mutation, error_match) -> None:
    record = valid_game_scenario_record()
    mutation(record)

    with pytest.raises(ValidationError, match=error_match):
        PermissionGameScenario.model_validate(record)


def test_seven_ship_it_yn_scenarios_exist() -> None:
    scenarios = load_game_scenarios()

    assert len(scenarios) == 7
    assert {scenario.level: scenario.title for scenario in scenarios} == (
        EXPECTED_STARTER_LEVELS
    )
    assert [scenario.level for scenario in scenarios] == list(range(1, 8))
    assert {scenario.id for scenario in scenarios} == {
        "tiny-cleanup",
        "one-line-diff",
        "flaky-tests-must-go",
        "the-helpful-issue",
        "one-permission-to-rule-them-all",
        "eval-is-red-demo-is-soon",
        "not-everything-is-deny",
    }


def test_game_scenarios_have_feedback_for_every_choice() -> None:
    scenarios = load_game_scenarios()

    for scenario in scenarios:
        choices = set(scenario.choices)
        assert choices == set(scenario.feedback)
        assert scenario.best_choices
        assert scenario.unsafe_choices
        assert scenario.facilitator_notes
        assert scenario.audit_events
        assert scenario.badges

        for choice in scenario.best_choices:
            assert scenario.feedback[choice].outcome == "correct"
        for choice in scenario.acceptable_choices:
            assert scenario.feedback[choice].outcome == "partial"
        for choice in scenario.unsafe_choices:
            assert scenario.feedback[choice].outcome == "unsafe"
        for choice in scenario.overblock_choices:
            assert scenario.feedback[choice].outcome == "overblock"

        for choice, feedback in scenario.feedback.items():
            assert choice in choices
            assert feedback.consequence
            assert feedback.lesson
            assert feedback.safer_alternative


def load_game_scenarios() -> list[PermissionGameScenario]:
    return [
        PermissionGameScenario.model_validate(json.loads(path.read_text()))
        for path in sorted(GAME_SCENARIO_DIR.glob("*.json"))
    ]


def valid_game_scenario_record() -> dict:
    return deepcopy(
        {
            "id": "eval-bypass-before-demo",
            "level": 6,
            "title": "Eval Is Red, Demo Is Soon",
            "agent_name": "PatchPilot",
            "agent_message": "Eval looks non-critical. I can bypass it for the demo.",
            "tool_call": {
                "type": "config_change",
                "surface": "ci_eval",
                "scope": "deployment_gate",
                "permission_request": "write",
            },
            "context": [
                {
                    "type": "terminal_log",
                    "label": "eval output",
                    "content": "Regression detected in checkout flow.",
                    "trusted": True,
                }
            ],
            "inspect_artifacts": [
                {
                    "id": "diff-eval-bypass",
                    "label": "CI diff",
                    "kind": "diff",
                    "content": "- run: npm test\n+ run: npm test -- --skip-risky-suite",
                    "reveals_risk": "eval_bypass",
                }
            ],
            "choices": [
                "approve",
                "deny",
                "inspect_diff",
                "require_eval",
                "run_in_sandbox",
                "restrict_scope",
                "escalate_reviewer",
            ],
            "best_choices": ["require_eval"],
            "acceptable_choices": ["escalate_reviewer"],
            "unsafe_choices": ["approve"],
            "overblock_choices": ["deny"],
            "permission_boundary": "blocked",
            "risk_category": "eval_bypass",
            "meters": {
                "velocity": -8,
                "blast_radius": 45,
                "trust": -20,
                "eval_confidence": -35,
                "audit_trail": -15,
            },
            "feedback": {
                "approve": {
                    "outcome": "unsafe",
                    "consequence": "The demo shipped with a hidden regression.",
                    "lesson": "Eval gates protect rollout quality under pressure.",
                    "safer_alternative": (
                        "Fix the regression or ship a scoped canary with rollback."
                    ),
                },
                "deny": {
                    "outcome": "overblock",
                    "consequence": "The team learned to preserve safety slowly.",
                    "lesson": "Deny is safe, but it can hide a repair path.",
                    "safer_alternative": "Require the eval and inspect the failure.",
                },
                "inspect_diff": {
                    "outcome": "partial",
                    "consequence": "The risky diff became visible before approval.",
                    "lesson": "Inspection helps, but the gate still has to run.",
                    "safer_alternative": "Inspect the diff, then require the eval.",
                },
                "require_eval": {
                    "outcome": "correct",
                    "consequence": (
                        "The rollout paused until the regression was understood."
                    ),
                    "lesson": "Demo pressure is not a release policy.",
                    "safer_alternative": "Run the eval, fix the issue, then retry.",
                },
                "run_in_sandbox": {
                    "outcome": "partial",
                    "consequence": "The bypass was tested away from production.",
                    "lesson": "Sandboxing is useful but cannot replace eval gates.",
                    "safer_alternative": "Run in sandbox and keep the eval required.",
                },
                "restrict_scope": {
                    "outcome": "partial",
                    "consequence": (
                        "The release scope narrowed but the gate stayed red."
                    ),
                    "lesson": "Scope control helps only when quality gates remain.",
                    "safer_alternative": "Restrict the rollout and require the eval.",
                },
                "escalate_reviewer": {
                    "outcome": "partial",
                    "consequence": "A reviewer caught the demo-pressure shortcut.",
                    "lesson": "Escalation is safer than solo approval under pressure.",
                    "safer_alternative": "Ask a reviewer and preserve the eval gate.",
                },
            },
            "badges": ["eval_gate_preserved"],
            "audit_events": ["required_eval_before_deploy"],
            "facilitator_notes": [
                "Ask players whether they have approved a skipped eval under pressure."
            ],
        }
    )
