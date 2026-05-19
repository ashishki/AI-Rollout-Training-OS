from pydantic import BaseModel, Field


class RolePackCreate(BaseModel):
    role: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1, max_length=255)


class RolePackRead(BaseModel):
    id: str
    workspace_id: str
    role: str
    title: str
    version: int
    launch_status: str


class MissionCreate(BaseModel):
    objective: str = Field(min_length=1)
    instructions: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1, max_length=64)
    rubric_id: str = Field(min_length=1, max_length=64)
    guardrail_quiz_id: str = Field(min_length=1, max_length=64)


class MissionRead(BaseModel):
    id: str
    role_pack_id: str
    workspace_id: str
    objective: str
    instructions: str
    artifact_type: str
    rubric_id: str
    guardrail_quiz_id: str
    active: bool
