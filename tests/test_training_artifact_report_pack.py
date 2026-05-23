from pathlib import Path

REPORT_PATH = Path("docs/solo_showcase_artifacts/report.md")


def test_training_artifact_report_pack_has_required_sections() -> None:
    report = REPORT_PATH.read_text()

    for required in [
        "# Lead-Response Operator Training Artifact Report",
        "## Source Register",
        "docs/public_corpus/ai_rollout_source_register.md",
        "## Mission Set",
        "lead-response-acknowledge",
        "lead-response-qualify",
        "lead-response-insufficient-evidence",
        "lead-response-human-handoff",
        "## Example Feedback",
        "## Approval Record",
        "## Metrics",
        "## Limits",
    ]:
        assert required in report


def test_training_artifact_report_pack_blocks_demo_overclaims() -> None:
    report = REPORT_PATH.read_text()

    for required in [
        "demo-only report pack",
        "Public/synthetic demo data does not prove adoption",
        "productivity gains",
        "compliance readiness",
        "enterprise readiness",
        "paid conversion",
        "GA readiness",
        "Adoption is unsupported",
        "Productivity gains are unsupported",
    ]:
        assert required in report

    assert "Raw learner text is intentionally not reproduced" in report


def test_solo_showcase_plan_links_training_artifact_report() -> None:
    plan = Path("docs/solo_showcase_plan.md").read_text()

    assert "docs/solo_showcase_artifacts/report.md" in plan
    assert "No productivity, compliance, enterprise, PMF, or GA claims" in plan
