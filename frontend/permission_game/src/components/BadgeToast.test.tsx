import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { BadgeToast } from "./BadgeToast";

describe("BadgeToast", () => {
  it("is subtle, deterministic, dismissible, and outside action controls", () => {
    const onDismiss = vi.fn();

    render(
      <BadgeToast
        badges={["scope_before_delete"]}
        onDismiss={onDismiss}
        visible
      />
    );

    const toast = screen.getByLabelText("Badge earned");
    expect(toast).toHaveClass("badge-toast");
    expect(toast).toHaveTextContent("Scope Before Delete");
    expect(screen.queryByLabelText("Decision controls")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Dismiss" }));

    expect(onDismiss).toHaveBeenCalledOnce();
  });
});
