import type { GameFeedbackOutcome, RiskCategory } from "./scenarioTypes";

export const ANALYTICS_STORAGE_KEY = "ship-it-yn-analytics-v1";

export type TimeToDecisionBucket = "under_10s" | "under_30s" | "over_30s";
export type InspectedArtifactBucket = "none" | "one" | "multiple";

export type LocalAnalyticsDecision = {
  riskCategory: RiskCategory | string;
  outcome: GameFeedbackOutcome;
  elapsedMs: number;
  inspectedArtifactCount: number;
  finalScore?: number;
};

export type LocalAnalyticsSnapshot = {
  sessionsStarted: number;
  decisions: number;
  riskCategoryOutcomes: Record<string, Record<GameFeedbackOutcome, number>>;
  timeToDecisionBuckets: Record<TimeToDecisionBucket, number>;
  inspectedArtifactCounts: Record<InspectedArtifactBucket, number>;
  finalScores: number[];
};

const emptyOutcomeCounts = (): Record<GameFeedbackOutcome, number> => ({
  correct: 0,
  partial: 0,
  unsafe: 0,
  overblock: 0,
});

export function emptyAnalyticsSnapshot(): LocalAnalyticsSnapshot {
  return {
    sessionsStarted: 0,
    decisions: 0,
    riskCategoryOutcomes: {},
    timeToDecisionBuckets: {
      under_10s: 0,
      under_30s: 0,
      over_30s: 0,
    },
    inspectedArtifactCounts: {
      none: 0,
      one: 0,
      multiple: 0,
    },
    finalScores: [],
  };
}

export function startAnalyticsSession(storage: Pick<Storage, "getItem" | "setItem">) {
  const snapshot = readAnalyticsSnapshot(storage);
  const next = {
    ...snapshot,
    sessionsStarted: snapshot.sessionsStarted + 1,
  };
  writeAnalyticsSnapshot(storage, next);
  return next;
}

export function recordAnalyticsDecision(
  storage: Pick<Storage, "getItem" | "setItem">,
  decision: LocalAnalyticsDecision
) {
  const snapshot = readAnalyticsSnapshot(storage);
  const riskCategory = safeAnalyticsKey(decision.riskCategory);
  const outcomeCounts = {
    ...emptyOutcomeCounts(),
    ...(snapshot.riskCategoryOutcomes[riskCategory] ?? {}),
  };
  const elapsedBucket = timeToDecisionBucket(decision.elapsedMs);
  const artifactBucket = inspectedArtifactBucket(decision.inspectedArtifactCount);
  outcomeCounts[decision.outcome] += 1;

  const next = {
    ...snapshot,
    decisions: snapshot.decisions + 1,
    riskCategoryOutcomes: {
      ...snapshot.riskCategoryOutcomes,
      [riskCategory]: outcomeCounts,
    },
    timeToDecisionBuckets: {
      ...snapshot.timeToDecisionBuckets,
      [elapsedBucket]: snapshot.timeToDecisionBuckets[elapsedBucket] + 1,
    },
    inspectedArtifactCounts: {
      ...snapshot.inspectedArtifactCounts,
      [artifactBucket]: snapshot.inspectedArtifactCounts[artifactBucket] + 1,
    },
    finalScores:
      typeof decision.finalScore === "number"
        ? [...snapshot.finalScores, clampScore(decision.finalScore)]
        : snapshot.finalScores,
  };
  writeAnalyticsSnapshot(storage, next);
  return next;
}

export function readAnalyticsSnapshot(
  storage: Pick<Storage, "getItem">
): LocalAnalyticsSnapshot {
  const raw = safeGetItem(storage);
  if (!raw) {
    return emptyAnalyticsSnapshot();
  }
  try {
    const parsed = JSON.parse(raw) as Partial<LocalAnalyticsSnapshot>;
    const empty = emptyAnalyticsSnapshot();
    return {
      ...empty,
      ...parsed,
      riskCategoryOutcomes: parsed.riskCategoryOutcomes ?? {},
      timeToDecisionBuckets: {
        ...empty.timeToDecisionBuckets,
        ...parsed.timeToDecisionBuckets,
      },
      inspectedArtifactCounts: {
        ...empty.inspectedArtifactCounts,
        ...parsed.inspectedArtifactCounts,
      },
      finalScores: Array.isArray(parsed.finalScores) ? parsed.finalScores : [],
    };
  } catch {
    return emptyAnalyticsSnapshot();
  }
}

export function writeAnalyticsSnapshot(
  storage: Pick<Storage, "setItem">,
  snapshot: LocalAnalyticsSnapshot
) {
  try {
    storage.setItem(ANALYTICS_STORAGE_KEY, JSON.stringify(snapshot));
  } catch {
    return;
  }
}

export function safeAnalyticsKey(value: string) {
  const normalized = value.trim().toLowerCase().replaceAll("-", "_");
  if (!normalized) {
    return "unknown";
  }
  if ([...normalized].every((character) => /[a-z0-9_]/.test(character))) {
    return normalized.slice(0, 80);
  }
  return "redacted_risk";
}

function timeToDecisionBucket(elapsedMs: number): TimeToDecisionBucket {
  if (elapsedMs < 10_000) {
    return "under_10s";
  }
  if (elapsedMs < 30_000) {
    return "under_30s";
  }
  return "over_30s";
}

function inspectedArtifactBucket(count: number): InspectedArtifactBucket {
  if (count <= 0) {
    return "none";
  }
  if (count === 1) {
    return "one";
  }
  return "multiple";
}

function clampScore(score: number) {
  return Math.max(0, Math.min(100, Math.round(score)));
}

function safeGetItem(storage: Pick<Storage, "getItem">) {
  try {
    return storage.getItem(ANALYTICS_STORAGE_KEY);
  } catch {
    return null;
  }
}
