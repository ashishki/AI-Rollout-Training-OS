from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

GameChoiceId = Literal[
    "approve",
    "deny",
    "inspect_diff",
    "run_in_sandbox",
    "require_eval",
    "restrict_scope",
    "escalate_reviewer",
    "rollback",
]

GamePermissionBoundary = Literal["allowed", "needs_approval", "blocked", "unknown"]

GameRiskCategory = Literal[
    "secrets",
    "destructive_filesystem",
    "diff_misrepresentation",
    "test_deletion",
    "indirect_prompt_injection",
    "overbroad_permission",
    "eval_bypass",
    "dependency_install",
    "ci_edit",
    "network_access",
    "log_exposure",
    "scope_creep",
    "context_contamination",
]

GameFeedbackOutcome = Literal["correct", "partial", "unsafe", "overblock"]


class GameToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=1, max_length=64)
    surface: str = Field(min_length=1, max_length=64)
    scope: str = Field(min_length=1, max_length=64)
    permission_request: str = Field(min_length=1, max_length=64)


class GameContextItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1)
    trusted: bool


class GameInspectArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9][a-z0-9-]*$")
    label: str = Field(min_length=1, max_length=80)
    kind: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    reveals_risk: GameRiskCategory


class GameMeterDeltas(BaseModel):
    model_config = ConfigDict(extra="forbid")

    velocity: int = Field(ge=-100, le=100)
    blast_radius: int = Field(ge=-100, le=100)
    trust: int = Field(ge=-100, le=100)
    eval_confidence: int = Field(ge=-100, le=100)
    audit_trail: int = Field(ge=-100, le=100)


class GameChoiceFeedback(BaseModel):
    model_config = ConfigDict(extra="forbid")

    outcome: GameFeedbackOutcome
    consequence: str = Field(min_length=1)
    lesson: str = Field(min_length=1)
    safer_alternative: str = Field(min_length=1)


class PermissionGameScenario(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9][a-z0-9-]*$")
    level: int = Field(ge=1, le=7)
    title: str = Field(min_length=1, max_length=120)
    agent_name: str = Field(min_length=1, max_length=80)
    agent_message: str = Field(min_length=1)
    tool_call: GameToolCall
    context: list[GameContextItem] = Field(min_length=1)
    inspect_artifacts: list[GameInspectArtifact] = Field(min_length=1)
    choices: list[GameChoiceId] = Field(min_length=1)
    best_choices: list[GameChoiceId] = Field(min_length=1)
    acceptable_choices: list[GameChoiceId] = Field(default_factory=list)
    unsafe_choices: list[GameChoiceId] = Field(default_factory=list)
    overblock_choices: list[GameChoiceId] = Field(default_factory=list)
    permission_boundary: GamePermissionBoundary
    risk_category: GameRiskCategory
    meters: GameMeterDeltas
    feedback: dict[GameChoiceId, GameChoiceFeedback] = Field(min_length=1)
    badges: list[str] = Field(min_length=1)
    audit_events: list[str] = Field(min_length=1)
    facilitator_notes: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_choice_contract(self) -> "PermissionGameScenario":
        choices = set(self.choices)
        if len(choices) != len(self.choices):
            raise ValueError("game scenario choices must be unique")

        for label, selected_choices in {
            "best_choices": self.best_choices,
            "acceptable_choices": self.acceptable_choices,
            "unsafe_choices": self.unsafe_choices,
            "overblock_choices": self.overblock_choices,
        }.items():
            unknown = sorted(set(selected_choices) - choices)
            if unknown:
                raise ValueError(f"{label} must reference declared choices: {unknown}")

        missing_feedback = sorted(choices - set(self.feedback))
        if missing_feedback:
            raise ValueError(
                "game scenario feedback missing choices: " + ", ".join(missing_feedback)
            )

        extra_feedback = sorted(set(self.feedback) - choices)
        if extra_feedback:
            raise ValueError(
                "game scenario feedback references undeclared choices: "
                + ", ".join(extra_feedback)
            )

        artifact_risks = {artifact.reveals_risk for artifact in self.inspect_artifacts}
        if self.risk_category not in artifact_risks:
            raise ValueError("inspect_artifacts must reveal the scenario risk_category")

        return self


__all__ = [
    "GameChoiceFeedback",
    "GameChoiceId",
    "GameContextItem",
    "GameFeedbackOutcome",
    "GameInspectArtifact",
    "GameMeterDeltas",
    "GamePermissionBoundary",
    "GameRiskCategory",
    "GameToolCall",
    "PermissionGameScenario",
]
