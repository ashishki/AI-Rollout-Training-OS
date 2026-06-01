import { readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

const styles = readFileSync("src/styles.css", "utf-8");

describe("accessibility CSS", () => {
  it("respects reduced motion and preserves visible focus states", () => {
    expect(styles).toContain("@media (prefers-reduced-motion: reduce)");
    expect(styles).toContain("@media (prefers-reduced-motion: no-preference)");
    expect(styles).toContain("animation-duration: 0.01ms !important");
    expect(styles).toContain("transition-duration: 0.01ms !important");
    expect(styles).toContain("button:focus-visible");
    expect(styles).toContain("textarea:focus-visible");
    expect(styles).toContain("outline: 2px solid #5aa7ff");
  });
});
