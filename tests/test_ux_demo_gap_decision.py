from pathlib import Path


def test_ux_demo_gap_decision_records_demo_proof_choice() -> None:
    plan = Path("docs/solo_showcase_plan.md").read_text()

    assert "## UX Demo Gap Decision" in plan
    assert "defer browser automation and screenshots" in plan
    assert "Markdown/API artifacts are sufficient" in plan
    assert "not a public GA UX proof" in plan
    assert "D-011" in plan


def test_ux_demo_gap_decision_keeps_p2_ux_finding_open() -> None:
    plan = Path("docs/solo_showcase_plan.md").read_text()
    decision_log = Path("docs/DECISION_LOG.md").read_text()

    assert "P2-UX-001 remains open" in plan
    assert "P2-UX-001 remains open" in decision_log
    assert "Defer browser automation and screenshots" in decision_log
    assert "docs/solo_showcase_plan.md#ux-demo-gap-decision" in decision_log
