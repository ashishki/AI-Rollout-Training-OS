import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AuditTrail } from "./AuditTrail";

describe("AuditTrail", () => {
  it("lists concise decision events and flags blind audit gaps safely", () => {
    render(
      <AuditTrail
        auditTrailQuality="blind"
        events={[
          {
            id: "decision-1",
            label: "Selected approve",
            detail: "Blocked broad request with password=super-secret omitted",
          },
        ]}
      />
    );

    expect(screen.getByLabelText("Audit trail")).toBeVisible();
    expect(screen.getByText("Audit gap: decision made before inspection.")).toBeVisible();
    expect(screen.getByText("Selected approve")).toBeVisible();
    expect(screen.getByText(/with \[redacted\] omitted/)).toBeVisible();
    expect(screen.queryByText(/super-secret/)).not.toBeInTheDocument();
  });
});
