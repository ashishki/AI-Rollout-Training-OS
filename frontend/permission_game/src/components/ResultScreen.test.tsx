import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ResultScreen } from "./ResultScreen";

describe("ResultScreen", () => {
  it("renders final score, status, hotspots, habits, badges, and share text", () => {
    render(
      <ResultScreen
        result={{
          score: 82,
          title: "Least Privilege Operator",
          demoResult: "Demo-ready practice run",
          prodStatus: "Not production evidence",
          unsafeApprovals: 0,
          overblocks: 1,
          strongestHabit: "scoped access",
          weakestRiskArea: "eval_bypass",
          badges: ["least_privilege_operator", "eval_gate_preserved"],
        }}
      />
    );

    expect(screen.getByLabelText("Final report")).toBeVisible();
    expect(screen.getByText("82/100")).toBeVisible();
    expect(screen.getByText("Least Privilege Operator")).toBeVisible();
    expect(screen.getByText("Demo-ready practice run")).toBeVisible();
    expect(screen.getAllByText("Not production evidence")).toHaveLength(2);
    expect(screen.getByText("0")).toBeVisible();
    expect(screen.getByText("1")).toBeVisible();
    expect(screen.getByText("scoped access")).toBeVisible();
    expect(screen.getByText("eval_bypass")).toBeVisible();
    expect(screen.getByText("practice eval bypass boundaries")).toBeVisible();
    expect(screen.getByLabelText("Final badges")).toHaveTextContent(
      "least privilege operator"
    );
    expect(screen.getByLabelText("Share text")).toHaveValue(
      "Ship It? Y/N score: 82/100 | Title: Least Privilege Operator | Unsafe approvals: 0 | Overblocks: 1 | Strongest habit: scoped access | Next habit: practice eval bypass boundaries"
    );
  });
});
