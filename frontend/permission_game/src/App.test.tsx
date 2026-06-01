import { render, screen } from "@testing-library/react";

import App from "./App";
import scenarios from "./data/shipItYnScenarios.json";

describe("Ship It? Y/N app scaffold", () => {
  it("renders a nonblank root with typed scenario data", () => {
    render(<App />);

    expect(screen.getByLabelText("Ship It? Y/N terminal layout")).toBeVisible();
    expect(screen.getAllByText("Tiny Cleanup")).toHaveLength(2);
    expect(screen.getByText("7 levels")).toBeVisible();
    expect(scenarios).toHaveLength(7);
  });
});
