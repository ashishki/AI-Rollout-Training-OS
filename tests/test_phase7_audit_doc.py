from pathlib import Path


def test_phase7_audit_records_workflow_status() -> None:
    doc = Path("docs/audit/PHASE7_UX_AUDIT.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    for required in [
        "PHASE7_UX_AUDIT: CONDITIONAL_GO",
        "## Critical Workflows",
        "## Open UX Blockers",
        "P2-UX-001",
        "Operator setup",
        "Learner mission flow",
        "Manager review",
    ]:
        assert required in doc

    assert "PHASE7-UX" in index
    assert "docs/audit/PHASE7_UX_AUDIT.md" in index
