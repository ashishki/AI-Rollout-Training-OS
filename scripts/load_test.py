from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Any

SCENARIOS = (
    "cohort_launch",
    "retrieval_query",
    "feedback_job",
    "reminder_scheduler",
    "report_generation",
)

BASE_LATENCY_MS = {
    "cohort_launch": 180.0,
    "retrieval_query": 75.0,
    "feedback_job": 820.0,
    "reminder_scheduler": 95.0,
    "report_generation": 140.0,
}


@dataclass(frozen=True)
class LoadTestSample:
    scenario: str
    iteration: int
    latency_ms: float


@dataclass(frozen=True)
class LoadTestSummary:
    scenario: str
    sample_count: int
    median_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    max_latency_ms: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "scenario": self.scenario,
            "sample_count": self.sample_count,
            "median_latency_ms": self.median_latency_ms,
            "p95_latency_ms": self.p95_latency_ms,
            "p99_latency_ms": self.p99_latency_ms,
            "max_latency_ms": self.max_latency_ms,
        }


def run_load_test(iterations: int = 20) -> dict[str, Any]:
    if iterations < 1:
        raise ValueError("iterations must be at least 1")

    samples = [
        _sample_latency(scenario=scenario, iteration=iteration)
        for scenario in SCENARIOS
        for iteration in range(1, iterations + 1)
    ]
    summaries = [_summarize_scenario(scenario, samples) for scenario in SCENARIOS]
    return {
        "source": "synthetic-load-test-v1",
        "iterations_per_scenario": iterations,
        "scenarios": [summary.as_dict() for summary in summaries],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run synthetic load-test harness.")
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    report = run_load_test(iterations=args.iterations)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(rendered + "\n")
    else:
        print(rendered)
    return 0


def _sample_latency(*, scenario: str, iteration: int) -> LoadTestSample:
    base = BASE_LATENCY_MS[scenario]
    jitter = ((iteration * 17) + (len(scenario) * 11)) % 90
    ramp = (iteration // 10) * 8
    return LoadTestSample(
        scenario=scenario,
        iteration=iteration,
        latency_ms=base + jitter + ramp,
    )


def _summarize_scenario(
    scenario: str, samples: list[LoadTestSample]
) -> LoadTestSummary:
    latencies = sorted(
        sample.latency_ms for sample in samples if sample.scenario == scenario
    )
    return LoadTestSummary(
        scenario=scenario,
        sample_count=len(latencies),
        median_latency_ms=_percentile(latencies, 0.50),
        p95_latency_ms=_percentile(latencies, 0.95),
        p99_latency_ms=_percentile(latencies, 0.99),
        max_latency_ms=max(latencies),
    )


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        raise ValueError("values must not be empty")
    index = max(0, ceil(percentile * len(values)) - 1)
    return values[index]


if __name__ == "__main__":
    raise SystemExit(main())
