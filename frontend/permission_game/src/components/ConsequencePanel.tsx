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
      <section aria-label="Consequence panel" className="consequence-panel">
        <h2>Consequence</h2>
        <p>Choose a decision to reveal the result.</p>
      </section>
    );
  }

  return (
    <section
      aria-label="Consequence panel"
      className="consequence-panel"
      data-outcome={feedback.outcome}
    >
      <div className="terminal-region-header">
        <span>outcome</span>
        <span>{feedback.outcome}</span>
      </div>
      <h2>{feedback.consequence}</h2>
      <p className="score-change">Score change: {formatScoreDelta(feedback.scoreDelta)}</p>
      <p>{feedback.lesson}</p>
      <div className="safer-alternative">
        <span>Safer path</span>
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
