import json
import re
from pathlib import Path
from typing import Any

GAME_SCENARIO_DIR = Path("ai_rollout_os/permissions/game_scenarios")

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(
        r"\b(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_/-]{8,}",
        re.I,
    ),
    re.compile(r"\b[A-Za-z0-9_/-]{24,}\.[A-Za-z0-9_/-]{12,}\.[A-Za-z0-9_/-]{12,}\b"),
]

DANGEROUS_COMMAND_PATTERNS = [
    re.compile(r"\brm\s+-rf\b"),
    re.compile(r"\bsudo\s+"),
    re.compile(r"\bcurl\s+https?://"),
    re.compile(r"\bwget\s+https?://"),
    re.compile(r"\b(?:bash|sh)\s+-c\b"),
    re.compile(r"\bnpm\s+install\b"),
    re.compile(r"\bpip\s+install\b"),
]

UNSUPPORTED_CLAIM_PATTERNS = [
    re.compile(r"\bcertif(?:y|ied|ication)\b", re.I),
    re.compile(r"\bcompliance\s+(?:approval|approved|certification)\b", re.I),
    re.compile(r"\bproduction[-\s]?safe\b", re.I),
    re.compile(r"\bproduction[-\s]?ready\b", re.I),
    re.compile(r"\bpmf\b", re.I),
    re.compile(r"\bpaid\s+conversion\b", re.I),
    re.compile(r"\bguaranteed\s+(?:safety|productivity|incident reduction)\b", re.I),
]

CUSTOMER_DATA_DOMAIN_PATTERN = re.compile(
    r"\bcustomer\s+data\b.*\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", re.I | re.S
)


def test_game_scenarios_do_not_contain_real_execution_or_secret_material() -> None:
    scenario_text = "\n".join(_scenario_text_values())

    for pattern in SECRET_PATTERNS:
        assert not pattern.search(scenario_text), pattern.pattern
    for pattern in DANGEROUS_COMMAND_PATTERNS:
        assert not pattern.search(scenario_text), pattern.pattern
    assert not CUSTOMER_DATA_DOMAIN_PATTERN.search(scenario_text)


def test_game_scenarios_block_unsupported_claims() -> None:
    scenario_text = "\n".join(_scenario_text_values())

    for pattern in UNSUPPORTED_CLAIM_PATTERNS:
        assert not pattern.search(scenario_text), pattern.pattern


def _scenario_text_values() -> list[str]:
    values: list[str] = []
    for path in sorted(GAME_SCENARIO_DIR.glob("*.json")):
        values.extend(_string_values(json.loads(path.read_text())))
    return values


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for entry in value for item in _string_values(entry)]
    if isinstance(value, dict):
        return [item for entry in value.values() for item in _string_values(entry)]
    return []
