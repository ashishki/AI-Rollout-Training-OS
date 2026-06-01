import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";

type TerminalLogProps = {
  scenarios: PermissionGameScenarioSummary[];
};

export function TerminalLog({ scenarios }: TerminalLogProps) {
  return (
    <section aria-label="Decision history" className="terminal-region">
      <div className="terminal-region-header">
        <span>history</span>
        <span>{scenarios.length} levels</span>
      </div>
      <ol className="mt-4 space-y-3">
        {scenarios.slice(0, 4).map((scenario) => (
          <li key={scenario.id} className="terminal-log-row">
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
