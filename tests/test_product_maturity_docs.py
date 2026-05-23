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
        "## Phase 15 - Solo Showcase And Small-Team Rollout",
    ]:
        assert heading in doc


def test_product_maturity_task_graph_is_ai_loop_ready() -> None:
    graph = Path("docs/product_maturity_task_graph.md").read_text()

    for task in [
        "T25",
        "T30",
        "T35",
        "T39",
        "T43",
        "T47",
        "T51",
        "T55",
        "T61",
        "T62",
        "T68",
    ]:
        assert f"## {task}:" in graph

    assert "Acceptance-Criteria:" in graph
    assert "Context-Refs:" in graph
    assert "Depends-On:" in graph


def test_orchestrator_knows_post_mvp_task_graph() -> None:
    prompt = Path("docs/prompts/ORCHESTRATOR.md").read_text()
    state = Path("docs/CODEX_PROMPT.md").read_text()

    assert "docs/product_maturity_task_graph.md" in prompt
    assert "docs/product_maturity_task_graph.md" in state
    assert "Post-MVP production maturity graph" in state
    assert "Active next task:" in state


def test_roadmap_lists_phase_6_metrics() -> None:
    doc = Path("docs/product_maturity_roadmap.md").read_text()
    phase_6 = doc.split("## Phase 6 - PMF Pilot System", maxsplit=1)[1].split(
        "## Phase 7 - Core Product UX", maxsplit=1
    )[0]

    for metric in [
        "Activation rate",
        "Completion rate",
        "Approved workflow changes",
        "Manager review time",
        "Risk rate",
        "Time-to-first-safe-use",
    ]:
        assert metric in phase_6

    assert "Phase 6 exit gate" in phase_6
