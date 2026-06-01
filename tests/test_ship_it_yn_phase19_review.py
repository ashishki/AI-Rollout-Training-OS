from pathlib import Path


def test_phase19_review_records_frontend_readiness_and_limits() -> None:
    review = Path("docs/audit/PHASE19_REACT_VITE_GAME_REVIEW.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "# Phase 19 React/Vite Playable Game Review" in review
    assert "Status: PASS" in review
    assert "T85-T91" in review
    assert "npm run build" in review
    assert "13 Vitest tests" in review
    assert "No real command execution" in review
    assert "P2-UX-001" in review
    assert "T92: FastAPI Static Game Route" in review
    assert "PHASE19-REACT-VITE-GAME" in index
    assert "docs/audit/PHASE19_REACT_VITE_GAME_REVIEW.md" in index
