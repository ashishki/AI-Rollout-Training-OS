import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import scenarios from "../data/shipItYnScenarios.json";
import type { PermissionGameScenario } from "../game/scenarioTypes";
import { ConsequencePanel } from "./ConsequencePanel";

const typedScenarios = scenarios as PermissionGameScenario[];

describe("ConsequencePanel", () => {
  it("renders consequence, lesson, safer alternative, and badge feedback", () => {
    const scenario = typedScenarios[0];

    render(
      <ConsequencePanel
        badges={scenario.badges ?? []}
        feedback={scenario.feedback?.restrict_scope}
        selectedChoice="restrict_scope"
      />
    );

    expect(screen.getByLabelText("Consequence panel")).toHaveAttribute(
      "data-outcome",
      "correct"
    );
    const panel = screen.getByLabelText("Consequence panel");
    expect(panel).toHaveTextContent(
      /outcome\s*correct\s*Only generated cache files were removed.*Score change: \+15.*Scope turns a risky destructive request.*Safer path.*Limit cleanup to the listed/s
    );
    expect(screen.getByLabelText("Badge earned")).toHaveTextContent(
      "Scope Before Delete"
    );
  });

  it("shows a stable empty state before a decision", () => {
    render(<ConsequencePanel badges={[]} selectedChoice={null} />);

    expect(screen.getByText("Choose a decision to reveal the result.")).toBeVisible();
  });
});
