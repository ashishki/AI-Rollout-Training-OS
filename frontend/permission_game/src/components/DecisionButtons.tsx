import type { KeyboardEvent } from "react";

import type { GameChoiceId } from "../game/scenarioTypes";

type DecisionButtonsProps = {
  choices: GameChoiceId[];
  onDecision: (choice: GameChoiceId) => void;
};

const CHOICE_CONFIG: Record<GameChoiceId, { label: string; shortcut: string }> = {
  approve: { label: "Разрешить", shortcut: "A" },
  deny: { label: "Запретить", shortcut: "D" },
  inspect_diff: { label: "Проверить", shortcut: "I" },
  run_in_sandbox: { label: "Песочница", shortcut: "S" },
  require_eval: { label: "Запросить доказательства", shortcut: "E" },
  restrict_scope: { label: "Сузить область", shortcut: "C" },
  escalate_reviewer: { label: "Эскалировать", shortcut: "R" },
  rollback: { label: "Откатить", shortcut: "B" },
};

export function DecisionButtons({ choices, onDecision }: DecisionButtonsProps) {
  function handleKeyDown(event: KeyboardEvent<HTMLElement>) {
    const selectedChoice = choices.find(
      (choice) =>
        CHOICE_CONFIG[choice].shortcut.toLowerCase() === event.key.toLowerCase()
    );
    if (!selectedChoice) {
      return;
    }

    event.preventDefault();
    onDecision(selectedChoice);
  }

  return (
    <section
      aria-label="Кнопки решения"
      className="decision-control-grid"
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {choices.map((choice) => {
        const config = CHOICE_CONFIG[choice];
        return (
          <button
            aria-keyshortcuts={config.shortcut}
            className="terminal-action-button"
            key={choice}
            onClick={() => onDecision(choice)}
            type="button"
          >
            <span>{config.label}</span>
            <kbd>{config.shortcut}</kbd>
          </button>
        );
      })}
    </section>
  );
}
