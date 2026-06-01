import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ROLE_PACKS } from "../game/rolePacks";
import { DiffPreview } from "./DiffPreview";

const managerScenario = ROLE_PACKS[0].scenarios[0];

describe("DiffPreview", () => {
  it("opens an accessible drawer with artifacts and highlighted risk", () => {
    const scenario = managerScenario;
    const onClose = vi.fn();

    render(
      <DiffPreview
        artifacts={scenario.inspectArtifacts}
        onClose={onClose}
        open
        riskCategory={scenario.riskCategory}
      />
    );

    expect(screen.getByRole("dialog", { name: "Панель проверки" })).toBeVisible();
    expect(screen.getByText("Варианты доступа")).toBeVisible();
    expect(screen.getByText(/обезличенную выборку/)).toBeVisible();
    expect(
      screen.getByText("Найден скрытый риск: log_exposure")
    ).toHaveAttribute("data-risk-category", "log_exposure");

    fireEvent.click(screen.getByRole("button", { name: "Закрыть" }));

    expect(onClose).toHaveBeenCalledOnce();
  });
});
