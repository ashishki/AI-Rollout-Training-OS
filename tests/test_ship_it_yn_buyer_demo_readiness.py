from pathlib import Path

REVIEW = Path("docs/audit/SHIP_IT_YN_BUYER_DEMO_READINESS_REVIEW.md")
AUDIT_INDEX = Path("docs/audit/AUDIT_INDEX.md")


def test_buyer_demo_readiness_cites_required_artifacts() -> None:
    review = REVIEW.read_text()

    for required in [
        "/demo/ship-it-yn",
        "Scenario coverage",
        "Scoring",
        "Browser evidence",
        "Facilitator pack",
        "Safe team summary",
        "Buyer feedback template",
        "Claim boundary review",
        "docs/ship_it_yn_facilitator_pack.md",
        "ai_rollout_os/permissions/game_summary.py",
        "docs/ship_it_yn_buyer_feedback.md",
        "docs/audit/SHIP_IT_YN_CLAIM_BOUNDARY_REVIEW.md",
    ]:
        assert required in review

    audit_index = AUDIT_INDEX.read_text()
    assert "SHIP-IT-YN-BUYER-DEMO-READINESS" in audit_index
    assert "SHOW_BUYER_DEMOS" in audit_index


def test_buyer_demo_readiness_records_claim_safe_decision() -> None:
    review = REVIEW.read_text()

    assert "Decision: SHOW_BUYER_DEMOS" in review
    assert "show buyer demos" in review.lower()
    assert "No PMF claim" in review
    assert "No paid conversion claim" in review

    for forbidden in [
        "PMF achieved",
        "paid conversion proven",
        "production ready",
        "compliance approved",
        "is certified safe",
    ]:
        assert forbidden.lower() not in review.lower()
