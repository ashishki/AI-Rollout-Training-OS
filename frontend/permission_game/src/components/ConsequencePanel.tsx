import { BadgeToast } from "./BadgeToast";
import type { GameChoiceFeedback, GameChoiceId } from "../game/scenarioTypes";

type ConsequencePanelProps = {
  selectedChoice: GameChoiceId | null;
  feedback?: GameChoiceFeedback;
  badges: string[];
  onDismissBadge?: () => void;
};

export function ConsequencePanel({
  selectedChoice,
  feedback,
  badges,
  onDismissBadge,
}: ConsequencePanelProps) {
  if (!selectedChoice || !feedback) {
    return (
      <section aria-label="Панель последствий" className="consequence-panel">
        <h2>Последствие</h2>
        <p>Выберите решение, чтобы увидеть результат.</p>
      </section>
    );
  }

  return (
    <section
      aria-label="Панель последствий"
      className="consequence-panel"
      data-outcome={feedback.outcome}
    >
      <div className="terminal-region-header">
        <span>исход</span>
        <span>{OUTCOME_LABELS[feedback.outcome]}</span>
      </div>
      <h2>{feedback.consequence}</h2>
      <p className="score-change">Очки: {formatScoreDelta(feedback.scoreDelta)}</p>
      <p>{feedback.lesson}</p>
      <div className="safer-alternative">
        <span>Безопаснее</span>
        <p>{feedback.saferAlternative}</p>
      </div>
      <BadgeToast
        badges={badges}
        onDismiss={onDismissBadge}
        visible={feedback.outcome === "correct"}
      />
    </section>
  );
}

function formatScoreDelta(scoreDelta: number) {
  return scoreDelta > 0 ? `+${scoreDelta}` : `${scoreDelta}`;
}

const OUTCOME_LABELS = {
  correct: "точно",
  partial: "частично",
  unsafe: "рискованно",
  overblock: "лишний запрет",
};
