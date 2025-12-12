import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, String, Text, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Priority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Status(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    assignee: Mapped[str | None] = mapped_column(String(100), nullable=True)
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority), nullable=False, default=Priority.MEDIUM
    )
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.TODO)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="ticket", cascade="all, delete-orphan"
    )


@event.listens_for(Ticket, "before_update")
def ticket_status_change_handler(mapper, connection, target):
    if target.status == Status.DONE and target.closed_at is None:
        target.closed_at = datetime.utcnow()
    elif target.status != Status.DONE and target.closed_at is not None:
        target.closed_at = None
