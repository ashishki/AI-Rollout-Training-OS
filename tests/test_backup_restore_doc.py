from pathlib import Path


def test_backup_restore_doc_has_required_sections() -> None:
    text = Path("docs/backup_restore.md").read_text()

    required_headings = (
        "## Backup Procedure",
        "## Restore Procedure",
        "## Retention Procedure",
        "## Rollback Procedure",
    )
    for heading in required_headings:
        assert heading in text
    for required_phrase in (
        "pg_dump",
        "pg_restore",
        "retention.redacted",
        "audit_events",
        "rollback",
    ):
        assert required_phrase in text
