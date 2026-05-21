from pathlib import Path


def test_incident_response_doc_complete() -> None:
    runbook = Path("docs/incident_response.md").read_text()

    assert "# Incident Response Runbook" in runbook
    assert "## Severity And Escalation" in runbook
    assert "## Common First Response" in runbook
    assert "## Retrieval Outage" in runbook
    assert "## Feedback Job Backlog" in runbook
    assert "## Data Leak Suspicion" in runbook
    assert "## Failed Migrations" in runbook
    assert "## Provider Degradation" in runbook
    assert "## Closure Checklist" in runbook
    assert "SEV-1" in runbook
    assert "SEV-2" in runbook
    assert "operator on call" in runbook
    assert "incident commander" in runbook
    assert "preserve audit logs" in runbook
    assert "Route new submissions to manager review" in runbook
    assert "workspace IDs" in runbook
    assert "Do not copy sensitive text into incident notes" in runbook
    assert "docs/backup_restore.md" in runbook
