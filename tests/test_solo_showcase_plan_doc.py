from pathlib import Path


def test_solo_showcase_plan_defines_demo_strategy() -> None:
    plan = Path("docs/solo_showcase_plan.md").read_text()

    for required in [
        "# Solo Showcase Plan",
        "## Target Role",
        "lead-response operator",
        "## Demo Scope",
        "## Non-Goals",
        "## Required Artifacts",
        "## Success Criteria",
        "Lead Response SLA Agent",
    ]:
        assert required in plan


def test_solo_showcase_plan_blocks_public_demo_overclaims() -> None:
    plan = Path("docs/solo_showcase_plan.md").read_text()

    for blocked_claim in [
        "enterprise rollout claims",
        "productivity or time-savings guarantees",
        "compliance attestation",
        "GA readiness claims",
        "paid customer, signed expansion, or PMF claims",
        "SaaS-grade multi-tenant security claims",
    ]:
        assert blocked_claim in plan

    assert "Synthetic submissions must be labeled as demo data" in plan
    assert (
        "unsupported adoption, productivity, compliance, enterprise, PMF, paid" in plan
    )
    assert "`insufficient_evidence`" in plan


def test_phase_15_roadmap_points_to_claim_safe_showcase() -> None:
    roadmap = Path("docs/product_maturity_roadmap.md").read_text()
    phase_15 = roadmap.split(
        "## Phase 15 - Solo Showcase And Small-Team Rollout", maxsplit=1
    )[1].split("## Metrics That Matter", maxsplit=1)[0]

    assert "Lead-response operator showcase strategy" in phase_15
    assert "docs/solo_showcase_plan.md" in phase_15
    assert "No productivity, adoption, compliance, enterprise, or GA claim" in phase_15
