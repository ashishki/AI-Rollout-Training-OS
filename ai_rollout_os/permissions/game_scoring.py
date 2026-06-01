from dataclasses import dataclass

from ai_rollout_os.permissions.game_schema import (
    GameMeterDeltas,
    PermissionGameScenario,
)

OUTCOME_SCORE_DELTAS = {
    "correct": 15,
    "partial": 5,
    "unsafe": -25,
    "overblock": -6,
}

SAFETY_SCORE_DELTAS = {
    "correct": 10,
    "partial": 3,
    "unsafe": -20,
    "overblock": 0,
}


@dataclass(frozen=True)
class GameDecisionResult:
    scenario_id: str
    level: int
    selected_decision: str
    outcome: str
    consequence: str
    lesson: str
    safer_alternative: str
    meter_deltas: GameMeterDeltas
    score_delta: int
    safety_score_delta: int
    audit_events: tuple[str, ...]

    @property
    def marks_player_unsafe(self) -> bool:
        return self.outcome == "unsafe"


def score_game_decision(
    scenario: PermissionGameScenario, selected_decision: str
) -> GameDecisionResult:
    if selected_decision not in scenario.choices:
        raise ValueError(f"unknown game decision for scenario {scenario.id}")

    feedback = scenario.feedback[selected_decision]
    outcome = feedback.outcome

    return GameDecisionResult(
        scenario_id=scenario.id,
        level=scenario.level,
        selected_decision=selected_decision,
        outcome=outcome,
        consequence=feedback.consequence,
        lesson=feedback.lesson,
        safer_alternative=feedback.safer_alternative,
        meter_deltas=_meter_deltas_for_outcome(scenario.meters, outcome),
        score_delta=OUTCOME_SCORE_DELTAS[outcome],
        safety_score_delta=SAFETY_SCORE_DELTAS[outcome],
        audit_events=(
            *scenario.audit_events,
            f"decision:{selected_decision}",
            f"outcome:{outcome}",
        ),
    )


def _meter_deltas_for_outcome(meters: GameMeterDeltas, outcome: str) -> GameMeterDeltas:
    if outcome == "correct":
        return meters
    if outcome == "partial":
        return GameMeterDeltas(
            velocity=_halve(meters.velocity),
            blast_radius=_halve(meters.blast_radius),
            trust=_halve(meters.trust),
            eval_confidence=_halve(meters.eval_confidence),
            audit_trail=_halve(meters.audit_trail),
        )
    if outcome == "overblock":
        return GameMeterDeltas(
            velocity=-max(abs(meters.velocity), 8),
            blast_radius=-abs(_halve(meters.blast_radius)),
            trust=min(meters.trust, 0),
            eval_confidence=0,
            audit_trail=max(_halve(meters.audit_trail), 0),
        )
    return GameMeterDeltas(
        velocity=max(abs(_halve(meters.velocity)), 4),
        blast_radius=max(abs(meters.blast_radius), 20),
        trust=-max(abs(meters.trust), 10),
        eval_confidence=-max(abs(meters.eval_confidence), 10),
        audit_trail=-max(abs(meters.audit_trail), 10),
    )


def _halve(value: int) -> int:
    return int(value / 2)


__all__ = ["GameDecisionResult", "score_game_decision"]
