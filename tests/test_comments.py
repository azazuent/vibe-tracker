from tests.factories import CommentFactory, TicketFactory


def test_create_comment_success(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={"author": "Alice", "content": "Great work!"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "Alice"
    assert data["content"] == "Great work!"
    assert data["ticket_id"] == str(ticket.id)


def test_create_comment_ticket_not_found(client):
    response = client.post(
        "/api/v1/tickets/00000000-0000-0000-0000-000000000000/comments",
        json={"author": "Alice", "content": "Test"},
    )
    assert response.status_code == 404


def test_create_comment_empty_content(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments", json={"author": "Alice", "content": ""}
    )
    assert response.status_code == 422


def test_list_comments(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    comment1 = CommentFactory(ticket_id=ticket.id, author="Alice")
    comment2 = CommentFactory(ticket_id=ticket.id, author="Bob")
    db.add_all([comment1, comment2])
    db.commit()

    response = client.get(f"/api/v1/tickets/{ticket.id}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_comments_empty(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    response = client.get(f"/api/v1/tickets/{ticket.id}/comments")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_comment(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    comment = CommentFactory(ticket_id=ticket.id)
    db.add(comment)
    db.commit()

    response = client.delete(f"/api/v1/tickets/{ticket.id}/comments/{comment.id}")
    assert response.status_code == 204


def test_delete_comment_not_found(client, db):
    ticket = TicketFactory()
    db.add(ticket)
    db.commit()

    response = client.delete(
        f"/api/v1/tickets/{ticket.id}/comments/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404
