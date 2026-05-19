from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import GuardrailQuestion, GuardrailQuiz
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_create_guardrail_quiz(migrated_engine: Engine) -> None:
    client = guardrail_client(migrated_engine)

    response = client.post(
        "/guardrail-quizzes",
        json=quiz_payload(),
        headers=auth_headers("operator-1", "operator"),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Support guardrails"
    assert payload["pass_threshold"] == 100
    assert payload["questions"][0]["answer_choices"][0]["id"] == "a"
    assert payload["questions"][0]["correct_answer_ids"] == ["a"]
    assert payload["questions"][0]["explanation"] == "Use approved sources."

    with Session(migrated_engine) as session:
        stored_quiz = session.scalar(select(GuardrailQuiz))
        stored_question = session.scalar(select(GuardrailQuestion))
    assert stored_quiz is not None
    assert stored_question is not None
    assert stored_question.correct_answer_ids == ["a"]


def test_quiz_scoring_is_deterministic(migrated_engine: Engine) -> None:
    client = guardrail_client(migrated_engine)
    quiz_id = create_quiz(client)

    response = client.post(
        f"/guardrail-quizzes/{quiz_id}/submissions",
        json={
            "answers": [
                {"question_id": "q1", "answer_ids": ["a"]},
                {"question_id": "q2", "answer_ids": ["c"]},
            ]
        },
        headers=auth_headers("learner-1", "learner"),
    )

    assert response.status_code == 200
    assert response.json()["score"] == 50
    assert response.json()["passed"] is False
    assert response.json()["missed_question_ids"] == ["q2"]


def test_feedback_release_requires_passing_quiz(migrated_engine: Engine) -> None:
    client = guardrail_client(migrated_engine)
    quiz_id = create_quiz(client)
    mission_id = create_role_pack_mission(client, quiz_id)

    blocked = client.get(
        f"/missions/{mission_id}/feedback-release",
        headers=auth_headers("learner-1", "learner"),
    )
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["code"] == "guardrail_quiz_not_passed"

    passed = client.post(
        f"/guardrail-quizzes/{quiz_id}/submissions",
        json={
            "answers": [
                {"question_id": "q1", "answer_ids": ["a"]},
                {"question_id": "q2", "answer_ids": ["b"]},
            ]
        },
        headers=auth_headers("learner-1", "learner"),
    )
    assert passed.status_code == 200
    assert passed.json()["passed"] is True

    released = client.get(
        f"/missions/{mission_id}/feedback-release",
        headers=auth_headers("learner-1", "learner"),
    )
    assert released.status_code == 200
    assert released.json() == {"mission_id": mission_id, "feedback_released": True}


def guardrail_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def create_quiz(client: TestClient) -> str:
    response = client.post(
        "/guardrail-quizzes",
        json=quiz_payload(),
        headers=auth_headers("operator-1", "operator"),
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def create_role_pack_mission(client: TestClient, quiz_id: str) -> str:
    role_pack = client.post(
        "/role-packs",
        json={"role": "support", "title": "Support AI rollout"},
        headers=auth_headers("operator-1", "operator"),
    )
    assert role_pack.status_code == 201
    role_pack_id = str(role_pack.json()["id"])
    mission = client.post(
        f"/role-packs/{role_pack_id}/missions",
        json={
            "objective": "Draft a customer-safe support reply.",
            "instructions": "Use approved workflow.",
            "artifact_type": "text_response",
            "rubric_id": "rubric-1",
            "guardrail_quiz_id": quiz_id,
        },
        headers=auth_headers("operator-1", "operator"),
    )
    assert mission.status_code == 200
    return str(mission.json()["id"])


def quiz_payload() -> dict:
    return {
        "title": "Support guardrails",
        "pass_threshold": 100,
        "questions": [
            {
                "id": "q1",
                "question_text": "What should support answers cite?",
                "answer_choices": [
                    {"id": "a", "text": "Approved sources"},
                    {"id": "x", "text": "Unverified memory"},
                ],
                "correct_answer_ids": ["a"],
                "explanation": "Use approved sources.",
            },
            {
                "id": "q2",
                "question_text": "When should sensitive data be pasted?",
                "answer_choices": [
                    {"id": "b", "text": "Never without approval"},
                    {"id": "c", "text": "Whenever it is convenient"},
                ],
                "correct_answer_ids": ["b"],
                "explanation": "Sensitive data requires approval.",
            },
        ],
    }


def auth_headers(actor_id: str, role: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-guardrails"}
