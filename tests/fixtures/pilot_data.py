from dataclasses import dataclass
from datetime import UTC, date, datetime

from ai_rollout_os.db.models import (
    Cohort,
    CohortEnrollment,
    FeedbackResult,
    GuardrailQuestion,
    GuardrailQuiz,
    MissionAssignment,
    MissionTemplate,
    ProgressReport,
    RolePack,
    Rubric,
    SourceDocument,
    Submission,
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


@dataclass(frozen=True)
class SoloMiniCohortData:
    workspace_id: str
    operator_id: str
    reviewer_id: str
    learner_id: str
    role_pack_id: str
    cohort_id: str
    mission_ids: list[str]
    assignment_ids: list[str]
    submission_ids: list[str]
    feedback_result_ids: list[str]
    approved_submission_id: str
    report_id: str
    policy_snapshot_id: str


@dataclass(frozen=True)
class LeadResponseMissionDefinition:
    mission_id: str
    objective: str
    instructions: str
    artifact_type: str
    citation_urls: list[str]


@dataclass(frozen=True)
class LeadResponseRolePackDefinition:
    role: str
    title: str
    guardrail_questions: list[str]
    missions: list[LeadResponseMissionDefinition]
    rubric_criteria: list[str]
    allowed_examples: list[str]
    forbidden_examples: list[str]
    policy_citation_urls: list[str]


def lead_response_role_pack_definition() -> LeadResponseRolePackDefinition:
    policy_citations = [
        "https://openai.com/policies/usage-policies/",
        "https://www.ingenuiti.com/ai-usage-policy/",
        "https://www.approachmarketing.com/ai-usage-policy",
        "https://www.salesforce.com/blog/sales/lead-qualification/",
        "https://blog.hubspot.com/sales/ultimate-guide-to-sales-qualification",
        "https://handbook.gitlab.com/handbook/support/workflows/ticket_lifecycle/",
    ]
    return LeadResponseRolePackDefinition(
        role="lead_response_operator",
        title="Lead-response operator public demo role pack",
        guardrail_questions=[
            "Which lead or customer data must be removed before using an AI tool?",
            "When must an AI-assisted response be routed to a human reviewer?",
            "What should the operator do when public sources do not support an answer?",
        ],
        missions=[
            LeadResponseMissionDefinition(
                mission_id="lead-response-acknowledge",
                objective=(
                    "Acknowledge a new inbound lead using only synthetic context."
                ),
                instructions=(
                    "Draft a short acknowledgement, avoid promises about pricing, "
                    "availability, legal terms, or outcomes, and cite public demo "
                    "policy evidence before reuse."
                ),
                artifact_type="lead_acknowledgement",
                citation_urls=[
                    "https://www.ingenuiti.com/ai-usage-policy/",
                    "https://www.approachmarketing.com/ai-usage-policy",
                ],
            ),
            LeadResponseMissionDefinition(
                mission_id="lead-response-qualify",
                objective=(
                    "Qualify a lead with fit, need, authority, budget, and timing."
                ),
                instructions=(
                    "Ask neutral qualification questions, distinguish known facts "
                    "from assumptions, and hand off uncertain business commitments "
                    "to a reviewer."
                ),
                artifact_type="qualification_notes",
                citation_urls=[
                    "https://www.salesforce.com/blog/sales/lead-qualification/",
                    "https://blog.hubspot.com/sales/ultimate-guide-to-sales-qualification",
                ],
            ),
            LeadResponseMissionDefinition(
                mission_id="lead-response-insufficient-evidence",
                objective="Handle unsupported requests with insufficient evidence.",
                instructions=(
                    "Return insufficient_evidence when public policy or workflow "
                    "sources do not support a claim, especially for regulated advice "
                    "or guaranteed outcomes."
                ),
                artifact_type="unsupported_answer_review",
                citation_urls=[
                    "https://openai.com/policies/usage-policies/",
                    "https://aws.amazon.com/ai/responsible-ai/policy/",
                ],
            ),
            LeadResponseMissionDefinition(
                mission_id="lead-response-human-handoff",
                objective=(
                    "Prepare a human-review handoff for a risky or high-value lead."
                ),
                instructions=(
                    "Summarize known facts, missing evidence, risk flags, and the "
                    "specific reviewer decision needed before external follow-up."
                ),
                artifact_type="review_handoff",
                citation_urls=[
                    "https://handbook.gitlab.com/handbook/support/workflows/ticket_lifecycle/",
                    "https://handbook.gitlab.com/handbook/support/workflows/customer_calls/",
                ],
            ),
        ],
        rubric_criteria=[
            "Uses only synthetic lead context and public-source policy evidence.",
            "Separates observed facts from assumptions and missing information.",
            "Cites at least one public source for policy or workflow guidance.",
            "Routes unsupported, regulated, or business-commitment claims to review.",
            "Avoids autonomous approval, pricing, legal, medical, financial, "
            "or compliance advice.",
        ],
        allowed_examples=[
            "Draft a first-pass acknowledgement for reviewer approval.",
            "Summarize synthetic qualification facts and missing evidence.",
            "Suggest neutral follow-up questions for fit, need, authority, "
            "budget, and timing.",
        ],
        forbidden_examples=[
            "Promise a discount, SLA, contract term, implementation date, "
            "or guaranteed outcome.",
            "Give legal, medical, financial, or regulated compliance advice.",
            "Use real customer, employee, lead, or prospect data in public "
            "demo artifacts.",
            "Mark an AI-generated response as approved without human reviewer action.",
        ],
        policy_citation_urls=policy_citations,
    )


def seed_solo_mini_cohort(session: Session) -> SoloMiniCohortData:
    role_pack = lead_response_role_pack_definition()
    workspace_id = "ws-solo-showcase"
    operator_id = "operator-solo"
    reviewer_id = "reviewer-solo"
    learner_id = "learner-solo"
    role_pack_id = "role-pack-lead-response-demo"
    cohort_id = "cohort-solo-lead-response"
    rubric_id = "rubric-lead-response-demo"
    guardrail_quiz_id = "quiz-lead-response-demo"
    policy_snapshot_id = "snapshot-public-demo-policy-v1"

    session.add(Workspace(id=workspace_id, name="Solo Showcase Workspace"))
    session.add_all(
        [
            User(
                id=operator_id,
                workspace_id=workspace_id,
                email="operator.solo@example.test",
                role="operator",
            ),
            User(
                id=reviewer_id,
                workspace_id=workspace_id,
                email="reviewer.solo@example.test",
                role="manager",
            ),
            User(
                id=learner_id,
                workspace_id=workspace_id,
                email="learner.solo@example.test",
                role="learner",
            ),
        ]
    )
    session.add(
        Rubric(
            id=rubric_id,
            workspace_id=workspace_id,
            title="Lead-response public demo rubric",
        )
    )
    session.add(
        GuardrailQuiz(
            id=guardrail_quiz_id,
            workspace_id=workspace_id,
            title="Lead-response public demo guardrails",
            version=1,
            pass_threshold=100,
        )
    )
    session.flush()
    session.add_all(
        [
            GuardrailQuestion(
                id=f"question-lead-response-{index}",
                quiz_id=guardrail_quiz_id,
                workspace_id=workspace_id,
                question_text=question,
                answer_choices=[
                    {"id": "safe", "text": "Use synthetic data and route to review."},
                    {
                        "id": "unsafe",
                        "text": "Use real leads and approve autonomously.",
                    },
                ],
                correct_answer_ids=["safe"],
                explanation="Public demo artifacts require synthetic data and review.",
            )
            for index, question in enumerate(role_pack.guardrail_questions, start=1)
        ]
    )
    session.add(
        RolePack(
            id=role_pack_id,
            workspace_id=workspace_id,
            role=role_pack.role,
            title=role_pack.title,
            version=1,
            launch_status="active",
            created_by=operator_id,
        )
    )
    session.flush()
    mission_ids = [mission.mission_id for mission in role_pack.missions]
    session.add_all(
        [
            MissionTemplate(
                id=mission.mission_id,
                role_pack_id=role_pack_id,
                workspace_id=workspace_id,
                objective=mission.objective,
                instructions=mission.instructions,
                artifact_type=mission.artifact_type,
                rubric_id=rubric_id,
                guardrail_quiz_id=guardrail_quiz_id,
                active=True,
            )
            for mission in role_pack.missions
        ]
    )
    session.add_all(
        [
            SourceDocument(
                id="public-demo-policy-v1",
                logical_document_id="public-demo-policy",
                workspace_id=workspace_id,
                title="Public demo AI policy synthesis",
                document_type="company_policy",
                body_text=(
                    "Public-source demo policy: use synthetic lead data only; "
                    "cite public sources; route unsupported, regulated, or "
                    "business-commitment claims to human review."
                ),
                effective_date=date(2026, 5, 23),
                snapshot_id=policy_snapshot_id,
                version=1,
                created_by=operator_id,
                approval_status="approved",
                approved_by=reviewer_id,
                approved_at=datetime(2026, 5, 23, 10, tzinfo=UTC),
            ),
            SourceDocument(
                id="public-demo-lead-sop-v1",
                logical_document_id="public-demo-lead-sop",
                workspace_id=workspace_id,
                title="Public demo lead-response SOP",
                document_type="sop",
                body_text=(
                    "Acknowledge the synthetic lead, collect qualification "
                    "facts, mark unsupported claims, and prepare human handoff."
                ),
                effective_date=date(2026, 5, 23),
                snapshot_id="snapshot-public-demo-lead-sop-v1",
                version=1,
                created_by=operator_id,
                approval_status="approved",
                approved_by=reviewer_id,
                approved_at=datetime(2026, 5, 23, 10, tzinfo=UTC),
            ),
        ]
    )
    session.add(
        Cohort(
            id=cohort_id,
            workspace_id=workspace_id,
            role_pack_id=role_pack_id,
            role_pack_version=1,
            manager_id=reviewer_id,
            start_date=date(2026, 5, 23),
            due_date=date(2026, 5, 30),
            status="launched",
            created_by=operator_id,
        )
    )
    session.add(
        CohortEnrollment(
            id="enrollment-solo-learner",
            cohort_id=cohort_id,
            workspace_id=workspace_id,
            learner_id=learner_id,
        )
    )
    assignment_ids = [
        "assignment-solo-acknowledge",
        "assignment-solo-qualify",
        "assignment-solo-insufficient-evidence",
        "assignment-solo-human-handoff",
    ]
    session.add_all(
        [
            MissionAssignment(
                id=assignment_id,
                cohort_id=cohort_id,
                workspace_id=workspace_id,
                learner_id=learner_id,
                mission_template_id=mission_id,
                role_pack_version=1,
                status="completed" if index < 2 else "assigned",
            )
            for index, (assignment_id, mission_id) in enumerate(
                zip(assignment_ids, mission_ids, strict=True)
            )
        ]
    )
    submission_ids = ["submission-solo-ack-v1", "submission-solo-qualify-v1"]
    session.add_all(
        [
            Submission(
                id=submission_ids[0],
                workspace_id=workspace_id,
                mission_template_id=mission_ids[0],
                assignment_id=assignment_ids[0],
                learner_id=learner_id,
                artifact_text=(
                    "DEMO DATA: synthetic lead acknowledged; no price, SLA, "
                    "legal, or outcome promise made."
                ),
                policy_snapshot_id=policy_snapshot_id,
                rubric_id=rubric_id,
                version=1,
                review_state="ready_for_manager_review",
                redaction_status="clear",
                approval_status="approved",
                approval_note="Demo reviewer approved source-grounded acknowledgement.",
                manager_id=reviewer_id,
                approved_at=datetime(2026, 5, 23, 11, tzinfo=UTC),
                approved_workflow_change=(
                    "Reuse synthetic-only acknowledgement pattern with reviewer "
                    "approval."
                ),
            ),
            Submission(
                id=submission_ids[1],
                workspace_id=workspace_id,
                mission_template_id=mission_ids[1],
                assignment_id=assignment_ids[1],
                learner_id=learner_id,
                artifact_text=(
                    "DEMO DATA: qualification notes separate known facts from "
                    "assumptions and flag unsupported claims."
                ),
                policy_snapshot_id=policy_snapshot_id,
                rubric_id=rubric_id,
                version=1,
                review_state="needs_human_review",
                redaction_status="clear",
                approval_status="not_reviewed",
            ),
        ]
    )
    feedback_result_ids = ["feedback-solo-ack-v1", "feedback-solo-qualify-v1"]
    session.add_all(
        [
            FeedbackResult(
                id=feedback_result_ids[0],
                workspace_id=workspace_id,
                submission_id=submission_ids[0],
                submission_version=1,
                feedback_status="completed",
                learner_feedback=(
                    "Demo feedback: citation-supported acknowledgement is safe "
                    "for reviewer-approved reuse."
                ),
                validation_status="valid",
                risk_flags=[],
                prompt_version="public-demo-prompt-v1",
                model_version="test-demo-model",
                rubric_version="lead-response-rubric-v1",
                corpus_version="public-demo-corpus-v1",
                feedback_schema_version="feedback-schema-v1",
            ),
            FeedbackResult(
                id=feedback_result_ids[1],
                workspace_id=workspace_id,
                submission_id=submission_ids[1],
                submission_version=1,
                feedback_status="needs_human_review",
                learner_feedback=(
                    "Demo feedback: unsupported conversion or compliance claims "
                    "must be marked insufficient_evidence."
                ),
                validation_status="requires_review",
                risk_flags=["unsupported_claim"],
                prompt_version="public-demo-prompt-v1",
                model_version="test-demo-model",
                rubric_version="lead-response-rubric-v1",
                corpus_version="public-demo-corpus-v1",
                feedback_schema_version="feedback-schema-v1",
            ),
        ]
    )
    report_id = "report-solo-lead-response"
    report_json = {
        "demo_data": True,
        "source_register": "docs/public_corpus/ai_rollout_source_register.md",
        "source_citations": role_pack.policy_citation_urls,
        "limitations": [
            "Synthetic mini-cohort only.",
            "No adoption, productivity, compliance, paid-conversion, or GA claim.",
        ],
        "unsupported_claims": [
            "Productivity lift is unsupported.",
            "Compliance readiness is unsupported.",
            "Enterprise readiness is unsupported.",
        ],
    }
    session.add(
        ProgressReport(
            id=report_id,
            workspace_id=workspace_id,
            cohort_id=cohort_id,
            version=1,
            role_pack_version=1,
            policy_snapshot_id=policy_snapshot_id,
            dashboard_metrics={
                "assignment_count": 4,
                "submission_count": 2,
                "approved_workflow_count": 1,
                "demo_data": True,
            },
            markdown_body=SOLO_MINI_COHORT_REPORT_MARKDOWN,
            json_body=report_json,
            created_by=reviewer_id,
        )
    )
    session.flush()
    return SoloMiniCohortData(
        workspace_id=workspace_id,
        operator_id=operator_id,
        reviewer_id=reviewer_id,
        learner_id=learner_id,
        role_pack_id=role_pack_id,
        cohort_id=cohort_id,
        mission_ids=mission_ids,
        assignment_ids=assignment_ids,
        submission_ids=submission_ids,
        feedback_result_ids=feedback_result_ids,
        approved_submission_id=submission_ids[0],
        report_id=report_id,
        policy_snapshot_id=policy_snapshot_id,
    )


SOLO_MINI_COHORT_REPORT_MARKDOWN = """# Solo Mini-Cohort Replay

Status: demo artifact

This report uses public-source evidence and synthetic learner activity only.
It does not prove adoption, productivity lift, compliance readiness,
enterprise readiness, paid conversion, or GA readiness.

## Demo Data

- Workspace: ws-solo-showcase
- Role pack: lead_response_operator
- Learner count: 1 synthetic learner
- Reviewer count: 1 synthetic manager/reviewer
- Submissions: 2 synthetic submissions
- Approved workflow changes: 1 reviewer-approved demo workflow

## Source Citations

- docs/public_corpus/ai_rollout_source_register.md
- https://openai.com/policies/usage-policies/
- https://www.salesforce.com/blog/sales/lead-qualification/
- https://handbook.gitlab.com/handbook/support/workflows/ticket_lifecycle/

## Limitations

- Synthetic mini-cohort only.
- Public sources are examples, not customer-approved internal policy.
- No private customer, employee, lead, or prospect data is used.
- Browser UX proof remains limited by P2-UX-001 until browser automation exists.

## Unsupported Claims

- Productivity lift is unsupported.
- Compliance readiness is unsupported.
- Enterprise readiness is unsupported.
- Paid conversion is unsupported.
"""


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
