from collections.abc import Generator

from ai_rollout_os.auth.permissions import require_role
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.training.guardrail_models import (
    FeedbackReleaseRead,
    GuardrailQuestionCreate,
    GuardrailQuizCreate,
    GuardrailQuizRead,
    QuizResultRead,
    QuizSubmission,
)
from ai_rollout_os.training.guardrail_service import GuardrailService
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

router = APIRouter()
OPERATOR_ACTOR = Depends(require_role("operator"))
LEARNER_ACTOR = Depends(require_role("learner"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.post("/guardrail-quizzes", response_model=GuardrailQuizRead, status_code=201)
def create_guardrail_quiz(
    payload: GuardrailQuizCreate,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> GuardrailQuizRead:
    quiz, questions = GuardrailService(session).create_quiz(payload, actor)
    session.commit()
    return GuardrailQuizRead(
        id=quiz.id,
        title=quiz.title,
        workspace_id=quiz.workspace_id,
        version=quiz.version,
        pass_threshold=quiz.pass_threshold,
        questions=[
            GuardrailQuestionCreate(
                id=question.id,
                question_text=question.question_text,
                answer_choices=question.answer_choices,
                correct_answer_ids=question.correct_answer_ids,
                explanation=question.explanation,
            )
            for question in questions
        ],
    )


@router.post(
    "/guardrail-quizzes/{quiz_id}/submissions",
    response_model=QuizResultRead,
)
def submit_guardrail_quiz(
    quiz_id: str,
    payload: QuizSubmission,
    actor: ActorContext = LEARNER_ACTOR,
    session: Session = DB_SESSION,
) -> QuizResultRead:
    result = GuardrailService(session).score_submission(quiz_id, payload, actor)
    session.commit()
    return QuizResultRead(
        id=result.id,
        quiz_id=result.quiz_id,
        learner_id=result.learner_id,
        score=result.score,
        passed=result.passed,
        missed_question_ids=result.missed_question_ids,
    )


@router.get(
    "/missions/{mission_id}/feedback-release",
    response_model=FeedbackReleaseRead,
)
def feedback_release_status(
    mission_id: str,
    actor: ActorContext = LEARNER_ACTOR,
    session: Session = DB_SESSION,
) -> FeedbackReleaseRead:
    GuardrailService(session).assert_feedback_release_allowed(mission_id, actor)
    return FeedbackReleaseRead(mission_id=mission_id, feedback_released=True)
