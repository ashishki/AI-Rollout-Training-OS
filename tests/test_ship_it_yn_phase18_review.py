from pathlib import Path


def test_phase18_review_records_core_readiness_and_limits() -> None:
    review = Path("docs/audit/PHASE18_SCENARIO_SCORING_CORE_REVIEW.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "# Phase 18 Scenario And Scoring Core Review" in review
    assert "Status: PASS" in review
    assert "T79-T84" in review
    assert "Phase 19" in review
    assert "T85: React/Vite Permission Game Scaffold" in review
    assert "existing permission simulator result loop builds local" in review
    assert "not by duplicating receipt logic" in review
    assert "P2-UX-001" in review
    assert "PHASE18-SCENARIO-SCORING" in index
    assert "docs/audit/PHASE18_SCENARIO_SCORING_CORE_REVIEW.md" in index
