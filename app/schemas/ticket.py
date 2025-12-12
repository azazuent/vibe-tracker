import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.db.models.ticket import Priority, Status


class TicketCreate(BaseModel):
    title: str
    description: str | None = None
    assignee: str | None = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    due_date: date | None = None


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee: str | None = None
    priority: Priority | None = None
    status: Status | None = None
    due_date: date | None = None


class TicketResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    assignee: str | None
    priority: Priority
    status: Status
    due_date: date | None
    created_at: datetime
    closed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
