from pathlib import Path


def test_release_docs_complete() -> None:
    release_notes = Path("docs/release_notes.md").read_text()
    upgrade_guide = Path("docs/upgrade_guide.md").read_text()
    combined = f"{release_notes}\n{upgrade_guide}"

    assert "# Release Notes" in release_notes
    assert "# Upgrade Guide" in upgrade_guide
    assert "## Customer-Visible Behavior" in release_notes
    assert "## Major Changes" in release_notes
    assert "## Migrations" in release_notes
    assert "## Rollback" in release_notes
    assert "## Upgrade Impact" in release_notes
    assert "## Before Upgrade" in upgrade_guide
    assert "## Upgrade Steps" in upgrade_guide
    assert "## Validation" in upgrade_guide
    assert "0012_document_approval.py" in combined
    assert "0013_model_registry.py" in combined
    assert "0014_feedback_sampling.py" in combined
    assert "alembic upgrade head" in combined
    assert "docs/migration_rehearsal.md" in combined
    assert "docs/backup_restore.md" in combined
    assert "customer-visible" in combined.lower()
    assert "rollback" in combined.lower()
