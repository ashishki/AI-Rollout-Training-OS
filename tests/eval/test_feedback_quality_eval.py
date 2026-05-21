from scripts.eval_feedback import (
    DEFAULT_MODEL_VERSION,
    FeedbackEvalCase,
    compute_feedback_quality_metrics,
    run_feedback_evaluation,
)


def test_feedback_quality_metrics() -> None:
    metrics = run_feedback_evaluation(write_markdown=False)

    assert metrics.meets_baseline
    assert metrics.faithfulness == 1.0
    assert metrics.completeness == 1.0
    assert metrics.relevance == 1.0
    assert metrics.unsupported_claim_rate == 0.0
    assert metrics.human_review_routing_accuracy == 1.0
    assert metrics.prompt_version
    assert metrics.model_version == DEFAULT_MODEL_VERSION


def test_unsupported_claims_lower_faithfulness() -> None:
    metrics = compute_feedback_quality_metrics(
        [
            FeedbackEvalCase(
                case_id="bad",
                role="support",
                customer_segment="pilot",
                feedback_text="This includes a productivity guarantee.",
                expected_points=("manager approval",),
                unsupported_markers=("productivity guarantee",),
                expected_human_review=True,
                routed_to_human_review=False,
            )
        ]
    )

    assert metrics.faithfulness == 0.0
    assert metrics.completeness == 0.0
    assert metrics.relevance == 0.0
    assert metrics.unsupported_claim_rate == 1.0
    assert metrics.human_review_routing_accuracy == 0.0
    assert not metrics.meets_baseline
