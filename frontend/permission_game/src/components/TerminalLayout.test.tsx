import { render, screen } from "@testing-library/react";

import scenarios from "../data/shipItYnScenarios.json";
import type { PermissionGameScenarioSummary } from "../game/scenarioTypes";
import { TerminalLayout } from "./TerminalLayout";

const typedScenarios = scenarios as PermissionGameScenarioSummary[];

describe("TerminalLayout", () => {
  it("renders stable desktop regions and mobile-friendly controls", () => {
    render(<TerminalLayout scenarios={typedScenarios} />);

    expect(screen.getByLabelText("Decision history")).toBeVisible();
    expect(screen.getByLabelText("Active scenario")).toBeVisible();
    expect(screen.getByLabelText("Risk meters and audit trail")).toBeVisible();
    expect(screen.getByRole("button", { name: "Inspect Diff" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Run Sandbox" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Restrict Scope" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Escalate" })).toBeVisible();
    expect(screen.getByLabelText("Ship It? Y/N terminal layout")).toHaveClass(
      "lg:grid-cols-[minmax(15rem,0.8fr)_minmax(22rem,1.4fr)_minmax(16rem,0.9fr)]"
    );
  });
});
