from pathlib import Path


def test_security_review_packet_complete() -> None:
    text = Path("docs/security_review.md").read_text()

    required_sections = (
        "## Architecture",
        "## Data Flow",
        "## Subprocessors",
        "## Secrets Management",
        "## Identity And SSO",
        "## RBAC Permission Matrix",
        "## Audit Logs",
        "## Controls",
        "## Incident Response",
    )
    for section in required_sections:
        assert section in text

    for required_phrase in (
        "PostgreSQL/pgvector",
        "OIDC_CLIENT_SECRET",
        "append-only",
        "insufficient_evidence",
        "retention.redacted",
        "Rotate affected environment secrets",
    ):
        assert required_phrase in text
