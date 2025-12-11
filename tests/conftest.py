from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import Comment, Ticket  # noqa: F401
from app.db.session import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Replace lifespan with a no-op for tests
@asynccontextmanager
async def test_lifespan(app: FastAPI):
    yield


app.router.lifespan_context = test_lifespan
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def cleanup():
    yield
    # Clean up all data after each test
    db = TestingSessionLocal()
    try:
        db.query(Comment).delete()
        db.query(Ticket).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client
