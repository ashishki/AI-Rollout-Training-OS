from pathlib import Path


def test_phase11_audit_doc_records_ai_quality_gate() -> None:
    audit = Path("docs/audit/PHASE11_AI_QUALITY_AUDIT.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "Status: PASS" in audit
    assert "No P0 or P1 blockers are open" in audit
    assert "T47-T50" in audit
    assert "feedback quality" in audit
    assert "provider, model, feature" in audit
    assert "workspace ID, and operation ID" in audit
    assert "learner artifact text" in audit
    assert "P2-UX-001" in audit
    assert "PHASE11-AI-QUALITY" in index
    assert "docs/audit/PHASE11_AI_QUALITY_AUDIT.md" in index
