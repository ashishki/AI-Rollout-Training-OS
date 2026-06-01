import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import type { GameChoiceId } from "../game/scenarioTypes";
import { DecisionButtons } from "./DecisionButtons";

const allChoices: GameChoiceId[] = [
  "approve",
  "deny",
  "inspect_diff",
  "run_in_sandbox",
  "require_eval",
  "restrict_scope",
  "escalate_reviewer",
  "rollback",
];

describe("DecisionButtons", () => {
  it("supports mouse activation for every available decision", () => {
    const onDecision = vi.fn();

    render(<DecisionButtons choices={allChoices} onDecision={onDecision} />);

    for (const label of [
      "Разрешить",
      "Запретить",
      "Проверить",
      "Песочница",
      "Запросить доказательства",
      "Сузить область",
      "Эскалировать",
      "Откатить",
    ]) {
      fireEvent.click(screen.getByRole("button", { name: new RegExp(label) }));
    }

    expect(onDecision).toHaveBeenCalledTimes(8);
    expect(onDecision).toHaveBeenLastCalledWith("rollback");
  });

  it("supports keyboard shortcuts for available decisions", () => {
    const onDecision = vi.fn();

    render(<DecisionButtons choices={allChoices} onDecision={onDecision} />);
    const controls = screen.getByLabelText("Кнопки решения");
    controls.focus();

    for (const key of "adisecrb") {
      fireEvent.keyDown(controls, { key });
    }

    expect(onDecision.mock.calls.map(([choice]) => choice)).toEqual(allChoices);
  });
});
