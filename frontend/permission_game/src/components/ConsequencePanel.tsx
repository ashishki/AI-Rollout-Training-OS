import { BadgeToast } from "./BadgeToast";
import type { GameChoiceFeedback, GameChoiceId } from "../game/scenarioTypes";

type ConsequencePanelProps = {
  selectedChoice: GameChoiceId | null;
  feedback?: GameChoiceFeedback;
  badges: string[];
};

export function ConsequencePanel({
  selectedChoice,
  feedback,
  badges,
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
      <p>{feedback.lesson}</p>
      <div className="safer-alternative">
        <span>Safer path</span>
        <p>{feedback.saferAlternative}</p>
      </div>
      <BadgeToast badges={badges} visible={feedback.outcome === "correct"} />
    </section>
  );
}
