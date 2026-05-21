from pathlib import Path


def test_packaging_doc_has_required_tiers() -> None:
    packaging = Path("docs/packaging.md").read_text()

    assert "# Packaging And Pricing" in packaging
    assert "## Buyer And Value Metric" in packaging
    assert "## Package Tiers" in packaging
    assert "## Feature Boundaries" in packaging
    assert "## Pricing Rules" in packaging
    assert "Team Pilot" in packaging
    assert "Enterprise Enablement" in packaging
    assert "Governance Plus" in packaging
    assert "Regulated Single-Tenant" in packaging
    assert "Primary buyer" in packaging
    assert "Value metric" in packaging
    assert "Active learners" in packaging
    assert "Limits" in packaging
    assert "Pricing drivers" in packaging
    assert "Do not promise guaranteed" in packaging
    assert "productivity gains" in packaging
