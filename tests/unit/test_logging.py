import json
import logging

from ai_rollout_os.observability.logging import REDACTED, StructuredJsonFormatter


def test_logging_formatter_redacts_sensitive_fields() -> None:
    record = logging.LogRecord(
        name="ai_rollout_os.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="learner alice@example.com submitted an artifact",
        args=(),
        exc_info=None,
    )
    record.trace_id = "trace-123"
    record.operation = "submission.review"
    record.result = "ok"
    record.learner_submission_text = "Customer ACME private workflow"
    record.email = "alice@example.com"

    rendered = StructuredJsonFormatter().format(record)
    payload = json.loads(rendered)

    assert "alice@example.com" not in rendered
    assert "Customer ACME private workflow" not in rendered
    assert payload["learner_submission_text"] == REDACTED
    assert payload["email"] == REDACTED
    assert payload["message"] == "learner [REDACTED_EMAIL] submitted an artifact"
