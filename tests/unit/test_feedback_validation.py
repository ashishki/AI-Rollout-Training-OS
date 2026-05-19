import pytest
from ai_rollout_os.feedback.engine import (
    FeedbackValidationError,
    validate_feedback_output,
)
from ai_rollout_os.feedback.schemas import StructuredFeedbackOutput
from ai_rollout_os.retrieval.evidence import EvidenceBlock


def test_feedback_rejects_unknown_citation_id() -> None:
    output = StructuredFeedbackOutput(
        rubric_outcome="needs_revision",
        learner_feedback="Revise the artifact to follow policy.",
        manager_notes="Needs coaching.",
        citations=[
            {
                "chunk_id": "missing-chunk",
                "source_id": "policy",
                "section_path": "Policy > Customer Data",
                "quote": "Do not paste customer data.",
            }
        ],
        risk_flags=["customer_data"],
        validation_status="valid",
    )
    evidence = [
        EvidenceBlock(
            source_id="policy",
            section_path="Policy > Customer Data",
            chunk_id="chunk-1",
            score=0.9,
            snippet="Do not paste customer data.",
        )
    ]

    with pytest.raises(FeedbackValidationError):
        validate_feedback_output(output, evidence)
