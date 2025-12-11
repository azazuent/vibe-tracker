from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.ticket import Status, Ticket
from app.db.session import get_db
from app.schemas.metric import MetricsResponse

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics(db: Session = Depends(get_db)):
    todo_count = db.query(Ticket).filter(Ticket.status == Status.TODO).count()
    in_progress_count = db.query(Ticket).filter(Ticket.status == Status.IN_PROGRESS).count()
    done_count = db.query(Ticket).filter(Ticket.status == Status.DONE).count()
    total_count = db.query(Ticket).count()

    closed_tickets = db.query(Ticket).filter(Ticket.closed_at.isnot(None)).all()

    avg_time_to_close_hours = None
    if closed_tickets:
        total_hours = sum(
            (ticket.closed_at - ticket.created_at).total_seconds() / 3600
            for ticket in closed_tickets
        )
        avg_time_to_close_hours = total_hours / len(closed_tickets)

    return MetricsResponse(
        todo_count=todo_count,
        in_progress_count=in_progress_count,
        done_count=done_count,
        total_count=total_count,
        avg_time_to_close_hours=avg_time_to_close_hours,
    )
