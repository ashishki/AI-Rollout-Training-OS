import json

import pytest
from ai_rollout_os.observability.ai_metrics import (
    AI_METRIC_LABEL_KEYS,
    AIMetricsLedger,
)


def test_ai_metrics_exclude_sensitive_text() -> None:
    ledger = AIMetricsLedger()
    record = ledger.record_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="feedback.generate",
        workspace_id="ws-1",
        operation_id="feedback_job_1",
        latency_ms=125.5,
        cost_usd=0.0042,
        input_tokens=500,
        output_tokens=120,
    )

    rendered = json.dumps(record.as_dict(), sort_keys=True)

    assert tuple(record.labels.as_dict()) == AI_METRIC_LABEL_KEYS
    assert "Customer ACME private workflow" not in rendered
    assert "alice@example.com" not in rendered
    assert "prompt" not in rendered
    assert "artifact" not in rendered

    with pytest.raises(ValueError, match="Unsafe AI metric label value"):
        ledger.record_call(
            provider="openai",
            model="gpt-4.1-mini",
            feature="feedback.generate",
            workspace_id="ws-1",
            operation_id="Customer ACME private workflow for alice@example.com",
            latency_ms=50,
            cost_usd=0.001,
        )

    assert len(ledger.records) == 1


def test_ai_metrics_group_cost_and_latency_by_provider_model_feature() -> None:
    ledger = AIMetricsLedger()
    ledger.record_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="feedback.generate",
        workspace_id="ws-1",
        operation_id="feedback_job_1",
        latency_ms=100,
        cost_usd=0.001,
        input_tokens=100,
        output_tokens=25,
    )
    ledger.record_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="feedback.generate",
        workspace_id="ws-1",
        operation_id="feedback_job_1",
        latency_ms=300,
        cost_usd=0.003,
        input_tokens=300,
        output_tokens=75,
    )
    ledger.record_call(
        provider="openai",
        model="gpt-4.1-mini",
        feature="risk.classify",
        workspace_id="ws-1",
        operation_id="feedback_job_1",
        latency_ms=40,
        cost_usd=0.0005,
    )

    summaries = [summary.as_dict() for summary in ledger.summarize()]

    assert len(summaries) == 2
    feedback_summary = summaries[0]
    assert feedback_summary["labels"] == {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "feature": "feedback.generate",
        "workspace_id": "ws-1",
        "operation_id": "feedback_job_1",
    }
    assert feedback_summary["call_count"] == 2
    assert feedback_summary["total_cost_usd"] == pytest.approx(0.004)
    assert feedback_summary["total_input_tokens"] == 400
    assert feedback_summary["total_output_tokens"] == 100
    assert feedback_summary["average_latency_ms"] == 200
    assert feedback_summary["p95_latency_ms"] == 300
