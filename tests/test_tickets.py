from datetime import date

from app.db.models.ticket import Priority, Status, Ticket
from tests.factories import CommentFactory, TicketFactory


def test_create_ticket_minimal(client):
    response = client.post("/api/v1/tickets", json={"title": "Test ticket"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test ticket"
    assert data["priority"] == "MEDIUM"
    assert data["status"] == "TODO"
    assert data["closed_at"] is None


def test_create_ticket_full(client):
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Full ticket",
            "description": "Detailed description",
            "assignee": "John Doe",
            "priority": "HIGH",
            "status": "IN_PROGRESS",
            "due_date": "2025-12-31",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Full ticket"
    assert data["description"] == "Detailed description"
    assert data["assignee"] == "John Doe"
    assert data["priority"] == "HIGH"
    assert data["status"] == "IN_PROGRESS"
    assert data["due_date"] == "2025-12-31"


def test_create_ticket_missing_title(client):
    response = client.post("/api/v1/tickets", json={})
    assert response.status_code == 422


def test_get_ticket_success(client, db):
    ticket = TicketFactory(title="Find me")
    db.add(ticket)
    db.commit()

    response = client.get(f"/api/v1/tickets/{ticket.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Find me"


def test_get_ticket_not_found(client):
    response = client.get("/api/v1/tickets/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_tickets_empty(client):
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tickets_with_filters(client, db):
    ticket1 = TicketFactory(assignee="Alice", status=Status.TODO, priority=Priority.HIGH)
    ticket2 = TicketFactory(assignee="Bob", status=Status.DONE, priority=Priority.LOW)
    ticket3 = TicketFactory(assignee="Alice", status=Status.TODO, priority=Priority.LOW)
    db.add_all([ticket1, ticket2, ticket3])
    db.commit()

    response = client.get("/api/v1/tickets?assignee=Alice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get("/api/v1/tickets?status=TODO")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get("/api/v1/tickets?priority=HIGH")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_update_ticket_partial(client, db):
    ticket = TicketFactory(title="Old title", assignee="Alice")
    db.add(ticket)
    db.commit()

    response = client.patch(f"/api/v1/tickets/{ticket.id}", json={"title": "New title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["assignee"] == "Alice"


def test_update_ticket_status_to_done(client, db):
    ticket = TicketFactory(status=Status.IN_PROGRESS, closed_at=None)
    db.add(ticket)
    db.commit()

    response = client.patch(f"/api/v1/tickets/{ticket.id}", json={"status": "DONE"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DONE"
    assert data["closed_at"] is not None


def test_update_ticket_status_from_done(client, db):
    ticket = TicketFactory(status=Status.TODO)
    db.add(ticket)
    db.commit()

    client.patch(f"/api/v1/tickets/{ticket.id}", json={"status": "DONE"})

    response = client.patch(f"/api/v1/tickets/{ticket.id}", json={"status": "IN_PROGRESS"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "IN_PROGRESS"
    assert data["closed_at"] is None


def test_delete_ticket(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    response = client.delete(f"/api/v1/tickets/{ticket.id}")
    assert response.status_code == 204

    ticket_in_db = db.query(Ticket).filter(Ticket.id == ticket.id).first()
    assert ticket_in_db is None


def test_delete_ticket_cascades_comments(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    comment = CommentFactory(ticket_id=ticket.id)
    db.add(comment)
    db.commit()

    response = client.delete(f"/api/v1/tickets/{ticket.id}")
    assert response.status_code == 204

    comments_response = client.get(f"/api/v1/tickets/{ticket.id}/comments")
    assert comments_response.status_code == 200
    assert comments_response.json() == []
