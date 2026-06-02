import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";

type MissionTrackProps = {
  activeIndex: number;
  completedCount: number;
  scenarios: PermissionGameScenarioSummary[];
};

export function MissionTrack({
  activeIndex,
  completedCount,
  scenarios,
}: MissionTrackProps) {
  return (
    <section aria-label="Карта миссий" className="mission-track">
      <div className="terminal-region-header">
        <span>карта</span>
        <span>
          {activeIndex + 1} / {scenarios.length}
        </span>
      </div>
      <ol className="mission-node-list">
        {scenarios.map((scenario, index) => {
          const state =
            index < completedCount
              ? "complete"
              : index === activeIndex
                ? "active"
                : "locked";
          return (
            <li className="mission-node" data-state={state} key={scenario.id}>
              <span className="mission-node-pip" aria-hidden="true" />
              <span className="mission-node-title">{scenario.title}</span>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
