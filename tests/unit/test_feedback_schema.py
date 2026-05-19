import pytest
from ai_rollout_os.feedback.schemas import StructuredFeedbackOutput
from pydantic import ValidationError


def test_feedback_schema_requires_expected_fields() -> None:
    required = {
        name
        for name, field in StructuredFeedbackOutput.model_fields.items()
        if field.is_required()
    }

    assert {
        "rubric_outcome",
        "learner_feedback",
        "manager_notes",
        "citations",
        "risk_flags",
        "validation_status",
    }.issubset(required)

    with pytest.raises(ValidationError):
        StructuredFeedbackOutput(
            rubric_outcome="meets_expectations",
            learner_feedback="Use the approved workflow.",
            citations=[
                {
                    "chunk_id": "chunk-1",
                    "source_id": "policy",
                    "section_path": "Policy",
                    "quote": "Approved workflow.",
                }
            ],
            risk_flags=[],
            validation_status="valid",
        )
