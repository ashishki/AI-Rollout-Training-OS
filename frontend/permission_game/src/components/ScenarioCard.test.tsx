import { render, screen } from "@testing-library/react";

import scenarios from "../data/shipItYnScenarios.json";
import type { PermissionGameScenario } from "../game/scenarioTypes";
import { ScenarioCard } from "./ScenarioCard";

const typedScenarios = scenarios as PermissionGameScenario[];

describe("ScenarioCard", () => {
  it("displays agent request, tool metadata, context, risk, and progress", () => {
    render(<ScenarioCard scenario={typedScenarios[0]} totalLevels={7} />);

    expect(screen.getByLabelText("Scenario card")).toBeVisible();
    expect(screen.getByText("Level 1 / 7")).toBeVisible();
    expect(screen.getByText("PatchPilot")).toBeVisible();
    expect(screen.getByText(/Approve cleanup across the project/)).toBeVisible();
    expect(screen.getByText("filesystem_change")).toBeVisible();
    expect(screen.getByText("unscoped_cleanup")).toBeVisible();
    expect(screen.getByText("delete")).toBeVisible();
    expect(screen.getByText("destructive_filesystem")).toBeVisible();
    expect(screen.getByText("proposed cleanup")).toBeVisible();
    expect(screen.getByText(/SIMULATED cleanup preview/)).toBeVisible();
  });
});
