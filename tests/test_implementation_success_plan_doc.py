from pathlib import Path


def test_implementation_success_plan_complete() -> None:
    plan = Path("docs/implementation_success_plan.md").read_text()

    assert "# Implementation Success Plan" in plan
    assert "## Roles And Owners" in plan
    assert "## Timeline" in plan
    assert "## Kickoff" in plan
    assert "## Policy Ingestion" in plan
    assert "## Role-Pack Setup" in plan
    assert "## Cohort Launch" in plan
    assert "## Manager Review" in plan
    assert "## Reporting" in plan
    assert "## Expansion Review" in plan
    assert "Owner responsibilities" in plan
    assert "Customer responsibilities" in plan
    assert "Implementation responsibilities" in plan
    assert "Expand" in plan
    assert "repeat" in plan
    assert "pause" in plan
    assert "reposition" in plan
