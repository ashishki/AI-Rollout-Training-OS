import { TerminalLog } from "./TerminalLog";
import { DecisionButtons } from "./DecisionButtons";
import { DiffPreview } from "./DiffPreview";
import { AuditTrail, type AuditTrailEvent } from "./AuditTrail";
import { ConsequencePanel } from "./ConsequencePanel";
import { ResultScreen } from "./ResultScreen";
import { RiskMeters, type RiskMeterValues } from "./RiskMeters";
import { ScenarioCard } from "./ScenarioCard";
import { AgentPulse } from "./AgentPulse";
import { MissionTrack } from "./MissionTrack";
import { useEffect, useState } from "react";
import {
  recordAnalyticsDecision,
  startAnalyticsSession,
} from "../game/analytics";
import type { GameChoiceId, GameRolePack } from "../game/scenarioTypes";
import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";

type TerminalLayoutProps = {
  role: GameRolePack;
  scenarios: PermissionGameScenarioSummary[];
  onChangeRole: () => void;
};

const initialMeterValues: RiskMeterValues = {
  velocity: 42,
  blastRadius: 18,
  trust: 50,
  evalConfidence: 64,
  auditTrail: 51,
};

const CHOICE_LABELS: Record<GameChoiceId, string> = {
  approve: "разрешить",
  deny: "запретить",
  inspect_diff: "проверить",
  run_in_sandbox: "песочница",
  require_eval: "запросить доказательства",
  restrict_scope: "сузить область",
  escalate_reviewer: "эскалировать",
  rollback: "откатить",
};

export function TerminalLayout({
  onChangeRole,
  role,
  scenarios,
}: TerminalLayoutProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [completedDecisions, setCompletedDecisions] = useState<GameChoiceId[]>([]);
  const [showFinalReport, setShowFinalReport] = useState(false);
  const activeScenario = scenarios[activeIndex];
  const [scenarioStartedAt, setScenarioStartedAt] = useState(() => Date.now());
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
      label: "Сценарий открыт",
      detail: activeScenario.id,
    },
    ...(selectedDecision
      ? [
          {
            id: "decision-selected",
            label: `Выбрано: ${CHOICE_LABELS[selectedDecision]}`,
            detail:
              auditTrailQuality === "inspected"
                ? `Проверено артефактов: ${inspectedArtifactIds.length}`
                : "Решение записано до проверки",
          },
        ]
      : []),
  ];

  useEffect(() => {
    const storage = analyticsStorage();
    if (storage) {
      startAnalyticsSession(storage);
    }
  }, []);

  useEffect(() => {
    resetRun();
  }, [role.id]);

  function handleDecision(choice: GameChoiceId) {
    if (choice === "inspect_diff") {
      setIsInspectOpen(true);
      setInspectedArtifactIds(
        activeScenario.inspectArtifacts.map((artifact) => artifact.id)
      );
      return;
    }
    setSelectedDecision(choice);
  }

  function advanceLevel() {
    if (!selectedDecision) {
      return;
    }
    const isFinalLevel = activeIndex === scenarios.length - 1;
    const completedDecisionCount = completedDecisions.length + 1;
    const feedback =
      activeScenario.feedback?.[selectedDecision] ?? fallbackFeedback(selectedDecision);
    const storage = analyticsStorage();
    if (storage) {
      recordAnalyticsDecision(storage, {
        riskCategory: activeScenario.riskCategory,
        outcome: feedback.outcome,
        elapsedMs: Date.now() - scenarioStartedAt,
        inspectedArtifactCount: inspectedArtifactIds.length,
        finalScore: isFinalLevel
          ? Math.min(completedDecisionCount * 12, 100)
          : undefined,
      });
    }
    setCompletedDecisions((current) => [...current, selectedDecision]);
    setSelectedDecision(null);
    setIsInspectOpen(false);
    setInspectedArtifactIds([]);
    if (isFinalLevel) {
      setShowFinalReport(true);
      return;
    }
    setActiveIndex((current) => current + 1);
    setScenarioStartedAt(Date.now());
  }

  function resetRun() {
    setActiveIndex(0);
    setScenarioStartedAt(Date.now());
    setCompletedDecisions([]);
    setShowFinalReport(false);
    setSelectedDecision(null);
    setIsInspectOpen(false);
    setInspectedArtifactIds([]);
  }

  if (showFinalReport) {
    return (
      <main className="min-h-screen bg-terminal-bg p-4 text-terminal-text">
        <div className="mx-auto max-w-4xl">
          <ResultScreen
            result={{
              score: Math.min(completedDecisions.length * 12, 100),
              title: "Спокойный ревьюер разрешений",
              demoResult: `${role.label}: демо завершено`,
              prodStatus: "Не доказательство для продакшна",
              unsafeApprovals: completedDecisions.filter(
                (decision) => decision === "approve"
              ).length,
              overblocks: completedDecisions.filter((decision) => decision === "deny")
                .length,
              strongestHabit: completedDecisions.includes("restrict_scope")
                ? "узкая область"
                : "внимание к следу проверки",
              weakestRiskArea: "none",
              badges: ["clean_approval_trail"],
            }}
          />
          <button className="terminal-reset-button mt-4" onClick={resetRun} type="button">
            Играть заново
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="permission-game-shell min-h-screen bg-terminal-bg text-terminal-text">
      <div
        aria-label="Ship It? Y/N игровое поле"
        className="mx-auto grid min-h-screen max-w-7xl gap-4 px-4 py-4 md:px-6 lg:grid-cols-[minmax(15rem,0.8fr)_minmax(22rem,1.4fr)_minmax(16rem,0.9fr)]"
      >
        <header className="game-editorial-header lg:col-span-3">
          <span>{role.label}</span>
          <h1>{activeScenario.title}</h1>
          <p>{activeScenario.agentMessage}</p>
        </header>

        <TerminalLog
          activeIndex={activeIndex}
          completedCount={completedDecisions.length}
          scenarios={scenarios}
        />

        <section aria-label="Активный сценарий" className="terminal-region">
          <div className="game-mode-strip">
            <span>{role.shortLabel}</span>
            <p>{role.promise}</p>
          </div>
          <MissionTrack
            activeIndex={activeIndex}
            completedCount={completedDecisions.length}
            scenarios={scenarios}
          />
          <ScenarioCard scenario={activeScenario} totalLevels={scenarios.length} />
          <DecisionButtons
            choices={activeScenario.choices}
            onDecision={handleDecision}
          />
          <ConsequencePanel
            badges={activeScenario.badges ?? []}
            feedback={
              selectedDecision
                ? activeScenario.feedback?.[selectedDecision] ??
                  fallbackFeedback(selectedDecision)
                : undefined
            }
            selectedChoice={selectedDecision}
          />
          {selectedDecision ? (
            <button className="next-level-button" onClick={advanceLevel} type="button">
              {activeIndex === scenarios.length - 1 ? "Показать итог" : "Следующий уровень"}
            </button>
          ) : null}
          <DiffPreview
            artifacts={activeScenario.inspectArtifacts}
            onClose={() => setIsInspectOpen(false)}
            open={isInspectOpen}
            riskCategory={activeScenario.riskCategory}
          />
        </section>

        <aside aria-label="Риск-метры и аудит" className="terminal-region">
          <div className="terminal-region-header">
            <span>метры</span>
            <div className="terminal-header-actions">
              <button className="terminal-reset-button" onClick={resetRun} type="button">
                Заново
              </button>
              <button className="terminal-reset-button" onClick={onChangeRole} type="button">
                Сменить роль
              </button>
            </div>
          </div>
          <AgentPulse
            inspectedArtifactCount={inspectedArtifactIds.length}
            riskCategory={activeScenario.riskCategory}
            role={role}
            selectedDecisionLabel={
              selectedDecision ? CHOICE_LABELS[selectedDecision] : null
            }
          />
          <RiskMeters values={meterValues} />
          <AuditTrail
            auditTrailQuality={auditTrailQuality}
            events={auditEvents}
          />
          <ResultScreen
            result={{
              score: selectedDecision ? 15 : 0,
              title: selectedDecision ? "Решение принято" : "Тренировка",
              demoResult: "Локальное демо",
              prodStatus: "Не доказательство для продакшна",
              unsafeApprovals: 0,
              overblocks: 0,
              strongestHabit:
                auditTrailQuality === "inspected"
                  ? "сначала доказательства"
                  : "внимание к следу проверки",
              weakestRiskArea: activeScenario.riskCategory,
              badges: activeScenario.badges ?? [],
            }}
          />
        </aside>
      </div>
    </main>
  );
}

function fallbackFeedback(choice: GameChoiceId) {
  return {
    outcome: "partial" as const,
    scoreDelta: 5,
    consequence: `Решение записано: ${CHOICE_LABELS[choice]}`,
    lesson: "Демо сохраняет решение для итогового отчёта.",
    saferAlternative: "Проверить контекст, сузить область и оставить след проверки.",
  };
}

function analyticsStorage() {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage;
}
