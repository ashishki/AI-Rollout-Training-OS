import { render, screen } from "@testing-library/react";

import App from "./App";
import scenarios from "./data/shipItYnScenarios.json";

describe("Ship It? Y/N app scaffold", () => {
  it("renders a nonblank root with typed scenario data", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: "Ship It? Y/N" })).toBeVisible();
    expect(screen.getByText("Tiny Cleanup")).toBeVisible();
    expect(screen.getByText("7")).toBeVisible();
    expect(scenarios).toHaveLength(7);
  });
});
