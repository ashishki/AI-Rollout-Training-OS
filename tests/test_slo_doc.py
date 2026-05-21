from pathlib import Path


def test_slo_doc_has_required_sections() -> None:
    slo = Path("docs/slo.md").read_text()

    assert "# Service SLOs" in slo
    assert "## Service Health Metrics" in slo
    assert "## SLO Targets" in slo
    assert "## Burn-Rate Signals" in slo
    assert "## Escalation Rules" in slo
    assert "API latency p95/p99" in slo
    assert "Feedback job latency p95/p99" in slo
    assert "Retrieval latency p95/p99" in slo
    assert "API error rate" in slo
    assert "Queue depth" in slo
    assert "Oldest job age" in slo
    assert "SEV-1" in slo
    assert "SEV-2" in slo
    assert "prompt text" in slo
    assert "learner artifacts" in slo
    assert "customer text" in slo
