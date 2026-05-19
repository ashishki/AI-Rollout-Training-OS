from ai_rollout_os.db.models import GuardrailQuestion, GuardrailQuiz, QuizResult
from pydantic import BaseModel, Field


class AnswerChoice(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1)


class GuardrailQuestionCreate(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    question_text: str = Field(min_length=1)
    answer_choices: list[AnswerChoice] = Field(min_length=1)
    correct_answer_ids: list[str] = Field(min_length=1)
    explanation: str = Field(min_length=1)


class GuardrailQuizCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    pass_threshold: int = Field(ge=0, le=100)
    questions: list[GuardrailQuestionCreate] = Field(min_length=1)


class GuardrailQuizRead(BaseModel):
    id: str
    title: str
    workspace_id: str
    version: int
    pass_threshold: int
    questions: list[GuardrailQuestionCreate]


class QuizAnswer(BaseModel):
    question_id: str = Field(min_length=1, max_length=64)
    answer_ids: list[str] = Field(default_factory=list)


class QuizSubmission(BaseModel):
    answers: list[QuizAnswer]


class QuizResultRead(BaseModel):
    id: str
    quiz_id: str
    learner_id: str
    score: int
    passed: bool
    missed_question_ids: list[str]


class FeedbackReleaseRead(BaseModel):
    mission_id: str
    feedback_released: bool


__all__ = [
    "AnswerChoice",
    "FeedbackReleaseRead",
    "GuardrailQuestion",
    "GuardrailQuestionCreate",
    "GuardrailQuiz",
    "GuardrailQuizCreate",
    "GuardrailQuizRead",
    "QuizAnswer",
    "QuizResult",
    "QuizResultRead",
    "QuizSubmission",
]
