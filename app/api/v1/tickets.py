import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.models.ticket import Priority, Status, Ticket
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate

router = APIRouter()


@router.post("/tickets", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(**ticket_data.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets", response_model=list[TicketResponse])
def list_tickets(
    assignee: str | None = Query(None),
    status_filter: Status | None = Query(None, alias="status"),
    priority: Priority | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Ticket)

    if assignee:
        query = query.filter(Ticket.assignee == assignee)
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    if priority:
        query = query.filter(Ticket.priority == priority)

    tickets = query.all()
    return tickets


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: uuid.UUID, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: uuid.UUID, ticket_data: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    update_data = ticket_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: uuid.UUID, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
