import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";

type TerminalLogProps = {
  activeIndex: number;
  completedCount: number;
  scenarios: PermissionGameScenarioSummary[];
};

export function TerminalLog({
  activeIndex,
  completedCount,
  scenarios,
}: TerminalLogProps) {
  return (
    <section aria-label="История решений" className="terminal-region">
      <div className="terminal-region-header">
        <span>история</span>
        <span>{scenarios.length} уров.</span>
      </div>
      <ol className="mt-4 space-y-3">
        {scenarios.slice(0, 4).map((scenario, index) => (
          <li
            key={scenario.id}
            className="terminal-log-row"
            data-state={
              index < completedCount
                ? "complete"
                : index === activeIndex
                  ? "active"
                  : "queued"
            }
          >
            <span className="terminal-log-index">
              {String(scenario.level).padStart(2, "0")}
            </span>
            <span className="min-w-0 truncate">{scenario.title}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}
