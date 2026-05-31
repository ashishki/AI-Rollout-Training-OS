from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from ai_rollout_os.permissions import (
    build_permission_decision_receipt,
    load_scenarios,
    score_decision,
)

SCENARIO_FIXTURE = Path("tests/fixtures/permission_scenarios.json")


def test_permission_decision_receipt_records_scenario_score_and_evidence() -> None:
    scenarios = {scenario.id: scenario for scenario in load_scenarios(SCENARIO_FIXTURE)}
    scenario = scenarios["secrets-env-read"]
    score = score_decision(scenario, "deny")

    receipt = build_permission_decision_receipt(
        scenario=scenario,
        score=score,
        generated_at=datetime(2026, 5, 31, tzinfo=UTC),
    )

    assert receipt.type == "permission_decision_receipt"
    assert receipt.schema_version == "entropy_core.product_receipt.v1"
    assert receipt.product_id == "ai-rollout-training-os"
    assert receipt.scenario_id == "secrets-env-read"
    assert receipt.verifier_status == "passed"
    assert receipt.evidence_refs[0].ref_id == "scenario:secrets-env-read"
    assert {ref.ref_type for ref in receipt.evidence_refs} == {
        "scenario",
        "permission_boundary",
        "lesson",
    }
    assert len(receipt.receipt_sha256()) == 64


def test_permission_decision_receipt_marks_unsafe_decision_as_failed() -> None:
    scenarios = {scenario.id: scenario for scenario in load_scenarios(SCENARIO_FIXTURE)}
    scenario = scenarios["ci-workflow-edit"]
    score = score_decision(scenario, "approve")

    receipt = build_permission_decision_receipt(
        scenario=scenario,
        score=score,
        generated_at=datetime(2026, 5, 31, tzinfo=UTC),
    )

    assert score.outcome == "unsafe"
    assert receipt.verifier_status == "failed"


def test_permission_decision_receipt_rejects_mismatched_score() -> None:
    scenarios = {scenario.id: scenario for scenario in load_scenarios(SCENARIO_FIXTURE)}
    scenario = scenarios["secrets-env-read"]
    other_score = score_decision(scenarios["ci-workflow-edit"], "approve")

    with pytest.raises(ValueError, match="scenario_id"):
        build_permission_decision_receipt(scenario=scenario, score=other_score)
