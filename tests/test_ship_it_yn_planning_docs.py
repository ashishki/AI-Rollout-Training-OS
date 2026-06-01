from pathlib import Path


def test_ship_it_yn_product_spec_defines_full_mvp() -> None:
    spec = Path("docs/ship_it_yn_product_spec.md").read_text()

    for required in [
        "Ship It? Y/N",
        "/demo/ship-it-yn",
        "React + Vite + TypeScript + Tailwind",
        "Seven Starter Levels",
        "Final Report",
        "No real command execution",
    ]:
        assert required in spec


def test_permission_game_schema_defines_required_contract() -> None:
    schema = Path("docs/permission_game_scenario_schema.md").read_text()

    for required in [
        "Allowed choices",
        "Permission boundaries",
        "Risk categories",
        "Validation Rules",
        "feedback for every playable choice",
    ]:
        assert required in schema


def test_frontend_architecture_requires_react_vite_and_browser_evidence() -> None:
    architecture = Path("docs/ship_it_yn_frontend_architecture.md").read_text()

    for required in [
        "React + Vite + TypeScript + Tailwind",
        "frontend/permission_game/",
        "FastAPI serving",
        "Browser Evidence",
        "Playwright",
    ]:
        assert required in architecture


def test_ai_development_plan_lists_next_phases_end_to_end() -> None:
    plan = Path("docs/ship_it_yn_ai_development_plan.md").read_text()

    for phase in [
        "Phase 17 - Product And Architecture Blueprint",
        "Phase 18 - Scenario And Scoring Core",
        "Phase 19 - React/Vite Playable Game",
        "Phase 20 - Browser Polish And Public Demo Evidence",
        "Phase 21 - Workshop, Analytics, And Buyer Validation",
    ]:
        assert phase in plan


def test_task_graph_sets_ship_it_yn_next_implementation_work() -> None:
    graph = Path("docs/product_maturity_task_graph.md").read_text()
    state = Path("docs/CODEX_PROMPT.md").read_text()

    for task in ["T75", "T80", "T85", "T91", "T98", "T105"]:
        assert f"## {task}:" in graph

    assert "Phase 17 - Ship It? Y/N Product And Architecture Blueprint" in graph
    assert (
        "Current phase: Phase 21 - Workshop, Analytics, And Buyer Validation" in state
    )
    assert "PHASE18-SCENARIO-SCORING" in state
    assert (
        "Active next task: Manual buyer demos (human-owned evidence collection)"
        in state
    )
