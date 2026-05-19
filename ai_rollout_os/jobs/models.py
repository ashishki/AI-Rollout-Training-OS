from dataclasses import dataclass


class FeedbackJobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    RETRYABLE_FAILED = "retryable_failed"
    COMPLETED = "completed"
    TIMED_OUT = "timed_out"


@dataclass(frozen=True)
class GeneratedFeedback:
    feedback_status: str
    learner_feedback: str | None
    validation_status: str
    risk_flags: list[str] | None = None
