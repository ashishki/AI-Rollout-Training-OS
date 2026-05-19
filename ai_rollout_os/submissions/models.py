from pydantic import BaseModel, Field

from ai_rollout_os.db.models import Submission


class SubmissionCreate(BaseModel):
    assignment_id: str = Field(min_length=1, max_length=64)
    artifact_text: str = Field(min_length=1)
    policy_snapshot_id: str = Field(min_length=1, max_length=64)
    rubric_id: str = Field(min_length=1, max_length=64)


class SubmissionRead(BaseModel):
    id: str
    workspace_id: str
    mission_template_id: str
    assignment_id: str
    learner_id: str
    artifact_text: str
    policy_snapshot_id: str
    rubric_id: str
    version: int
    review_state: str
    redaction_status: str


class RedactionApprovalCreate(BaseModel):
    note: str = Field(min_length=1)


class ManagerApprovalCreate(BaseModel):
    approval_note: str = Field(min_length=1)
    approved_workflow_change: str = Field(min_length=1)


class ManagerSubmissionRead(BaseModel):
    id: str
    learner_id: str
    mission_id: str
    feedback_status: str
    guardrail_status: str
    risk_flags: list[str]
    approval_status: str
    manager_id: str | None
    approved_at: str | None
    approval_note: str | None
    approved_workflow_change: str | None


__all__ = [
    "ManagerApprovalCreate",
    "ManagerSubmissionRead",
    "RedactionApprovalCreate",
    "Submission",
    "SubmissionCreate",
    "SubmissionRead",
]
