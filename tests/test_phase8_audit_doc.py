from pathlib import Path


def test_phase8_audit_doc_records_security_gate() -> None:
    audit = Path("docs/audit/PHASE8_SECURITY_AUDIT.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "Status: PASS" in audit
    assert "No P0 or P1 blockers are open" in audit
    assert "T35-T38" in audit
    assert "P2-UX-001" in audit
    assert "PHASE8-SECURITY" in index
    assert "docs/audit/PHASE8_SECURITY_AUDIT.md" in index
