import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ROLE_PACKS } from "../game/rolePacks";
import { ConsequencePanel } from "./ConsequencePanel";

const managerScenario = ROLE_PACKS[0].scenarios[0];

describe("ConsequencePanel", () => {
  it("renders consequence, lesson, safer alternative, and badge feedback", () => {
    const scenario = managerScenario;

    render(
      <ConsequencePanel
        badges={scenario.badges ?? []}
        feedback={scenario.feedback?.restrict_scope}
        selectedChoice="restrict_scope"
      />
    );

    expect(screen.getByLabelText("Панель последствий")).toHaveAttribute(
      "data-outcome",
      "correct"
    );
    const panel = screen.getByLabelText("Панель последствий");
    expect(panel).toHaveTextContent(
      /исход\s*точно\s*Хорошее решение.*Очки: \+15.*Сильное разрешение.*Безопаснее/s
    );
    expect(screen.getByLabelText("Получен бейдж")).toHaveTextContent("Минимум данных");
  });

  it("shows a stable empty state before a decision", () => {
    render(<ConsequencePanel badges={[]} selectedChoice={null} />);

    expect(screen.getByText("Выберите решение, чтобы увидеть результат.")).toBeVisible();
  });
});
