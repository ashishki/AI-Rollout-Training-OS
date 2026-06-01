import type { GameInspectArtifact, RiskCategory } from "../game/scenarioTypes";

type DiffPreviewProps = {
  open: boolean;
  artifacts: GameInspectArtifact[];
  riskCategory: RiskCategory;
  onClose: () => void;
};

export function DiffPreview({
  open,
  artifacts,
  riskCategory,
  onClose,
}: DiffPreviewProps) {
  if (!open) {
    return null;
  }

  return (
    <aside
      aria-label="Панель проверки"
      aria-modal="false"
      className="diff-preview-drawer"
      role="dialog"
    >
      <div className="terminal-region-header">
        <span>проверка</span>
        <button className="diff-preview-close" onClick={onClose} type="button">
          Закрыть
        </button>
      </div>
      <div className="risk-reveal" data-risk-category={riskCategory}>
        Найден скрытый риск: {riskCategory}
      </div>
      <div className="mt-4 space-y-3">
        {artifacts.map((artifact) => (
          <article className="diff-preview-artifact" key={artifact.id}>
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-sm font-semibold">{artifact.label}</h2>
              <span>{artifact.kind}</span>
            </div>
            <pre>{artifact.content}</pre>
          </article>
        ))}
      </div>
    </aside>
  );
}
