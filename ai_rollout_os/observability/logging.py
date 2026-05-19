import json
import logging
import re
from typing import Any

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
REDACTED = "[REDACTED]"
REDACTED_EMAIL = "[REDACTED_EMAIL]"

SENSITIVE_FIELDS = {
    "ai_provider_api_key",
    "api_key",
    "company_policy_text",
    "email",
    "full_name",
    "learner_submission_text",
    "manager_comments",
    "password",
    "policy_body",
    "secret_key",
    "sop_text",
    "submission_text",
    "token",
}

STANDARD_LOG_RECORD_FIELDS = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)


def redact_text(value: str) -> str:
    return EMAIL_RE.sub(REDACTED_EMAIL, value)


def redact_value(key: str, value: Any) -> Any:
    if key in SENSITIVE_FIELDS:
        return REDACTED
    if isinstance(value, str):
        return redact_text(value)
    return value


class StructuredJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "message": redact_text(record.getMessage()),
            "trace_id": getattr(record, "trace_id", "unknown"),
            "env": getattr(record, "env", "unknown"),
            "service": getattr(record, "service", "ai-rollout-training-os"),
            "operation": getattr(record, "operation", "unknown"),
            "result": getattr(record, "result", "unknown"),
        }

        for key, value in record.__dict__.items():
            if key in STANDARD_LOG_RECORD_FIELDS or key in payload:
                continue
            payload[key] = redact_value(key, value)

        return json.dumps(payload, sort_keys=True)


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredJsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
