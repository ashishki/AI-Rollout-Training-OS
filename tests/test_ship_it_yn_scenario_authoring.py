from pathlib import Path

DOC = Path("docs/ship_it_yn_scenario_authoring.md")


def test_scenario_authoring_workflow_has_required_controls() -> None:
    document = DOC.read_text()

    for required in [
        "Prompt Boundaries",
        "Required Human Review",
        "Schema Validation",
        "Safety Tests",
        "Blocked Live Scoring Usage",
        "PermissionGameScenario.model_validate",
        "tests/test_permission_game_scenarios.py",
        "tests/test_permission_game_safety.py",
        "tests/test_permission_game_scoring.py",
    ]:
        assert required in document

    for forbidden_claim in [
        "AI decides production approval",
        "AI is the scoring authority",
        "skip human review",
    ]:
        assert forbidden_claim.lower() not in document.lower()


def test_scenario_authoring_workflow_lists_pack_examples() -> None:
    document = DOC.read_text()

    for pack in [
        "Dev scenario pack",
        "Support scenario pack",
        "Ops scenario pack",
        "Data scenario pack",
        "Internal Tools scenario pack",
    ]:
        assert pack in document

    for risk in [
        "diff_misrepresentation",
        "indirect_prompt_injection",
        "network_access",
        "log_exposure",
        "overbroad_permission",
    ]:
        assert risk in document
