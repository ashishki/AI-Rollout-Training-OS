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


@dataclass(frozen=True)
class GameSessionSummary:
    total_score: int
    safety_score: int
    meter_totals: GameMeterDeltas
    badges: tuple[str, ...]
    final_title: str
    unsafe_approvals: int
    overblocks: int
    strongest_habit: str
    weakest_risk_area: str
    share_text: str


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


def summarize_game_session(results: list[GameDecisionResult]) -> GameSessionSummary:
    if not results:
        raise ValueError("game session summary requires at least one decision")

    total_score = _clamp(sum(result.score_delta for result in results), 0, 100)
    safety_score = _clamp(sum(result.safety_score_delta for result in results), 0, 100)
    unsafe_approvals = sum(1 for result in results if result.outcome == "unsafe")
    overblocks = sum(1 for result in results if result.outcome == "overblock")
    meter_totals = _meter_totals(results)
    badges = _badges_for_results(results)
    final_title = _final_title(
        total_score=total_score,
        unsafe_approvals=unsafe_approvals,
        overblocks=overblocks,
        badges=badges,
    )
    strongest_habit = _strongest_habit(badges)
    weakest_risk_area = _weakest_risk_area(results)

    return GameSessionSummary(
        total_score=total_score,
        safety_score=safety_score,
        meter_totals=meter_totals,
        badges=badges,
        final_title=final_title,
        unsafe_approvals=unsafe_approvals,
        overblocks=overblocks,
        strongest_habit=strongest_habit,
        weakest_risk_area=weakest_risk_area,
        share_text=(
            f"Ship It? Y/N score: {total_score}/100 - {final_title}. "
            f"Unsafe approvals: {unsafe_approvals}. Overblocks: {overblocks}."
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


def _meter_totals(results: list[GameDecisionResult]) -> GameMeterDeltas:
    return GameMeterDeltas(
        velocity=_clamp(
            sum(result.meter_deltas.velocity for result in results), -100, 100
        ),
        blast_radius=_clamp(
            sum(result.meter_deltas.blast_radius for result in results), -100, 100
        ),
        trust=_clamp(sum(result.meter_deltas.trust for result in results), -100, 100),
        eval_confidence=_clamp(
            sum(result.meter_deltas.eval_confidence for result in results), -100, 100
        ),
        audit_trail=_clamp(
            sum(result.meter_deltas.audit_trail for result in results), -100, 100
        ),
    )


def _badges_for_results(results: list[GameDecisionResult]) -> tuple[str, ...]:
    badges: list[str] = []
    correct_decisions = {
        result.selected_decision for result in results if result.outcome == "correct"
    }
    if "restrict_scope" in correct_decisions:
        badges.append("least_privilege_operator")
    if "require_eval" in correct_decisions:
        badges.append("eval_gate_preserved")
    if "run_in_sandbox" in correct_decisions:
        badges.append("bounded_execution")
    if all(result.outcome != "unsafe" for result in results):
        badges.append("clean_approval_trail")
    return tuple(dict.fromkeys(badges))


def _final_title(
    *, total_score: int, unsafe_approvals: int, overblocks: int, badges: tuple[str, ...]
) -> str:
    if unsafe_approvals:
        return "Risky Speedrunner"
    if overblocks >= 2:
        return "Cautious Gatekeeper"
    if total_score >= 80 and "least_privilege_operator" in badges:
        return "Least Privilege Operator"
    if total_score >= 60:
        return "Steady Release Reviewer"
    return "Permission Apprentice"


def _strongest_habit(badges: tuple[str, ...]) -> str:
    if "least_privilege_operator" in badges:
        return "scoped access"
    if "eval_gate_preserved" in badges:
        return "eval discipline"
    if "bounded_execution" in badges:
        return "sandboxed execution"
    return "audit awareness"


def _weakest_risk_area(results: list[GameDecisionResult]) -> str:
    for result in results:
        if result.outcome == "unsafe":
            return result.scenario_id
    for result in results:
        if result.outcome == "overblock":
            return result.scenario_id
    return "none"


def _clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


__all__ = [
    "GameDecisionResult",
    "GameSessionSummary",
    "score_game_decision",
    "summarize_game_session",
]
