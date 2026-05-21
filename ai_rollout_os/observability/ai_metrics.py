from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import Any

SAFE_LABEL_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
AI_METRIC_LABEL_KEYS = ("provider", "model", "feature", "workspace_id", "operation_id")


@dataclass(frozen=True)
class AIMetricLabels:
    provider: str
    model: str
    feature: str
    workspace_id: str
    operation_id: str

    def as_dict(self) -> dict[str, str]:
        return {
            "provider": self.provider,
            "model": self.model,
            "feature": self.feature,
            "workspace_id": self.workspace_id,
            "operation_id": self.operation_id,
        }


@dataclass(frozen=True)
class AIMetricRecord:
    labels: AIMetricLabels
    latency_ms: float
    cost_usd: float
    input_tokens: int
    output_tokens: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "labels": self.labels.as_dict(),
            "latency_ms": self.latency_ms,
            "cost_usd": self.cost_usd,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }


@dataclass(frozen=True)
class AIMetricSummary:
    labels: AIMetricLabels
    call_count: int
    total_cost_usd: float
    total_input_tokens: int
    total_output_tokens: int
    average_latency_ms: float
    p95_latency_ms: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "labels": self.labels.as_dict(),
            "call_count": self.call_count,
            "total_cost_usd": self.total_cost_usd,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "average_latency_ms": self.average_latency_ms,
            "p95_latency_ms": self.p95_latency_ms,
        }


class AIMetricsLedger:
    def __init__(self) -> None:
        self._records: list[AIMetricRecord] = []

    @property
    def records(self) -> tuple[AIMetricRecord, ...]:
        return tuple(self._records)

    def record_call(
        self,
        *,
        provider: str,
        model: str,
        feature: str,
        workspace_id: str,
        operation_id: str,
        latency_ms: float,
        cost_usd: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> AIMetricRecord:
        labels = AIMetricLabels(
            provider=_safe_label("provider", provider),
            model=_safe_label("model", model),
            feature=_safe_label("feature", feature),
            workspace_id=_safe_label("workspace_id", workspace_id),
            operation_id=_safe_label("operation_id", operation_id),
        )
        record = AIMetricRecord(
            labels=labels,
            latency_ms=_non_negative_float("latency_ms", latency_ms),
            cost_usd=_non_negative_float("cost_usd", cost_usd),
            input_tokens=_non_negative_int("input_tokens", input_tokens),
            output_tokens=_non_negative_int("output_tokens", output_tokens),
        )
        self._records.append(record)
        return record

    def summarize(self) -> list[AIMetricSummary]:
        grouped: dict[tuple[str, ...], list[AIMetricRecord]] = defaultdict(list)
        for record in self._records:
            grouped[_label_key(record.labels)].append(record)

        summaries = []
        for records in grouped.values():
            labels = records[0].labels
            latencies = sorted(record.latency_ms for record in records)
            summaries.append(
                AIMetricSummary(
                    labels=labels,
                    call_count=len(records),
                    total_cost_usd=sum(record.cost_usd for record in records),
                    total_input_tokens=sum(record.input_tokens for record in records),
                    total_output_tokens=sum(record.output_tokens for record in records),
                    average_latency_ms=sum(latencies) / len(latencies),
                    p95_latency_ms=_percentile(latencies, 0.95),
                )
            )
        return sorted(summaries, key=lambda summary: _label_key(summary.labels))


def _safe_label(key: str, value: str) -> str:
    if key not in AI_METRIC_LABEL_KEYS:
        raise ValueError(f"Unsupported AI metric label: {key}")
    if not SAFE_LABEL_RE.fullmatch(value):
        raise ValueError(f"Unsafe AI metric label value for {key}")
    return value


def _non_negative_float(key: str, value: float) -> float:
    numeric = float(value)
    if numeric < 0:
        raise ValueError(f"{key} must be non-negative")
    return numeric


def _non_negative_int(key: str, value: int) -> int:
    numeric = int(value)
    if numeric < 0:
        raise ValueError(f"{key} must be non-negative")
    return numeric


def _label_key(labels: AIMetricLabels) -> tuple[str, ...]:
    return tuple(labels.as_dict()[key] for key in AI_METRIC_LABEL_KEYS)


def _percentile(values: list[float], percentile: float) -> float:
    index = max(0, ceil(percentile * len(values)) - 1)
    return values[index]
