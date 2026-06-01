from pathlib import Path

DOC = Path("docs/ship_it_yn_buyer_feedback.md")


def test_buyer_feedback_template_has_required_fields() -> None:
    document = DOC.read_text()

    for required in [
        "Buyer role:",
        "Team agent usage:",
        "Strongest scenario:",
        "Weakest scenario:",
        "Willingness to run workshop:",
        "Objections:",
        "Next action:",
    ]:
        assert required in document

    for supporting_field in [
        "Manual demo feedback template",
        "/demo/ship-it-yn",
        "Facilitator pack:",
        "Safe team summary:",
        "Local analytics snapshot:",
        "No PMF or paid-conversion claim",
    ]:
        assert supporting_field in document


def test_buyer_feedback_log_separates_observed_and_assumed() -> None:
    document = DOC.read_text()

    assert "## Evidence Log" in document
    assert "Observed evidence" in document
    assert "Founder/operator assumptions" in document
    assert "Assumptions do not count as buyer validation" in document
    assert document.index("Observed evidence") < document.index(
        "Founder/operator assumptions"
    )

    for forbidden in [
        "customer name",
        "personal email",
        "raw learner prompt",
        "proprietary workflow text",
        "credential",
        "secret",
    ]:
        assert forbidden in document.lower()
