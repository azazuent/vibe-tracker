import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.comment import Comment
from app.db.models.ticket import Ticket
from app.db.session import get_db
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter()


@router.post(
    "/tickets/{ticket_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
def create_comment(
    ticket_id: uuid.UUID, comment_data: CommentCreate, db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    comment = Comment(ticket_id=ticket_id, **comment_data.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/tickets/{ticket_id}/comments", response_model=list[CommentResponse])
def list_comments(ticket_id: uuid.UUID, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.ticket_id == ticket_id).all()
    return comments


@router.delete(
    "/tickets/{ticket_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(ticket_id: uuid.UUID, comment_id: uuid.UUID, db: Session = Depends(get_db)):
    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.ticket_id == ticket_id)
        .first()
    )
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    db.delete(comment)
    db.commit()
