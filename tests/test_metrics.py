from datetime import datetime, timedelta

from app.db.models.ticket import Status
from tests.factories import TicketFactory


def test_metrics_empty_db(client):
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["todo_count"] == 0
    assert data["in_progress_count"] == 0
    assert data["done_count"] == 0
    assert data["total_count"] == 0
    assert data["avg_time_to_close_hours"] is None


def test_metrics_counts_correct(client, db):
    ticket1 = TicketFactory(status=Status.TODO)
    ticket2 = TicketFactory(status=Status.TODO)
    ticket3 = TicketFactory(status=Status.IN_PROGRESS)
    ticket4 = TicketFactory(status=Status.DONE)
    db.add_all([ticket1, ticket2, ticket3, ticket4])
    db.commit()

    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["todo_count"] == 2
    assert data["in_progress_count"] == 1
    assert data["done_count"] == 1
    assert data["total_count"] == 4


def test_metrics_avg_time_calculation(client, db):
    now = datetime.utcnow()
    ticket1 = TicketFactory(
        status=Status.DONE, created_at=now - timedelta(hours=10), closed_at=now
    )
    ticket2 = TicketFactory(
        status=Status.DONE, created_at=now - timedelta(hours=20), closed_at=now
    )
    db.add_all([ticket1, ticket2])
    db.commit()

    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["avg_time_to_close_hours"] is not None
    assert 14 <= data["avg_time_to_close_hours"] <= 16


def test_metrics_avg_null_when_no_closed(client, db):
    ticket1 = TicketFactory(status=Status.TODO)
    ticket2 = TicketFactory(status=Status.IN_PROGRESS)
    db.add_all([ticket1, ticket2])
    db.commit()

    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["avg_time_to_close_hours"] is None
