import { buildShareText, recommendedNextHabit } from "../game/shareText";
import { useState } from "react";
import { copyShareText } from "../game/shareText";

export type FinalResult = {
  score: number;
  title: string;
  demoResult: string;
  prodStatus: string;
  unsafeApprovals: number;
  overblocks: number;
  strongestHabit: string;
  weakestRiskArea: string;
  badges: string[];
};

type ResultScreenProps = {
  result: FinalResult;
};

export function ResultScreen({ result }: ResultScreenProps) {
  const shareText = buildShareText(result);
  const [copyStatus, setCopyStatus] = useState("Готово к копированию");

  async function handleCopy() {
    await copyShareText(shareText);
    setCopyStatus("Скопировано");
  }

  return (
    <section aria-label="Итоговый отчёт" className="result-screen">
      <div className="terminal-region-header">
        <span>итог</span>
        <span>{result.prodStatus}</span>
      </div>
      <h1>{result.title}</h1>
      <p className="result-score">{result.score}/100</p>
      <dl className="result-grid">
        <ResultMetric label="Результат" value={result.demoResult} />
        <ResultMetric label="Статус" value={result.prodStatus} />
        <ResultMetric label="Рискованные разрешения" value={result.unsafeApprovals} />
        <ResultMetric label="Лишние запреты" value={result.overblocks} />
        <ResultMetric label="Сильная привычка" value={result.strongestHabit} />
        <ResultMetric label="Слабая зона" value={result.weakestRiskArea} />
        <ResultMetric
          label="Следующая привычка"
          value={recommendedNextHabit(result.weakestRiskArea)}
        />
      </dl>
      <div className="result-badges" aria-label="Итоговые бейджи">
        {result.badges.map((badge) => (
          <span key={badge}>{formatBadge(badge)}</span>
        ))}
      </div>
      <div className="result-share-actions">
        <button onClick={handleCopy} type="button">
          Скопировать итог
        </button>
        <span aria-live="polite">{copyStatus}</span>
      </div>
      <textarea aria-label="Текст для отправки" readOnly value={shareText} />
    </section>
  );
}

function ResultMetric({ label, value }: { label: string; value: number | string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

const BADGE_LABELS: Record<string, string> = {
  clean_approval_trail: "Чистый след решений",
  data_minimizer: "Минимум данных",
  eval_gate_preserved: "Eval сохранён",
  least_privilege_manager: "Минимум прав",
  least_privilege_operator: "Минимум прав",
  pressure_resisted: "Давление выдержано",
  safe_yes: "Безопасное да",
  scope_before_delete: "Сначала область",
};

function formatBadge(badge: string) {
  if (BADGE_LABELS[badge]) {
    return BADGE_LABELS[badge];
  }
  return badge
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}
