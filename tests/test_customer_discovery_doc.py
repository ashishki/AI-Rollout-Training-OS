from pathlib import Path


def test_customer_discovery_doc_has_required_sections() -> None:
    doc = Path("docs/customer_discovery.md").read_text()

    for heading in [
        "## Evidence Schema",
        "## Interview Log Template",
        "## Decision Rules",
        "## Registry",
    ]:
        assert heading in doc

    for field in [
        "`record_id`",
        "`date`",
        "`company_segment`",
        "`icp_fit`",
        "`buyer_role`",
        "`internal_blockers`",
        "`current_workaround`",
        "`adoption_blocker`",
        "`willingness_to_pay_signal`",
        "`pilot_outcome_notes`",
        "`confidence_level`",
    ]:
        assert field in doc

    for decision in ["expand", "repeat", "pause", "reposition"]:
        assert decision in doc


def test_customer_discovery_doc_distinguishes_evidence_from_assumptions() -> None:
    doc = Path("docs/customer_discovery.md").read_text()
    observed = doc.split("## Observed Customer Evidence", maxsplit=1)[1].split(
        "## Internal Assumptions", maxsplit=1
    )[0]
    assumptions = doc.split("## Internal Assumptions", maxsplit=1)[1].split(
        "## Decision Rules", maxsplit=1
    )[0]

    assert "direct customer or pilot artifacts" in observed
    assert "Internal assumptions are allowed only when labeled" in assumptions
    assert "cannot satisfy Phase 6 exit gates by themselves" in assumptions
