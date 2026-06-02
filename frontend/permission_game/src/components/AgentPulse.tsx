import type { GameRolePack, RiskCategory } from "../game/scenarioTypes";

type AgentPulseProps = {
  inspectedArtifactCount: number;
  riskCategory: RiskCategory;
  role: GameRolePack;
  selectedDecisionLabel: string | null;
};

const RISK_TONE: Partial<Record<RiskCategory, string>> = {
  destructive_filesystem: "filesystem",
  diff_misrepresentation: "diff",
  eval_bypass: "eval",
  log_exposure: "data",
  overbroad_permission: "access",
  scope_creep: "scope",
  test_deletion: "tests",
};

const TONE_LABELS: Record<string, string> = {
  access: "доступ",
  data: "данные",
  diff: "дифф",
  eval: "eval",
  filesystem: "файлы",
  scope: "область",
  signal: "сигнал",
  tests: "тесты",
};

export function AgentPulse({
  inspectedArtifactCount,
  riskCategory,
  role,
  selectedDecisionLabel,
}: AgentPulseProps) {
  const tone = RISK_TONE[riskCategory] ?? "signal";
  const status = selectedDecisionLabel
    ? `выбрано: ${selectedDecisionLabel}`
    : inspectedArtifactCount > 0
      ? "проверка открыта"
      : "ожидает решения";

  return (
    <section aria-label="Пульс агента" className="agent-pulse" data-tone={tone}>
      <div className="terminal-region-header">
        <span>пульс агента</span>
        <span>{role.shortLabel}</span>
      </div>
      <div className="agent-pulse-stage" aria-hidden="true">
        <svg className="agent-pulse-orbit" viewBox="0 0 180 180">
          <circle className="agent-pulse-ring ring-outer" cx="90" cy="90" r="76" />
          <circle className="agent-pulse-ring ring-mid" cx="90" cy="90" r="52" />
          <circle className="agent-pulse-core" cx="90" cy="90" r="24" />
          <path
            className="agent-pulse-path"
            d="M38 96c18-42 78-62 106-20 18 28-8 66-44 70-38 4-74-18-62-50Z"
          />
          <circle className="agent-pulse-dot dot-a" cx="144" cy="78" r="5" />
          <circle className="agent-pulse-dot dot-b" cx="52" cy="119" r="4" />
        </svg>
      </div>
      <dl className="agent-pulse-readout">
        <div>
          <dt>состояние</dt>
          <dd>{status}</dd>
        </div>
        <div>
          <dt>риск</dt>
          <dd>{TONE_LABELS[tone]}</dd>
        </div>
        <div>
          <dt>проверено</dt>
          <dd>{inspectedArtifactCount}</dd>
        </div>
      </dl>
    </section>
  );
}
