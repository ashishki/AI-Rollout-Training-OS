import { TerminalLog } from "./TerminalLog";
import { DecisionButtons } from "./DecisionButtons";
import { DiffPreview } from "./DiffPreview";
import { AuditTrail, type AuditTrailEvent } from "./AuditTrail";
import { ConsequencePanel } from "./ConsequencePanel";
import { RiskMeters, type RiskMeterValues } from "./RiskMeters";
import { ScenarioCard } from "./ScenarioCard";
import { useState } from "react";
import type { GameChoiceId } from "../game/scenarioTypes";
import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";

type TerminalLayoutProps = {
  scenarios: PermissionGameScenarioSummary[];
};

const initialMeterValues: RiskMeterValues = {
  velocity: 42,
  blastRadius: 18,
  trust: 50,
  evalConfidence: 64,
  auditTrail: 51,
};

export function TerminalLayout({ scenarios }: TerminalLayoutProps) {
  const activeScenario = scenarios[0];
  const [selectedDecision, setSelectedDecision] = useState<GameChoiceId | null>(
    null
  );
  const [isInspectOpen, setIsInspectOpen] = useState(false);
  const [inspectedArtifactIds, setInspectedArtifactIds] = useState<string[]>([]);
  const auditTrailQuality = inspectedArtifactIds.length > 0 ? "inspected" : "blind";
  const meterValues = selectedDecision
    ? {
        ...initialMeterValues,
        auditTrail: auditTrailQuality === "inspected" ? 68 : 39,
      }
    : initialMeterValues;
  const auditEvents: AuditTrailEvent[] = [
    {
      id: "scenario-loaded",
      label: "Scenario loaded",
      detail: activeScenario.id,
    },
    ...(selectedDecision
      ? [
          {
            id: "decision-selected",
            label: `Selected ${selectedDecision}`,
            detail:
              auditTrailQuality === "inspected"
                ? `Inspected ${inspectedArtifactIds.join(", ")}`
                : "Decision recorded before inspection",
          },
        ]
      : []),
  ];

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
          <ConsequencePanel
            badges={activeScenario.badges ?? []}
            feedback={
              selectedDecision
                ? activeScenario.feedback?.[selectedDecision]
                : undefined
            }
            selectedChoice={selectedDecision}
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
          <RiskMeters values={meterValues} />
          <AuditTrail
            auditTrailQuality={auditTrailQuality}
            events={auditEvents}
          />
        </aside>
      </div>
    </main>
  );
}
