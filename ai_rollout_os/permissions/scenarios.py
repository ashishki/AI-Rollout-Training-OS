from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CHOICE_IDS = {
    "approve",
    "deny",
    "ask_for_clarification",
    "run_in_sandbox",
    "escalate_to_reviewer",
}

PERMISSION_BOUNDARIES = {"allowed", "needs_approval", "blocked", "unknown"}


class ScenarioValidationError(ValueError):
    """Raised when a permission scenario record is incomplete or inconsistent."""


@dataclass(frozen=True)
class PermissionScenario:
    id: str
    title: str
    request: str
    context: str
    choices: tuple[str, ...]
    correct_decision: str
    permission_boundary: str
    risk_category: str
    safer_alternative: str
    lesson_text: str

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> PermissionScenario:
        required_fields = {
            "id",
            "title",
            "request",
            "context",
            "choices",
            "correct_decision",
            "permission_boundary",
            "risk_category",
            "safer_alternative",
            "lesson_text",
        }
        missing = sorted(
            field
            for field in required_fields
            if field not in data or data[field] in ("", [], None)
        )
        if missing:
            raise ScenarioValidationError(
                f"permission scenario missing required fields: {', '.join(missing)}"
            )

        choices = tuple(data["choices"])
        if not choices or any(choice not in CHOICE_IDS for choice in choices):
            raise ScenarioValidationError(
                f"permission scenario {data['id']} has invalid choices"
            )

        correct_decision = str(data["correct_decision"])
        if correct_decision not in choices:
            raise ScenarioValidationError(
                f"permission scenario {data['id']} correct_decision is not a choice"
            )

        permission_boundary = str(data["permission_boundary"])
        if permission_boundary not in PERMISSION_BOUNDARIES:
            raise ScenarioValidationError(
                f"permission scenario {data['id']} has invalid permission boundary"
            )

        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            request=str(data["request"]),
            context=str(data["context"]),
            choices=choices,
            correct_decision=correct_decision,
            permission_boundary=permission_boundary,
            risk_category=str(data["risk_category"]),
            safer_alternative=str(data["safer_alternative"]),
            lesson_text=str(data["lesson_text"]),
        )


def load_scenarios(path: Path) -> list[PermissionScenario]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ScenarioValidationError("permission scenario library must be a list")
    return [PermissionScenario.from_mapping(item) for item in data]
