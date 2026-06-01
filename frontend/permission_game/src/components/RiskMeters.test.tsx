import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RiskMeters, type RiskMeterValues } from "./RiskMeters";

const initialValues: RiskMeterValues = {
  velocity: 40,
  blastRadius: 20,
  trust: 55,
  evalConfidence: 60,
  auditTrail: 35,
};

describe("RiskMeters", () => {
  it("updates meter values without changing the stable row structure", () => {
    const { container, rerender } = render(<RiskMeters values={initialValues} />);

    expect(screen.getAllByRole("progressbar")).toHaveLength(5);
    expect(container.querySelectorAll(".risk-meter-row")).toHaveLength(5);
    expect(screen.getByRole("progressbar", { name: "Скорость" })).toHaveAttribute(
      "aria-valuenow",
      "40"
    );

    rerender(
      <RiskMeters
        values={{
          velocity: 52,
          blastRadius: 28,
          trust: 48,
          evalConfidence: 70,
          auditTrail: 64,
        }}
      />
    );

    expect(container.querySelectorAll(".risk-meter-row")).toHaveLength(5);
    expect(screen.getByRole("progressbar", { name: "Скорость" })).toHaveAttribute(
      "aria-valuenow",
      "52"
    );
    expect(
      screen.getByRole("progressbar", { name: "След проверки" })
    ).toHaveAttribute("aria-valuenow", "64");
  });
});
