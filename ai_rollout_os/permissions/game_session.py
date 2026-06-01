from dataclasses import dataclass

from ai_rollout_os.permissions.game_scoring import (
    GameDecisionResult,
    GameSessionSummary,
    summarize_game_session,
)


@dataclass(frozen=True)
class PublicGameDecision:
    scenario_id: str
    selected_decision: str
    outcome: str
    inspected_artifact_ids: tuple[str, ...]


@dataclass(frozen=True)
class PublicGameSessionState:
    session_id: str
    scenario_order: tuple[str, ...]
    decisions: tuple[PublicGameDecision, ...]
    elapsed_seconds: int
    meter_totals: dict[str, int]
    badges: tuple[str, ...]
    final_report: dict[str, object]

    def to_public_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "scenario_order": list(self.scenario_order),
            "decisions": [
                {
                    "scenario_id": decision.scenario_id,
                    "selected_decision": decision.selected_decision,
                    "outcome": decision.outcome,
                    "inspected_artifact_ids": list(decision.inspected_artifact_ids),
                }
                for decision in self.decisions
            ],
            "elapsed_seconds": self.elapsed_seconds,
            "meter_totals": dict(self.meter_totals),
            "badges": list(self.badges),
            "final_report": dict(self.final_report),
        }


def build_public_game_session_state(
    *,
    session_id: str,
    scenario_order: list[str],
    decision_results: list[GameDecisionResult],
    inspected_artifacts_by_scenario: dict[str, list[str]],
    elapsed_seconds: int,
) -> PublicGameSessionState:
    if not session_id:
        raise ValueError("public game session requires a session_id")
    if elapsed_seconds < 0:
        raise ValueError("public game session elapsed_seconds cannot be negative")

    summary = summarize_game_session(decision_results)
    return PublicGameSessionState(
        session_id=session_id,
        scenario_order=tuple(scenario_order),
        decisions=tuple(
            PublicGameDecision(
                scenario_id=result.scenario_id,
                selected_decision=result.selected_decision,
                outcome=result.outcome,
                inspected_artifact_ids=tuple(
                    inspected_artifacts_by_scenario.get(result.scenario_id, [])
                ),
            )
            for result in decision_results
        ),
        elapsed_seconds=elapsed_seconds,
        meter_totals=summary.meter_totals.model_dump(),
        badges=summary.badges,
        final_report=_final_report(summary),
    )


def _final_report(summary: GameSessionSummary) -> dict[str, object]:
    return {
        "final_score": summary.total_score,
        "safety_score": summary.safety_score,
        "title": summary.final_title,
        "unsafe_approvals": summary.unsafe_approvals,
        "overblocks": summary.overblocks,
        "strongest_habit": summary.strongest_habit,
        "weakest_risk_area": summary.weakest_risk_area,
        "share_text": summary.share_text,
    }


__all__ = [
    "PublicGameDecision",
    "PublicGameSessionState",
    "build_public_game_session_state",
]
