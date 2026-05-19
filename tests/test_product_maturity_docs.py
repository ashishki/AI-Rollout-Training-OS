from pathlib import Path


def test_product_maturity_roadmap_has_required_phases() -> None:
    doc = Path("docs/product_maturity_roadmap.md").read_text()

    for heading in [
        "## Phase 6 - PMF Pilot System",
        "## Phase 7 - Core Product UX",
        "## Phase 8 - Enterprise Security",
        "## Phase 9 - Governance Layer",
        "## Phase 10 - Integrations",
        "## Phase 11 - AI Quality & Model Ops",
        "## Phase 12 - Reliability & Scale",
        "## Phase 13 - Commercial Packaging",
        "## Phase 14 - GA Readiness",
    ]:
        assert heading in doc


def test_product_maturity_task_graph_is_ai_loop_ready() -> None:
    graph = Path("docs/product_maturity_task_graph.md").read_text()

    for task in ["T25", "T30", "T35", "T39", "T43", "T47", "T51", "T55", "T61"]:
        assert f"## {task}:" in graph

    assert "Acceptance-Criteria:" in graph
    assert "Context-Refs:" in graph
    assert "Depends-On:" in graph


def test_orchestrator_knows_post_mvp_task_graph() -> None:
    prompt = Path("docs/prompts/ORCHESTRATOR.md").read_text()
    state = Path("docs/CODEX_PROMPT.md").read_text()

    assert "docs/product_maturity_task_graph.md" in prompt
    assert "docs/product_maturity_task_graph.md" in state
    assert "T25: Pilot Outcome Metrics Model" in state
