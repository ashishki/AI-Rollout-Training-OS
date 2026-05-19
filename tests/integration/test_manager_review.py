from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import (
    AuditEvent,
    FeedbackResult,
    GuardrailQuiz,
    MissionTemplate,
    QuizResult,
    RolePack,
    Submission,
)
from ai_rollout_os.feedback.jobs import FeedbackJobService
from ai_rollout_os.jobs.models import GeneratedFeedback
from ai_rollout_os.jobs.worker import FeedbackWorker
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_manager_submission_filters(migrated_engine: Engine) -> None:
    client = manager_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_review_data(session)
        session.commit()

    response = client.get(
        (
            "/manager/submissions?learner_id=learner-1&mission_id=mission-1"
            "&feedback_status=ready_for_manager_review&guardrail_status=passed"
            "&risk_flag=privacy"
        ),
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert [item["id"] for item in payload] == ["submission-1"]
    assert payload[0]["feedback_status"] == "ready_for_manager_review"
    assert payload[0]["guardrail_status"] == "passed"
    assert payload[0]["risk_flags"] == ["privacy"]


def test_manager_can_approve_workflow_change(migrated_engine: Engine) -> None:
    client = manager_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_review_data(session)
        session.commit()

    response = client.post(
        "/manager/submissions/submission-1/approve",
        json={
            "approval_note": "Approved for support pilot reuse.",
            "approved_workflow_change": "Reusable customer-safe reply workflow.",
        },
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["approval_status"] == "approved"
    assert payload["manager_id"] == "manager-1"
    assert payload["approval_note"] == "Approved for support pilot reuse."
    assert (
        payload["approved_workflow_change"] == "Reusable customer-safe reply workflow."
    )
    assert payload["approved_at"] is not None

    with Session(migrated_engine) as session:
        stored = session.scalar(
            select(Submission).where(Submission.id == "submission-1")
        )
        audit_event = session.scalar(
            select(AuditEvent).where(
                AuditEvent.action == "submission.workflow_change_approved"
            )
        )
    assert stored is not None
    assert stored.approved_workflow_change == "Reusable customer-safe reply workflow."
    assert audit_event is not None
    assert audit_event.resource_id == "submission-1"


def test_feedback_job_cannot_set_manager_approval(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        submission = ready_submission()
        session.add(submission)
        session.commit()
        FeedbackJobService(session).enqueue_ready_submission(
            submission_id=submission.id
        )
        session.commit()

        worker = FeedbackWorker(
            session=session,
            settings=get_settings({"APP_ENV": "test"}),
            evaluator=lambda _job: GeneratedFeedback(
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=["privacy"],
            ),
        )
        job = worker.run_one()
        assert job is not None
        session.commit()

        stored = session.scalar(
            select(Submission).where(Submission.id == submission.id)
        )

    assert stored is not None
    assert stored.approval_status == "not_reviewed"
    assert stored.manager_id is None
    assert stored.approved_at is None
    assert stored.approved_workflow_change is None


def manager_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def seed_review_data(session: Session) -> None:
    session.add(
        RolePack(
            id="role-pack-1",
            workspace_id="ws-1",
            role="support",
            title="Support AI rollout",
            version=1,
            launch_status="active",
            created_by="operator-1",
        )
    )
    session.add(
        GuardrailQuiz(
            id="quiz-1",
            workspace_id="ws-1",
            title="Support guardrails",
            version=1,
            pass_threshold=80,
        )
    )
    session.add(
        MissionTemplate(
            id="mission-1",
            role_pack_id="role-pack-1",
            workspace_id="ws-1",
            objective="Draft safe support reply.",
            instructions="Use approved evidence.",
            artifact_type="text_response",
            rubric_id="rubric-1",
            guardrail_quiz_id="quiz-1",
            active=True,
        )
    )
    session.add(
        QuizResult(
            id="quiz-result-1",
            quiz_id="quiz-1",
            workspace_id="ws-1",
            learner_id="learner-1",
            score=100,
            passed=True,
            missed_question_ids=[],
            answers=[],
        )
    )
    session.add(ready_submission())
    session.add(
        Submission(
            id="submission-2",
            workspace_id="ws-1",
            mission_template_id="mission-2",
            assignment_id="assignment-2",
            learner_id="learner-2",
            artifact_text="Other draft workflow artifact.",
            policy_snapshot_id="snapshot-1",
            rubric_id="rubric-1",
            version=1,
            review_state="ready_for_feedback",
            redaction_status="clear",
            approval_status="not_reviewed",
        )
    )
    session.add(
        FeedbackResult(
            id="feedback-result-1",
            workspace_id="ws-1",
            submission_id="submission-1",
            submission_version=1,
            feedback_status="ready_for_manager_review",
            learner_feedback="Use approved evidence.",
            validation_status="valid",
            risk_flags=["privacy"],
        )
    )
    session.add(
        FeedbackResult(
            id="feedback-result-2",
            workspace_id="ws-1",
            submission_id="submission-2",
            submission_version=1,
            feedback_status="needs_human_review",
            learner_feedback=None,
            validation_status="insufficient_evidence",
            risk_flags=["missing_evidence"],
        )
    )


def ready_submission() -> Submission:
    return Submission(
        id="submission-1",
        workspace_id="ws-1",
        mission_template_id="mission-1",
        assignment_id="assignment-1",
        learner_id="learner-1",
        artifact_text="Draft workflow artifact.",
        policy_snapshot_id="snapshot-1",
        rubric_id="rubric-1",
        version=1,
        review_state="ready_for_feedback",
        redaction_status="clear",
        approval_status="not_reviewed",
    )


def auth_headers(actor_id: str, role: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-manager-review"}
