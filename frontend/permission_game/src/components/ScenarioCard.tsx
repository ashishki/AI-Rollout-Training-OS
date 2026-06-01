import type { PermissionGameScenario } from "../game/scenarioTypes";

type ScenarioCardProps = {
  scenario: PermissionGameScenario;
  totalLevels: number;
};

export function ScenarioCard({ scenario, totalLevels }: ScenarioCardProps) {
  return (
    <article aria-label="Карточка сценария" className="scenario-card">
      <div className="terminal-region-header">
        <span>
          Уровень {scenario.level} / {totalLevels}
        </span>
        <span>{BOUNDARY_LABELS[scenario.permissionBoundary]}</span>
      </div>
      <p className="mt-4 text-sm font-semibold text-terminal-action">
        {scenario.agentName}
      </p>
      <h1 className="mt-2 text-2xl font-semibold leading-tight">{scenario.title}</h1>
      <p className="mt-4 text-sm leading-6 text-terminal-text">
        {scenario.agentMessage}
      </p>

      <dl className="mt-5 grid gap-3 sm:grid-cols-2">
        <Metadata label="Инструмент" value={scenario.toolCall.type} />
        <Metadata label="Поверхность" value={scenario.toolCall.surface} />
        <Metadata label="Область" value={scenario.toolCall.scope} />
        <Metadata label="Запрос" value={scenario.toolCall.permissionRequest} />
        <Metadata label="Риск" value={RISK_LABELS[scenario.riskCategory]} />
        <Metadata
          label="Граница"
          value={BOUNDARY_LABELS[scenario.permissionBoundary]}
        />
      </dl>

      <div className="mt-5 space-y-3">
        {scenario.context.map((item) => (
          <section key={`${item.type}-${item.label}`} className="scenario-context">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-sm font-semibold">{item.label}</h2>
              <span className="scenario-context-trust">
                {item.trusted ? "доверенный" : "внешний"}
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

const BOUNDARY_LABELS = {
  allowed: "можно",
  needs_approval: "нужно согласование",
  blocked: "заблокировать",
  unknown: "нужен контекст",
};

const RISK_LABELS = {
  secrets: "секреты",
  destructive_filesystem: "удаление файлов",
  diff_misrepresentation: "diff выглядит проще, чем есть",
  test_deletion: "удаление тестов",
  indirect_prompt_injection: "внешняя инструкция",
  overbroad_permission: "слишком широкие права",
  eval_bypass: "обход eval",
  dependency_install: "зависимость",
  ci_edit: "CI",
  network_access: "сеть",
  log_exposure: "логи и данные",
  scope_creep: "расползание области",
  context_contamination: "грязный контекст",
};
