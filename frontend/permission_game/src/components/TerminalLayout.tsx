import { TerminalLog } from "./TerminalLog";
import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";

type TerminalLayoutProps = {
  scenarios: PermissionGameScenarioSummary[];
};

const meterRows = [
  ["Velocity", "42", "terminal-meter-fill-safe"],
  ["Blast radius", "18", "terminal-meter-fill-risk"],
  ["Eval confidence", "64", "terminal-meter-fill-action"],
  ["Audit trail", "51", "terminal-meter-fill-warn"],
] as const;

export function TerminalLayout({ scenarios }: TerminalLayoutProps) {
  const activeScenario = scenarios[0];

  return (
    <main className="min-h-screen bg-terminal-bg text-terminal-text">
      <div
        aria-label="Ship It? Y/N terminal layout"
        className="mx-auto grid min-h-screen max-w-7xl gap-4 px-4 py-4 md:px-6 lg:grid-cols-[minmax(15rem,0.8fr)_minmax(22rem,1.4fr)_minmax(16rem,0.9fr)]"
      >
        <TerminalLog scenarios={scenarios} />

        <section aria-label="Active scenario" className="terminal-region">
          <div className="terminal-region-header">
            <span>active request</span>
            <span>level {activeScenario.level}</span>
          </div>
          <div className="mt-5 rounded border border-terminal-line bg-terminal-bg p-4">
            <p className="text-sm text-terminal-muted">PatchPilot requests write access</p>
            <h1 className="mt-3 text-2xl font-semibold leading-tight">
              {activeScenario.title}
            </h1>
            <p className="mt-4 text-sm leading-6 text-terminal-muted">
              Boundary: {activeScenario.permissionBoundary}. Risk:{" "}
              {activeScenario.riskCategory}.
            </p>
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <button className="terminal-action-button" type="button">
              Inspect Diff
            </button>
            <button className="terminal-action-button" type="button">
              Run Sandbox
            </button>
            <button className="terminal-action-button" type="button">
              Restrict Scope
            </button>
            <button className="terminal-action-button" type="button">
              Escalate
            </button>
          </div>
        </section>

        <aside aria-label="Risk meters and audit trail" className="terminal-region">
          <div className="terminal-region-header">
            <span>meters</span>
            <span>draft</span>
          </div>
          <div className="mt-4 space-y-4">
            {meterRows.map(([label, value, fillClass]) => (
              <div key={label}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span>{label}</span>
                  <span className="text-terminal-muted">{value}</span>
                </div>
                <div className="terminal-meter-track">
                  <span className={fillClass} style={{ width: `${value}%` }} />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 rounded border border-terminal-line bg-terminal-bg p-3">
            <h2 className="text-sm font-semibold uppercase text-terminal-muted">
              Audit Trail
            </h2>
            <p className="mt-3 text-sm leading-6">
              Scenario loaded. Awaiting first decision.
            </p>
          </div>
        </aside>
      </div>
    </main>
  );
}
