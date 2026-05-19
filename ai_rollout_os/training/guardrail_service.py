from uuid import uuid4

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    GuardrailQuestion,
    GuardrailQuiz,
    MissionTemplate,
    QuizResult,
)
from ai_rollout_os.training.guardrail_models import GuardrailQuizCreate, QuizSubmission
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session


class GuardrailService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_quiz(
        self, payload: GuardrailQuizCreate, actor: ActorContext
    ) -> tuple[GuardrailQuiz, list[GuardrailQuestion]]:
        quiz = GuardrailQuiz(
            id=f"quiz_{uuid4().hex}",
            workspace_id=actor.workspace_id,
            title=payload.title,
            version=1,
            pass_threshold=payload.pass_threshold,
        )
        self._session.add(quiz)
        self._session.flush()
        questions = [
            GuardrailQuestion(
                id=question.id,
                quiz_id=quiz.id,
                workspace_id=actor.workspace_id,
                question_text=question.question_text,
                answer_choices=[
                    choice.model_dump() for choice in question.answer_choices
                ],
                correct_answer_ids=question.correct_answer_ids,
                explanation=question.explanation,
            )
            for question in payload.questions
        ]
        self._session.add_all(questions)
        self._session.flush()
        return quiz, questions

    def score_submission(
        self, quiz_id: str, payload: QuizSubmission, actor: ActorContext
    ) -> QuizResult:
        quiz = self._quiz_for_actor(quiz_id, actor)
        questions = self._session.scalars(
            select(GuardrailQuestion).where(
                GuardrailQuestion.quiz_id == quiz.id,
                GuardrailQuestion.workspace_id == actor.workspace_id,
            )
        ).all()
        answer_map = {
            answer.question_id: set(answer.answer_ids) for answer in payload.answers
        }
        missed_question_ids = [
            question.id
            for question in questions
            if answer_map.get(question.id, set()) != set(question.correct_answer_ids)
        ]
        correct_count = len(questions) - len(missed_question_ids)
        score = int((correct_count / len(questions)) * 100) if questions else 0
        result = QuizResult(
            id=f"quiz_result_{uuid4().hex}",
            quiz_id=quiz.id,
            workspace_id=actor.workspace_id,
            learner_id=actor.actor_id,
            score=score,
            passed=score >= quiz.pass_threshold,
            missed_question_ids=missed_question_ids,
            answers=[answer.model_dump() for answer in payload.answers],
        )
        self._session.add(result)
        self._session.flush()
        return result

    def assert_feedback_release_allowed(
        self, mission_id: str, actor: ActorContext
    ) -> None:
        mission = self._session.scalar(
            select(MissionTemplate).where(
                MissionTemplate.id == mission_id,
                MissionTemplate.workspace_id == actor.workspace_id,
            )
        )
        if mission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
            )
        passing_result = self._session.scalar(
            select(QuizResult.id).where(
                QuizResult.quiz_id == mission.guardrail_quiz_id,
                QuizResult.workspace_id == actor.workspace_id,
                QuizResult.learner_id == actor.actor_id,
                QuizResult.passed.is_(True),
            )
        )
        if passing_result is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "guardrail_quiz_not_passed"},
            )

    def _quiz_for_actor(self, quiz_id: str, actor: ActorContext) -> GuardrailQuiz:
        quiz = self._session.scalar(
            select(GuardrailQuiz).where(
                GuardrailQuiz.id == quiz_id,
                GuardrailQuiz.workspace_id == actor.workspace_id,
            )
        )
        if quiz is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )
        return quiz
