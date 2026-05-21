from pathlib import Path


def test_production_readiness_audit_complete() -> None:
    audit = Path("docs/audit/PRODUCTION_READINESS_AUDIT.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "# Production Readiness Audit" in audit
    assert "Status: NOT READY FOR GA" in audit
    assert "## GA Decision" in audit
    assert "## Evidence Links" in audit
    assert "## Open Blockers For GA" in audit
    assert "## Accepted Risks For Controlled Pilots" in audit
    assert "## Final Readiness Result" in audit
    assert "NO-GO FOR GA" in audit
    assert "GA-BLOCKER-001" in audit
    assert "Browser automation" in audit
    assert "Paid customer or signed expansion path" in audit
    assert "docs/ga_readiness.md" in audit
    assert "docs/release_notes.md" in audit
    assert "PRODUCTION-READINESS" in index
    assert "docs/audit/PRODUCTION_READINESS_AUDIT.md" in index
