import re
from pathlib import Path


def test_codex_prompt_records_initial_baseline() -> None:
    state = Path("docs/CODEX_PROMPT.md").read_text()
    baseline_match = re.search(r"- Baseline: (?P<count>\d+) passing tests", state)

    assert baseline_match is not None
    assert int(baseline_match.group("count")) >= 9
    assert "T04: Configuration And Observability Baseline" in state
    assert "| 2026-05-19 | T03: First Smoke Tests |" in state
