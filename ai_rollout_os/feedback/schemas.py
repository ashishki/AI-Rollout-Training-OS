from pydantic import BaseModel, Field


class FeedbackCitation(BaseModel):
    chunk_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    section_path: str = Field(min_length=1)
    quote: str = Field(min_length=1)


class StructuredFeedbackOutput(BaseModel):
    rubric_outcome: str = Field(min_length=1)
    learner_feedback: str = Field(min_length=1)
    manager_notes: str = Field(min_length=1)
    citations: list[FeedbackCitation] = Field(min_length=1)
    risk_flags: list[str]
    validation_status: str = Field(min_length=1)
