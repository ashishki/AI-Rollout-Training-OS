import os
import re
from dataclasses import dataclass

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
DEFAULT_CUSTOMER_MARKERS = ("CUSTOMER_DATA", "CUSTOMER:")


@dataclass(frozen=True)
class RedactionResult:
    flagged: bool
    reasons: tuple[str, ...]


def inspect_sensitive_text(text: str) -> RedactionResult:
    reasons: list[str] = []
    if EMAIL_RE.search(text):
        reasons.append("email")
    markers = configured_customer_markers()
    if any(marker and marker in text for marker in markers):
        reasons.append("customer_data_marker")
    return RedactionResult(flagged=bool(reasons), reasons=tuple(reasons))


def configured_customer_markers() -> tuple[str, ...]:
    configured = os.getenv("CUSTOMER_DATA_MARKERS")
    if not configured:
        return DEFAULT_CUSTOMER_MARKERS
    return tuple(marker.strip() for marker in configured.split(",") if marker.strip())
