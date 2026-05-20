from pathlib import Path


def test_phase6_audit_records_pmf_gate() -> None:
    doc = Path("docs/audit/PHASE6_PMF_AUDIT.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    for required in [
        "PHASE6_PMF_AUDIT: CONDITIONAL_GO",
        "Go/no-go status",
        "## PMF Evidence",
        "## Gaps",
        "Phase 6 exit gate",
        "No-go for claiming PMF",
    ]:
        assert required in doc

    assert "PHASE6-PMF" in index
    assert "docs/audit/PHASE6_PMF_AUDIT.md" in index
