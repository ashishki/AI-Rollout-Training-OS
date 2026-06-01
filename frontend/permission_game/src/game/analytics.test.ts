import { describe, expect, it } from "vitest";
import {
  ANALYTICS_STORAGE_KEY,
  recordAnalyticsDecision,
  safeAnalyticsKey,
  startAnalyticsSession,
} from "./analytics";

class MemoryStorage {
  private values = new Map<string, string>();

  getItem(key: string) {
    return this.values.get(key) ?? null;
  }

  setItem(key: string, value: string) {
    this.values.set(key, value);
  }
}

describe("local analytics", () => {
  it("stores only aggregate local session fields", () => {
    const storage = new MemoryStorage();

    startAnalyticsSession(storage);
    const snapshot = recordAnalyticsDecision(storage, {
      riskCategory: "eval_bypass",
      outcome: "unsafe",
      elapsedMs: 12_500,
      inspectedArtifactCount: 2,
      finalScore: 84,
    });

    expect(snapshot.sessionsStarted).toBe(1);
    expect(snapshot.decisions).toBe(1);
    expect(snapshot.riskCategoryOutcomes.eval_bypass.unsafe).toBe(1);
    expect(snapshot.timeToDecisionBuckets.under_30s).toBe(1);
    expect(snapshot.inspectedArtifactCounts.multiple).toBe(1);
    expect(snapshot.finalScores).toEqual([84]);

    const serialized = storage.getItem(ANALYTICS_STORAGE_KEY) ?? "";
    for (const forbidden of [
      "actor_id",
      "workspace_id",
      "learner",
      "email",
      "raw_prompt",
      "credential",
      "customer",
      "scenario_id",
      "selected_decision",
    ]) {
      expect(serialized).not.toContain(forbidden);
    }
  });

  it("redacts unsafe analytics labels", () => {
    expect(safeAnalyticsKey("customer alice@example.com API_KEY=sk-live")).toBe(
      "redacted_risk"
    );
  });

  it("does not fail gameplay when browser storage is unavailable", () => {
    const blockedStorage = {
      getItem() {
        throw new Error("storage unavailable");
      },
      setItem() {
        throw new Error("storage unavailable");
      },
    };

    expect(() => startAnalyticsSession(blockedStorage)).not.toThrow();
    expect(() =>
      recordAnalyticsDecision(blockedStorage, {
        riskCategory: "tool_scope",
        outcome: "correct",
        elapsedMs: 2_000,
        inspectedArtifactCount: 1,
      })
    ).not.toThrow();
  });
});
