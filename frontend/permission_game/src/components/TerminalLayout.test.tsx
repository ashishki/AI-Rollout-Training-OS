import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import { ROLE_PACKS } from "../game/rolePacks";
import { TerminalLayout } from "./TerminalLayout";

const managerRole = ROLE_PACKS[0];

describe("TerminalLayout", () => {
  it("renders stable desktop regions and mobile-friendly controls", () => {
    render(
      <TerminalLayout
        onChangeRole={vi.fn()}
        role={managerRole}
        scenarios={managerRole.scenarios}
      />
    );

    expect(screen.getByLabelText("История решений")).toBeVisible();
    expect(screen.getByLabelText("Активный сценарий")).toBeVisible();
    expect(screen.getByLabelText("Риск-метры и аудит")).toBeVisible();
    expect(screen.getByRole("button", { name: /Проверить/ })).toBeVisible();
    expect(screen.getByRole("button", { name: /Сузить область/ })).toBeVisible();
    expect(screen.getByRole("button", { name: /Эскалировать/ })).toBeVisible();
    expect(screen.getByLabelText("Ship It? Y/N игровое поле")).toHaveClass(
      "lg:grid-cols-[minmax(15rem,0.8fr)_minmax(22rem,1.4fr)_minmax(16rem,0.9fr)]"
    );
  });
});
