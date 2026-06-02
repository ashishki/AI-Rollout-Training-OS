import { fireEvent, render, screen } from "@testing-library/react";

import App from "./App";
import { ROLE_PACKS } from "./game/rolePacks";

describe("Ship It? Y/N app scaffold", () => {
  it("renders role selection and opens the Russian manager mode", () => {
    render(<App />);

    expect(screen.getByLabelText("Выбор роли")).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: /Менеджер/ }));

    expect(screen.getByLabelText("Ship It? Y/N игровое поле")).toBeVisible();
    expect(screen.getAllByText("Все тикеты перед встречей")).toHaveLength(3);
    expect(screen.getByLabelText("Карта миссий")).toBeVisible();
    expect(screen.getByText("4 уров.")).toBeVisible();
    expect(ROLE_PACKS).toHaveLength(3);
  });
});
