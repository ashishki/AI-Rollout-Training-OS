from pathlib import Path

README = Path("README.md")


def test_readme_positions_ship_it_yn_as_permission_game() -> None:
    readme = README.read_text()
    first_screen = readme[:1200]

    assert readme.startswith("# Ship It? Y/N - AI Permission Judgment Game")
    assert "public front door for AI Rollout Training OS" in first_screen
    assert "permission judgment game" in first_screen
    assert "not a generic LMS" in first_screen
    assert "not a compliance certificate" in first_screen
    assert "not a real agent runner" in first_screen
    assert "Local demo route: `/demo/ship-it-yn`" in first_screen


def test_readme_includes_ship_it_yn_cta_and_claim_boundaries() -> None:
    readme = README.read_text()

    for required in [
        "Primary CTA",
        "http://127.0.0.1:8000/demo/ship-it-yn",
        "docs/audit/artifacts/ship_it_yn_desktop.png",
        "docs/audit/artifacts/ship_it_yn_mobile.png",
        "## Для кого",
        "Engineering team leads",
        "AI rollout facilitators",
        "Developers using agentic coding tools",
        "## Blocked claims",
        "No certified safety claim.",
        "No compliance approval claim.",
        "No production readiness claim.",
        "No PMF, paid conversion, or customer adoption claim.",
        "No autonomous execution or real privileged-action approval claim.",
    ]:
        assert required in readme
