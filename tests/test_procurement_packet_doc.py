from pathlib import Path


def test_procurement_packet_complete() -> None:
    packet = Path("docs/procurement_packet.md").read_text()

    assert "# Procurement Packet" in packet
    assert "## Security Packet" in packet
    assert "## Privacy And Data Processing Summary" in packet
    assert "## Deployment Options" in packet
    assert "## Support Model" in packet
    assert "## Implementation Plan" in packet
    assert "docs/security_review.md" in packet
    assert "docs/packaging.md" in packet
    assert "docs/slo.md" in packet
    assert "docs/incident_response.md" in packet
    assert "docs/migration_rehearsal.md" in packet
    assert "Shared pilot deployment" in packet
    assert "Customer-dedicated deployment" in packet
    assert "Regulated single-tenant" in packet
    assert "Privacy" in packet
    assert "Support" in packet
