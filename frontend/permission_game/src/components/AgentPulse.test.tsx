import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ROLE_PACKS } from "../game/rolePacks";
import { AgentPulse } from "./AgentPulse";

describe("AgentPulse", () => {
  it("shows role, risk tone, decision status, and inspected artifact count", () => {
    render(
      <AgentPulse
        inspectedArtifactCount={2}
        riskCategory="log_exposure"
        role={ROLE_PACKS[0]}
        selectedDecisionLabel="сузить область"
      />
    );

    expect(screen.getByLabelText("Пульс агента")).toHaveAttribute(
      "data-tone",
      "data"
    );
    expect(screen.getByText("Менеджер")).toBeVisible();
    expect(screen.getByText("выбрано: сузить область")).toBeVisible();
    expect(screen.getByText("данные")).toBeVisible();
    expect(screen.getByText("2")).toBeVisible();
  });
});
