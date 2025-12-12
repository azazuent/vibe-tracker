import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class CommentCreate(BaseModel):
    author: str
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        return v


class CommentResponse(BaseModel):
    id: uuid.UUID
    ticket_id: uuid.UUID
    author: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
