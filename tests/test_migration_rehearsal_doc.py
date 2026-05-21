from pathlib import Path


def test_migration_rehearsal_doc_complete() -> None:
    rehearsal = Path("docs/migration_rehearsal.md").read_text()

    assert "# Migration Rehearsal" in rehearsal
    assert "## Backup Step" in rehearsal
    assert "## Upgrade Step" in rehearsal
    assert "## Validation Step" in rehearsal
    assert "## Rollback Plan" in rehearsal
    assert "## Restore Step" in rehearsal
    assert "## Go / No-Go Criteria" in rehearsal
    assert "alembic upgrade head" in rehearsal
    assert "alembic current" in rehearsal
    assert "pg_restore --clean --if-exists --no-owner" in rehearsal
    assert "docs/backup_restore.md" in rehearsal
    assert "docs/incident_response.md" in rehearsal
    assert "audit event count did not decrease" in rehearsal
    assert "Sensitive content appears" in rehearsal
