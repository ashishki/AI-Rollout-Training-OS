from pathlib import Path


def test_success_rubric_has_outcome_decisions() -> None:
    doc = Path("docs/pilot_success_rubric.md").read_text()

    for outcome in ["### Expand", "### Repeat", "### Pause", "### Reposition"]:
        assert outcome in doc

    assert "Decision: expand | repeat | pause | reposition" in doc


def test_success_rubric_covers_metric_groups() -> None:
    doc = Path("docs/pilot_success_rubric.md").read_text()

    for group in ["Product metrics", "Quality metrics", "Business metrics"]:
        assert group in doc

    for metric in [
        "Activation rate",
        "assignment completion rate",
        "citation precision",
        "no-answer accuracy",
        "Pilot-to-paid conversion",
        "time to first approved workflow change",
    ]:
        assert metric in doc
