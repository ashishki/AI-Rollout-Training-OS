from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import (
    FeedbackResult,
    GuardrailQuiz,
    MissionTemplate,
    ProgressReport,
    RolePack,
    SourceDocument,
    Submission,
    User,
)
from ai_rollout_os.feedback.jobs import FeedbackJobService
from ai_rollout_os.jobs.models import GeneratedFeedback
from ai_rollout_os.jobs.worker import FeedbackWorker
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from tests.fixtures.pilot_data import seed_pilot_data


def test_pilot_fixture_creates_minimum_dataset(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        pilot = seed_pilot_data(session)
        session.commit()

    with Session(migrated_engine) as session:
        users = session.scalars(
            select(User).where(User.workspace_id == pilot.workspace_id)
        ).all()
        role_pack = session.get(RolePack, pilot.role_pack_id)
        missions = session.scalars(
            select(MissionTemplate).where(
                MissionTemplate.role_pack_id == pilot.role_pack_id
            )
        ).all()
        quizzes = session.scalars(
            select(GuardrailQuiz).where(
                GuardrailQuiz.workspace_id == pilot.workspace_id
            )
        ).all()
        documents = session.scalars(
            select(SourceDocument).where(
                SourceDocument.workspace_id == pilot.workspace_id
            )
        ).all()

    assert len(users) == 4
    assert {user.role for user in users} == {"operator", "manager", "learner"}
    assert role_pack is not None
    assert len(missions) == 2
    assert len(quizzes) == 1
    assert {document.document_type for document in documents} == {
        "company_policy",
        "sop",
    }


def test_end_to_end_pilot_flow(migrated_engine: Engine) -> None:
    client = pilot_client(migrated_engine)
    with Session(migrated_engine) as session:
        pilot = seed_pilot_data(session)
        session.commit()

    cohort = client.post(
        "/cohorts",
        json={
            "role_pack_id": pilot.role_pack_id,
            "role_pack_version": 1,
            "manager_id": pilot.manager_id,
            "learner_ids": pilot.learner_ids,
            "start_date": "2026-05-19",
            "due_date": "2026-06-19",
        },
        headers=auth_headers(pilot.operator_id, "operator", pilot.workspace_id),
    )
    assert cohort.status_code == 201
    launch = client.post(
        f"/cohorts/{cohort.json()['id']}/launch",
        headers=auth_headers(pilot.operator_id, "operator", pilot.workspace_id),
    )
    assert launch.status_code == 200
    assignments = launch.json()
    assert len(assignments) == 4
    assignment = next(
        item
        for item in assignments
        if item["learner_id"] == pilot.learner_ids[0]
        and item["mission_template_id"] == pilot.mission_ids[0]
    )

    quiz = client.post(
        f"/guardrail-quizzes/{pilot.guardrail_quiz_id}/submissions",
        json={
            "answers": [
                {
                    "question_id": pilot.question_id,
                    "answer_ids": ["safe"],
                }
            ]
        },
        headers=auth_headers(pilot.learner_ids[0], "learner", pilot.workspace_id),
    )
    assert quiz.status_code == 200
    assert quiz.json()["passed"] is True

    submission_response = client.post(
        f"/missions/{pilot.mission_ids[0]}/submissions",
        json={
            "assignment_id": assignment["id"],
            "artifact_text": (
                "Draft reply uses sanitized ticket context and cites policy."
            ),
            "policy_snapshot_id": pilot.policy_snapshot_id,
            "rubric_id": pilot.rubric_id,
        },
        headers=auth_headers(pilot.learner_ids[0], "learner", pilot.workspace_id),
    )
    assert submission_response.status_code == 201
    submission_id = submission_response.json()["id"]

    run_feedback_worker(migrated_engine, submission_id)

    approval = client.post(
        f"/manager/submissions/{submission_id}/approve",
        json={
            "approval_note": "Evidence is sufficient for pilot reuse.",
            "approved_workflow_change": "Reuse sanitized support reply workflow.",
        },
        headers=auth_headers(pilot.manager_id, "manager", pilot.workspace_id),
    )
    assert approval.status_code == 200
    assert approval.json()["approval_status"] == "approved"

    report = client.post(
        f"/manager/cohorts/{cohort.json()['id']}/reports",
        headers=auth_headers(pilot.manager_id, "manager", pilot.workspace_id),
    )
    assert report.status_code == 201
    assert "Reuse sanitized support reply workflow." in report.json()["markdown_body"]

    with Session(migrated_engine) as session:
        feedback_result = session.scalar(
            select(FeedbackResult).where(FeedbackResult.submission_id == submission_id)
        )
        progress_report = session.scalar(select(ProgressReport))
    assert feedback_result is not None
    assert progress_report is not None


def run_feedback_worker(engine: Engine, submission_id: str) -> None:
    with Session(engine) as session:
        submission = session.get(Submission, submission_id)
        assert submission is not None
        submission.review_state = "ready_for_feedback"
        FeedbackJobService(session).enqueue_ready_submission(
            submission_id=submission_id
        )
        worker = FeedbackWorker(
            session=session,
            settings=get_settings({"APP_ENV": "test"}),
            evaluator=lambda _job: GeneratedFeedback(
                feedback_status="completed",
                learner_feedback="Good use of sanitized evidence.",
                validation_status="valid",
                risk_flags=[],
            ),
        )
        completed = worker.run_one()
        assert completed is not None
        session.commit()


def pilot_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}),
        session_factory=session_factory,
    )
    return TestClient(app)


def auth_headers(actor_id: str, role: str, workspace_id: str) -> dict[str, str]:
    token = create_token(
        actor_id=actor_id,
        role=role,
        workspace_id=workspace_id,
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-pilot"}
