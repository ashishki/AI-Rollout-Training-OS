from datetime import date

from ai_rollout_os.db.models import Cohort, CohortEnrollment, MissionAssignment
from pydantic import BaseModel, Field


class CohortCreate(BaseModel):
    role_pack_id: str = Field(min_length=1, max_length=64)
    role_pack_version: int = Field(ge=1)
    manager_id: str = Field(min_length=1, max_length=64)
    learner_ids: list[str] = Field(default_factory=list)
    start_date: date
    due_date: date


class CohortRead(BaseModel):
    id: str
    workspace_id: str
    role_pack_id: str
    role_pack_version: int
    manager_id: str
    start_date: date
    due_date: date
    status: str
    learner_ids: list[str]


class AssignmentRead(BaseModel):
    id: str
    cohort_id: str
    learner_id: str
    mission_template_id: str
    role_pack_version: int
    status: str


__all__ = [
    "AssignmentRead",
    "Cohort",
    "CohortCreate",
    "CohortEnrollment",
    "CohortRead",
    "MissionAssignment",
]
