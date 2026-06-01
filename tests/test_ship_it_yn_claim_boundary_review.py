from pathlib import Path

REVIEW = Path("docs/audit/SHIP_IT_YN_CLAIM_BOUNDARY_REVIEW.md")
AUDIT_INDEX = Path("docs/audit/AUDIT_INDEX.md")


def test_claim_boundary_review_blocks_unsupported_claims() -> None:
    review = REVIEW.read_text()

    for blocked_claim in [
        "compliance approval",
        "certified safety",
        "production readiness",
        "incident reduction",
        "PMF",
        "paid conversion",
    ]:
        assert blocked_claim in review

    for required in [
        "Status: CLAIM_BOUNDARY_PASS",
        "Blocked Claims",
        "must not be claimed unless new evidence exists",
        "No compliance approval",
        "No PMF or paid-conversion claim",
    ]:
        assert required in review

    audit_index = AUDIT_INDEX.read_text()
    assert "SHIP-IT-YN-CLAIM-BOUNDARY" in audit_index
    assert "CLAIM_BOUNDARY_PASS" in audit_index


def test_claim_boundary_review_confirms_public_demo_safety() -> None:
    review = REVIEW.read_text()

    for required in [
        "/demo/ship-it-yn",
        "No real agent actions",
        "No real command execution",
        "No sensitive data collection",
        "localStorage",
        "ship-it-yn-analytics-v1",
        "no tracking network calls",
        "docs/ship_it_yn_buyer_feedback.md",
        "docs/ship_it_yn_scenario_authoring.md",
    ]:
        assert required in review
