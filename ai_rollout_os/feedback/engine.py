from sqlalchemy.orm import Session

from ai_rollout_os.feedback.repository import FeedbackRecord, FeedbackRepository
from ai_rollout_os.feedback.schemas import StructuredFeedbackOutput
from ai_rollout_os.retrieval.evidence import EvidenceBlock, RetrievalResult


class FeedbackValidationError(ValueError):
    pass


class RubricEvaluationEngine:
    def __init__(self, session: Session) -> None:
        self._repository = FeedbackRepository(session)

    def evaluate_submission(
        self,
        *,
        submission_id: str,
        retrieval_result: RetrievalResult,
        llm_output: StructuredFeedbackOutput | None = None,
        actor_id: str = "system",
        trace_id: str = "trace-feedback-engine",
    ) -> FeedbackRecord:
        if retrieval_result.status == "insufficient_evidence":
            return self._repository.store_needs_human_review(
                submission_id=submission_id,
                reason=retrieval_result.reason,
                actor_id=actor_id,
                trace_id=trace_id,
            )

        if llm_output is None:
            raise FeedbackValidationError("Missing structured feedback output")

        validate_feedback_output(llm_output, retrieval_result.evidence)
        return FeedbackRecord(
            submission_id=submission_id,
            feedback_status="ready_for_manager_review",
            learner_feedback=llm_output.learner_feedback,
            validation_status=llm_output.validation_status,
        )


def validate_feedback_output(
    output: StructuredFeedbackOutput, evidence: list[EvidenceBlock]
) -> None:
    allowed_chunk_ids = {block.chunk_id for block in evidence}
    unknown_ids = [
        citation.chunk_id
        for citation in output.citations
        if citation.chunk_id not in allowed_chunk_ids
    ]
    if unknown_ids:
        raise FeedbackValidationError("Feedback cited evidence that was not retrieved")
