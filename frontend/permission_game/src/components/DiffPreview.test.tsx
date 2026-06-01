import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import scenarios from "../data/shipItYnScenarios.json";
import type { PermissionGameScenario } from "../game/scenarioTypes";
import { DiffPreview } from "./DiffPreview";

const typedScenarios = scenarios as PermissionGameScenario[];

describe("DiffPreview", () => {
  it("opens an accessible drawer with artifacts and highlighted risk", () => {
    const scenario = typedScenarios[0];
    const onClose = vi.fn();

    render(
      <DiffPreview
        artifacts={scenario.inspectArtifacts}
        onClose={onClose}
        open
        riskCategory={scenario.riskCategory}
      />
    );

    expect(screen.getByRole("dialog", { name: "Inspect drawer" })).toBeVisible();
    expect(screen.getByText("Cleanup preview")).toBeVisible();
    expect(screen.getByText(/migration backup directory/)).toBeVisible();
    expect(
      screen.getByText("Hidden risk revealed: destructive_filesystem")
    ).toHaveAttribute("data-risk-category", "destructive_filesystem");

    fireEvent.click(screen.getByRole("button", { name: "Close" }));

    expect(onClose).toHaveBeenCalledOnce();
  });
});
