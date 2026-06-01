import { render, screen } from "@testing-library/react";

import { ROLE_PACKS } from "../game/rolePacks";
import { ScenarioCard } from "./ScenarioCard";

const managerScenario = ROLE_PACKS[0].scenarios[0];

describe("ScenarioCard", () => {
  it("displays agent request, tool metadata, context, risk, and progress", () => {
    render(<ScenarioCard scenario={managerScenario} totalLevels={4} />);

    expect(screen.getByLabelText("Карточка сценария")).toBeVisible();
    expect(screen.getByText("Уровень 1 / 4")).toBeVisible();
    expect(screen.getByText("AssistPilot")).toBeVisible();
    expect(screen.getByText(/прочитать все тикеты поддержки/)).toBeVisible();
    expect(screen.getByText("доступ к данным")).toBeVisible();
    expect(screen.getByText("все тикеты")).toBeVisible();
    expect(screen.getByText("читать")).toBeVisible();
    expect(screen.getByText("логи и данные")).toBeVisible();
    expect(screen.getByText("срочная встреча")).toBeVisible();
    expect(screen.getByText(/персональные данные/)).toBeVisible();
  });
});
