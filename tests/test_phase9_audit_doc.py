from pathlib import Path


def test_phase9_audit_doc_records_governance_gate() -> None:
    audit = Path("docs/audit/PHASE9_GOVERNANCE_AUDIT.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "Status: PASS" in audit
    assert "No P0 or P1 blockers are open" in audit
    assert "T39-T42" in audit
    assert "reproducible" in audit
    assert "P2-UX-001" in audit
    assert "PHASE9-GOVERNANCE" in index
    assert "docs/audit/PHASE9_GOVERNANCE_AUDIT.md" in index
