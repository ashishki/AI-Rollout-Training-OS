from pathlib import Path


def test_ship_it_yn_readiness_review_cites_required_evidence() -> None:
    review = Path("docs/audit/SHIP_IT_YN_UX_READINESS_REVIEW.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    for required in [
        "# Ship It? Y/N UX Readiness Review",
        "Status: SHOW_PUBLIC_DEMO",
        "/demo/ship-it-yn",
        "tests/test_permission_game_scenarios.py",
        "tests/test_permission_game_scoring.py",
        "frontend/permission_game/",
        "tests/browser/test_ship_it_yn_gameplay.py",
        "docs/audit/artifacts/ship_it_yn_desktop.png",
        "docs/audit/artifacts/ship_it_yn_mobile.png",
        "README.md",
        "tests/test_permission_game_marketing.py",
        "No certified safety",
        "compliance approval",
        "production readiness",
        "PMF",
        "paid conversion",
        "T99: Facilitator Debrief Pack",
    ]:
        assert required in review

    assert "SHIP-IT-YN-UX-READINESS" in index
    assert "docs/audit/SHIP_IT_YN_UX_READINESS_REVIEW.md" in index


def test_ship_it_yn_readiness_review_updates_p2_ux_001() -> None:
    review = Path("docs/audit/SHIP_IT_YN_UX_READINESS_REVIEW.md").read_text()
    state = Path("docs/CODEX_PROMPT.md").read_text()

    assert "P2-UX-001" in review
    assert "Resolved for Ship It? Y/N public game scope" in review
    assert "Broader app-shell browser e2e remains open" in review
    assert "P2-UX-001" in state
    assert "Resolved for Ship It? Y/N public game scope" in state
