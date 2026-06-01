import { TerminalLog } from "./TerminalLog";
import { DecisionButtons } from "./DecisionButtons";
import { DiffPreview } from "./DiffPreview";
import { ScenarioCard } from "./ScenarioCard";
import { useState } from "react";
import type { GameChoiceId } from "../game/scenarioTypes";
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
  const [selectedDecision, setSelectedDecision] = useState<string | null>(null);
  const [isInspectOpen, setIsInspectOpen] = useState(false);
  const [inspectedArtifactIds, setInspectedArtifactIds] = useState<string[]>([]);

  function handleDecision(choice: GameChoiceId) {
    setSelectedDecision(choice);
    if (choice === "inspect_diff") {
      setIsInspectOpen(true);
      setInspectedArtifactIds(
        activeScenario.inspectArtifacts.map((artifact) => artifact.id)
      );
    }
  }

  return (
    <main className="min-h-screen bg-terminal-bg text-terminal-text">
      <div
        aria-label="Ship It? Y/N terminal layout"
        className="mx-auto grid min-h-screen max-w-7xl gap-4 px-4 py-4 md:px-6 lg:grid-cols-[minmax(15rem,0.8fr)_minmax(22rem,1.4fr)_minmax(16rem,0.9fr)]"
      >
        <TerminalLog scenarios={scenarios} />

        <section aria-label="Active scenario" className="terminal-region">
          <ScenarioCard scenario={activeScenario} totalLevels={scenarios.length} />
          <DecisionButtons
            choices={activeScenario.choices}
            onDecision={handleDecision}
          />
          <DiffPreview
            artifacts={activeScenario.inspectArtifacts}
            onClose={() => setIsInspectOpen(false)}
            open={isInspectOpen}
            riskCategory={activeScenario.riskCategory}
          />
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
              {selectedDecision
                ? `Selected decision: ${selectedDecision}`
                : "Scenario loaded. Awaiting first decision."}
            </p>
            {inspectedArtifactIds.length > 0 ? (
              <p className="mt-2 text-sm text-terminal-muted">
                Inspected: {inspectedArtifactIds.join(", ")}
              </p>
            ) : null}
          </div>
        </aside>
      </div>
    </main>
  );
}
