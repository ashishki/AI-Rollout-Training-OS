from dataclasses import dataclass
from datetime import date

from ai_rollout_os.db.models import (
    GuardrailQuestion,
    GuardrailQuiz,
    MissionTemplate,
    RolePack,
    Rubric,
    SourceDocument,
    User,
    Workspace,
)
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class PilotData:
    workspace_id: str
    operator_id: str
    manager_id: str
    learner_ids: list[str]
    role_pack_id: str
    mission_ids: list[str]
    guardrail_quiz_id: str
    question_id: str
    policy_snapshot_id: str
    rubric_id: str


def seed_pilot_data(session: Session) -> PilotData:
    workspace_id = "ws-pilot"
    operator_id = "operator-pilot"
    manager_id = "manager-pilot"
    learner_ids = ["learner-pilot-1", "learner-pilot-2"]
    role_pack_id = "role-pack-pilot-support"
    guardrail_quiz_id = "quiz-pilot-guardrails"
    question_id = "question-safe-data"
    rubric_id = "rubric-pilot-feedback"

    session.add(Workspace(id=workspace_id, name="Pilot Workspace"))
    session.add_all(
        [
            User(
                id=operator_id,
                workspace_id=workspace_id,
                email="operator@example.test",
                role="operator",
            ),
            User(
                id=manager_id,
                workspace_id=workspace_id,
                email="manager@example.test",
                role="manager",
            ),
            User(
                id=learner_ids[0],
                workspace_id=workspace_id,
                email="learner1@example.test",
                role="learner",
            ),
            User(
                id=learner_ids[1],
                workspace_id=workspace_id,
                email="learner2@example.test",
                role="learner",
            ),
        ]
    )
    session.add(Rubric(id=rubric_id, workspace_id=workspace_id, title="Pilot rubric"))
    session.add(
        GuardrailQuiz(
            id=guardrail_quiz_id,
            workspace_id=workspace_id,
            title="Pilot guardrails",
            version=1,
            pass_threshold=80,
        )
    )
    session.flush()
    session.add(
        GuardrailQuestion(
            id=question_id,
            quiz_id=guardrail_quiz_id,
            workspace_id=workspace_id,
            question_text="Which data may be pasted into AI tools?",
            answer_choices=[
                {"id": "safe", "text": "Sanitized ticket context"},
                {"id": "unsafe", "text": "Payment details"},
            ],
            correct_answer_ids=["safe"],
            explanation="Only sanitized context is allowed.",
        )
    )
    session.add(
        RolePack(
            id=role_pack_id,
            workspace_id=workspace_id,
            role="support",
            title="Support pilot role pack",
            version=1,
            launch_status="active",
            created_by=operator_id,
        )
    )
    session.flush()
    mission_ids = ["mission-pilot-reply", "mission-pilot-review"]
    session.add_all(
        [
            MissionTemplate(
                id=mission_ids[0],
                role_pack_id=role_pack_id,
                workspace_id=workspace_id,
                objective="Draft a safe support reply.",
                instructions="Use policy evidence and avoid sensitive data.",
                artifact_type="text_response",
                rubric_id=rubric_id,
                guardrail_quiz_id=guardrail_quiz_id,
                active=True,
            ),
            MissionTemplate(
                id=mission_ids[1],
                role_pack_id=role_pack_id,
                workspace_id=workspace_id,
                objective="Review an AI-assisted workflow.",
                instructions="Identify what needs manager approval.",
                artifact_type="workflow_review",
                rubric_id=rubric_id,
                guardrail_quiz_id=guardrail_quiz_id,
                active=True,
            ),
        ]
    )
    session.add_all(
        [
            SourceDocument(
                id="pilot-policy-v1",
                logical_document_id="pilot-policy",
                workspace_id=workspace_id,
                title="Pilot AI policy",
                document_type="company_policy",
                body_text=(
                    "Use sanitized support context only. Manager approval is "
                    "required before reusing workflow changes."
                ),
                effective_date=date(2026, 5, 19),
                snapshot_id="snapshot-pilot-policy-v1",
                version=1,
                created_by=operator_id,
            ),
            SourceDocument(
                id="pilot-sop-v1",
                logical_document_id="pilot-sop",
                workspace_id=workspace_id,
                title="Pilot support SOP",
                document_type="sop",
                body_text=(
                    "Learners submit artifacts, receive feedback, and managers "
                    "approve reusable workflow changes."
                ),
                effective_date=date(2026, 5, 19),
                snapshot_id="snapshot-pilot-sop-v1",
                version=1,
                created_by=operator_id,
            ),
        ]
    )
    session.flush()
    return PilotData(
        workspace_id=workspace_id,
        operator_id=operator_id,
        manager_id=manager_id,
        learner_ids=learner_ids,
        role_pack_id=role_pack_id,
        mission_ids=mission_ids,
        guardrail_quiz_id=guardrail_quiz_id,
        question_id=question_id,
        policy_snapshot_id="snapshot-pilot-policy-v1",
        rubric_id=rubric_id,
    )
