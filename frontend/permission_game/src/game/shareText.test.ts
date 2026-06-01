import { describe, expect, it, vi } from "vitest";

import { buildShareText, copyShareText } from "./shareText";

describe("shareText", () => {
  it("contains no personal data and can be copied from the browser", async () => {
    const shareText = buildShareText({
      score: 82,
      title: "Least Privilege Operator",
      unsafeApprovals: 0,
      overblocks: 1,
      strongestHabit: "scoped access",
      weakestRiskArea: "eval_bypass",
    });
    const clipboard = { writeText: vi.fn().mockResolvedValue(undefined) };

    await copyShareText(`${shareText} user_id=123 token=secret`, clipboard);

    expect(shareText).toContain("Ship It? Y/N счёт: 82/100");
    expect(shareText).toContain(
      "Следующая привычка: потренировать границы: eval bypass"
    );
    expect(shareText).not.toMatch(/user_id|token|secret|@/);
    expect(clipboard.writeText).toHaveBeenCalledWith(
      expect.not.stringMatching(/user_id|token|secret|@/)
    );
  });
});
