from datetime import date

from ai_rollout_os.db.models import SourceDocument
from pydantic import BaseModel, Field

DOCUMENT_TYPES = {
    "company_policy",
    "sop",
    "allowed_use",
    "forbidden_use",
    "approved_example",
}


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    document_type: str = Field(min_length=1, max_length=64)
    body_text: str = Field(min_length=1)
    effective_date: date


class DocumentUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    document_type: str = Field(min_length=1, max_length=64)
    body_text: str = Field(min_length=1)
    effective_date: date


class DocumentRead(BaseModel):
    id: str
    logical_document_id: str
    workspace_id: str
    title: str
    document_type: str
    body_text: str
    effective_date: date
    snapshot_id: str
    version: int


__all__ = [
    "DOCUMENT_TYPES",
    "DocumentCreate",
    "DocumentRead",
    "DocumentUpdate",
    "SourceDocument",
]
