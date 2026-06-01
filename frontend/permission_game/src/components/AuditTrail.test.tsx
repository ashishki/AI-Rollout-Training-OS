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
            label: "Выбрано: разрешить",
            detail: "Запрос остановлен: password=super-secret скрыт",
          },
        ]}
      />
    );

    expect(screen.getByLabelText("След проверки")).toBeVisible();
    expect(
      screen.getByText("Пробел аудита: решение принято до проверки доказательств.")
    ).toBeVisible();
    expect(screen.getByText("Выбрано: разрешить")).toBeVisible();
    expect(screen.getByText(/Запрос остановлен: \[redacted\] скрыт/)).toBeVisible();
    expect(screen.queryByText(/super-secret/)).not.toBeInTheDocument();
  });
});
