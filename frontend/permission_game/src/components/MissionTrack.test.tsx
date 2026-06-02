import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ROLE_PACKS } from "../game/rolePacks";
import { MissionTrack } from "./MissionTrack";

const managerScenarios = ROLE_PACKS[0].scenarios;

describe("MissionTrack", () => {
  it("marks completed, active, and locked missions without changing scenario order", () => {
    const { container } = render(
      <MissionTrack
        activeIndex={1}
        completedCount={1}
        scenarios={managerScenarios}
      />
    );

    expect(screen.getByLabelText("Карта миссий")).toBeVisible();
    expect(screen.getByText("2 / 4")).toBeVisible();
    expect(screen.getAllByRole("listitem")).toHaveLength(4);
    expect(container.querySelector('[data-state="complete"]')).toHaveTextContent(
      "Все тикеты перед встречей"
    );
    expect(container.querySelector('[data-state="active"]')).toHaveTextContent(
      "Красный сигнал перед демо"
    );
    expect(container.querySelectorAll('[data-state="locked"]')).toHaveLength(2);
  });
});
