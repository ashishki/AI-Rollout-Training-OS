import type { PermissionGameScenario } from "../game/scenarioTypes";

type ScenarioCardProps = {
  scenario: PermissionGameScenario;
  totalLevels: number;
};

export function ScenarioCard({ scenario, totalLevels }: ScenarioCardProps) {
  return (
    <article aria-label="Scenario card" className="scenario-card">
      <div className="terminal-region-header">
        <span>
          Level {scenario.level} / {totalLevels}
        </span>
        <span>{scenario.permissionBoundary}</span>
      </div>
      <p className="mt-4 text-sm font-semibold text-terminal-action">
        {scenario.agentName}
      </p>
      <h1 className="mt-2 text-2xl font-semibold leading-tight">{scenario.title}</h1>
      <p className="mt-4 text-sm leading-6 text-terminal-text">
        {scenario.agentMessage}
      </p>

      <dl className="mt-5 grid gap-3 sm:grid-cols-2">
        <Metadata label="Tool" value={scenario.toolCall.type} />
        <Metadata label="Surface" value={scenario.toolCall.surface} />
        <Metadata label="Scope" value={scenario.toolCall.scope} />
        <Metadata label="Request" value={scenario.toolCall.permissionRequest} />
        <Metadata label="Risk" value={scenario.riskCategory} />
        <Metadata label="Boundary" value={scenario.permissionBoundary} />
      </dl>

      <div className="mt-5 space-y-3">
        {scenario.context.map((item) => (
          <section key={`${item.type}-${item.label}`} className="scenario-context">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-sm font-semibold">{item.label}</h2>
              <span className="scenario-context-trust">
                {item.trusted ? "trusted" : "untrusted"}
              </span>
            </div>
            <p className="mt-2 text-sm leading-6 text-terminal-muted">
              {item.content}
            </p>
          </section>
        ))}
      </div>
    </article>
  );
}

function Metadata({ label, value }: { label: string; value: string }) {
  return (
    <div className="scenario-metadata">
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}
