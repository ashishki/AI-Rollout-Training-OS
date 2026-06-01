from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass

from ai_rollout_os.permissions.game_scoring import GameDecisionResult


@dataclass(frozen=True)
class TeamRiskHotspot:
    risk_area: str
    decision_count: int
    unsafe_approvals: int
    overblocks: int

    def to_public_dict(self) -> dict[str, int | str]:
        return {
            "risk_area": self.risk_area,
            "decision_count": self.decision_count,
            "unsafe_approvals": self.unsafe_approvals,
            "overblocks": self.overblocks,
        }


@dataclass(frozen=True)
class TeamGameSummary:
    total_decisions: int
    risk_hotspots: tuple[TeamRiskHotspot, ...]
    common_unsafe_approvals: tuple[str, ...]
    common_overblocks: tuple[str, ...]
    recommended_habits: tuple[str, ...]

    def to_public_dict(self) -> dict[str, object]:
        return {
            "total_decisions": self.total_decisions,
            "risk_hotspots": [
                hotspot.to_public_dict() for hotspot in self.risk_hotspots
            ],
            "common_unsafe_approvals": list(self.common_unsafe_approvals),
            "common_overblocks": list(self.common_overblocks),
            "recommended_habits": list(self.recommended_habits),
        }


def build_team_game_summary(
    decision_results: list[GameDecisionResult],
    *,
    scenario_risk_categories: Mapping[str, str] | None = None,
) -> TeamGameSummary:
    if not decision_results:
        raise ValueError("team game summary requires at least one decision")

    risk_categories = scenario_risk_categories or {}
    risk_area_by_result = [
        _safe_label(risk_categories.get(result.scenario_id, result.scenario_id))
        for result in decision_results
    ]
    hotspot_counter: Counter[str] = Counter()
    unsafe_counter: Counter[str] = Counter()
    overblock_counter: Counter[str] = Counter()

    for result, risk_area in zip(decision_results, risk_area_by_result, strict=True):
        if result.outcome != "correct":
            hotspot_counter[risk_area] += 1
        if result.outcome == "unsafe":
            unsafe_counter[risk_area] += 1
        if result.outcome == "overblock":
            overblock_counter[risk_area] += 1

    return TeamGameSummary(
        total_decisions=len(decision_results),
        risk_hotspots=tuple(
            TeamRiskHotspot(
                risk_area=risk_area,
                decision_count=count,
                unsafe_approvals=unsafe_counter[risk_area],
                overblocks=overblock_counter[risk_area],
            )
            for risk_area, count in _sorted_counts(hotspot_counter)
        ),
        common_unsafe_approvals=tuple(
            risk_area for risk_area, _count in _sorted_counts(unsafe_counter)
        ),
        common_overblocks=tuple(
            risk_area for risk_area, _count in _sorted_counts(overblock_counter)
        ),
        recommended_habits=_recommended_habits(unsafe_counter, overblock_counter),
    )


def _recommended_habits(
    unsafe_counter: Counter[str], overblock_counter: Counter[str]
) -> tuple[str, ...]:
    habits = ["review aggregate hotspots as a team"]
    if unsafe_counter:
        habits.append("inspect before broad approval")
        habits.append("require evidence before bypassing tests or evals")
    if overblock_counter:
        habits.append("state what evidence would make safe work approvable")
    return tuple(habits)


def _sorted_counts(counter: Counter[str]) -> list[tuple[str, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))


def _safe_label(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    if not normalized:
        return "unknown"
    if all(character.isalnum() or character == "_" for character in normalized):
        return normalized[:80]
    return "redacted_risk"


__all__ = [
    "TeamGameSummary",
    "TeamRiskHotspot",
    "build_team_game_summary",
]
