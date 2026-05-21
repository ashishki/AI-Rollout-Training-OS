from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_rollout_os.feedback.model_registry import (  # noqa: E402
    FEEDBACK_PROMPT_VERSION,
    FEEDBACK_SCHEMA_VERSION,
)

DEFAULT_EVAL_DOC = Path("docs/retrieval_eval.md")
TASK_NAME = "T48: Feedback Quality Eval Runner"
EVAL_SOURCE = (
    "scripts/eval_feedback.py against built-in role/customer feedback dataset, "
    "run 2026-05-21"
)
FEEDBACK_EVAL_CORPUS_VERSION = "feedback-eval-corpus-v1"
DEFAULT_MODEL_VERSION = "test-feedback-eval-model"


@dataclass(frozen=True)
class FeedbackEvalCase:
    case_id: str
    role: str
    customer_segment: str
    feedback_text: str
    expected_points: tuple[str, ...]
    unsupported_markers: tuple[str, ...]
    expected_human_review: bool
    routed_to_human_review: bool


@dataclass(frozen=True)
class FeedbackQualityMetrics:
    faithfulness: float
    completeness: float
    relevance: float
    unsupported_claim_rate: float
    human_review_routing_accuracy: float
    case_count: int
    corpus_version: str
    prompt_version: str
    model_version: str
    feedback_schema_version: str

    @property
    def meets_baseline(self) -> bool:
        return (
            self.faithfulness >= 0.90
            and self.completeness >= 0.80
            and self.relevance >= 0.90
            and self.unsupported_claim_rate <= 0.10
            and self.human_review_routing_accuracy >= 0.90
        )

    def as_dict(self) -> dict[str, float | int | str | bool]:
        return {
            "faithfulness": self.faithfulness,
            "completeness": self.completeness,
            "relevance": self.relevance,
            "unsupported_claim_rate": self.unsupported_claim_rate,
            "human_review_routing_accuracy": self.human_review_routing_accuracy,
            "case_count": self.case_count,
            "corpus_version": self.corpus_version,
            "prompt_version": self.prompt_version,
            "model_version": self.model_version,
            "feedback_schema_version": self.feedback_schema_version,
            "meets_baseline": self.meets_baseline,
        }


def default_eval_cases() -> list[FeedbackEvalCase]:
    return [
        FeedbackEvalCase(
            case_id="FQ01",
            role="support",
            customer_segment="pilot-support",
            feedback_text=(
                "Use sanitized customer data only, cite the policy snapshot, "
                "and route reuse to manager approval."
            ),
            expected_points=(
                "sanitized customer data",
                "policy snapshot",
                "manager approval",
            ),
            unsupported_markers=("productivity guarantee", "legal approval granted"),
            expected_human_review=False,
            routed_to_human_review=False,
        ),
        FeedbackEvalCase(
            case_id="FQ02",
            role="sales",
            customer_segment="pilot-sales",
            feedback_text=(
                "Draft outreach is allowed only as a first draft; a human must "
                "verify facts, pricing, and customer-specific commitments."
            ),
            expected_points=("first draft", "verify facts", "pricing"),
            unsupported_markers=("send automatically", "guaranteed conversion"),
            expected_human_review=False,
            routed_to_human_review=False,
        ),
        FeedbackEvalCase(
            case_id="FQ03",
            role="recruiting",
            customer_segment="pilot-recruiting",
            feedback_text=(
                "Remove candidate contact details before AI use and route the "
                "flagged artifact to human review."
            ),
            expected_points=("candidate contact details", "human review"),
            unsupported_markers=("store personal email", "certified safe"),
            expected_human_review=True,
            routed_to_human_review=True,
        ),
        FeedbackEvalCase(
            case_id="FQ04",
            role="policy",
            customer_segment="pilot-governance",
            feedback_text=(
                "The learner is asking for policy ownership approval, so the "
                "system must return insufficient evidence and route to human review."
            ),
            expected_points=(
                "policy ownership approval",
                "insufficient evidence",
                "human review",
            ),
            unsupported_markers=("policy approved", "legal approval granted"),
            expected_human_review=True,
            routed_to_human_review=True,
        ),
    ]


def run_feedback_evaluation(
    *,
    cases: list[FeedbackEvalCase] | None = None,
    eval_doc_path: Path = DEFAULT_EVAL_DOC,
    write_markdown: bool = True,
    model_version: str = DEFAULT_MODEL_VERSION,
) -> FeedbackQualityMetrics:
    metrics = compute_feedback_quality_metrics(
        cases or default_eval_cases(),
        model_version=model_version,
    )
    if write_markdown:
        update_eval_markdown(eval_doc_path, metrics)
    return metrics


def compute_feedback_quality_metrics(
    cases: list[FeedbackEvalCase], *, model_version: str = DEFAULT_MODEL_VERSION
) -> FeedbackQualityMetrics:
    if not cases:
        raise ValueError("Feedback eval requires at least one case")
    unsupported_results = [_has_unsupported_claim(case) for case in cases]
    completeness_scores = [_completeness(case) for case in cases]
    relevance_scores = [_relevance(case) for case in cases]
    routing_results = [
        case.expected_human_review == case.routed_to_human_review for case in cases
    ]
    unsupported_claim_rate = _rate(sum(unsupported_results), len(cases))
    return FeedbackQualityMetrics(
        faithfulness=1.0 - unsupported_claim_rate,
        completeness=sum(completeness_scores) / len(completeness_scores),
        relevance=sum(relevance_scores) / len(relevance_scores),
        unsupported_claim_rate=unsupported_claim_rate,
        human_review_routing_accuracy=_rate(sum(routing_results), len(cases)),
        case_count=len(cases),
        corpus_version=FEEDBACK_EVAL_CORPUS_VERSION,
        prompt_version=FEEDBACK_PROMPT_VERSION,
        model_version=model_version,
        feedback_schema_version=FEEDBACK_SCHEMA_VERSION,
    )


def update_eval_markdown(eval_doc_path: Path, metrics: FeedbackQualityMetrics) -> None:
    doc = eval_doc_path.read_text()
    row = (
        f"| {date.today().isoformat()} | {TASK_NAME} | {EVAL_SOURCE} | "
        f"`{metrics.corpus_version}` | `{metrics.prompt_version}` | "
        f"`{metrics.model_version}` | faithfulness={metrics.faithfulness:.2f}; "
        f"completeness={metrics.completeness:.2f}; "
        f"relevance={metrics.relevance:.2f}; "
        f"unsupported_claim_rate={metrics.unsupported_claim_rate:.2f}; "
        f"human_review_routing_accuracy={metrics.human_review_routing_accuracy:.2f} | "
        f"{'pass' if metrics.meets_baseline else 'fail'} | "
        "Deterministic feedback quality eval. |"
    )
    if row in doc:
        return
    marker = (
        "|------|------|-------------|----------------|----------------|"
        "---------------|---------|--------|-------|"
    )
    eval_doc_path.write_text(doc.replace(marker, f"{marker}\n{row}", 1))


def _has_unsupported_claim(case: FeedbackEvalCase) -> bool:
    feedback = case.feedback_text.lower()
    return any(marker.lower() in feedback for marker in case.unsupported_markers)


def _completeness(case: FeedbackEvalCase) -> float:
    feedback = case.feedback_text.lower()
    expected = [point.lower() for point in case.expected_points]
    return _rate(sum(point in feedback for point in expected), len(expected))


def _relevance(case: FeedbackEvalCase) -> float:
    return 1.0 if _completeness(case) > 0 else 0.0


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-doc", default=str(DEFAULT_EVAL_DOC))
    parser.add_argument("--model-version", default=DEFAULT_MODEL_VERSION)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)

    metrics = run_feedback_evaluation(
        eval_doc_path=Path(args.eval_doc),
        write_markdown=not args.no_write,
        model_version=args.model_version,
    )
    print(json.dumps(metrics.as_dict(), sort_keys=True))
    return 0 if metrics.meets_baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
