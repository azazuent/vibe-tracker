from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import comments, metrics, tickets
from app.db.models import Comment, Ticket  # noqa: F401
from app.db.session import create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all()
    yield


app = FastAPI(
    title="Vibe Tracker",
    description="Lightweight REST API for task tracking",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router, prefix="/api/v1", tags=["tickets"])
app.include_router(comments.router, prefix="/api/v1", tags=["comments"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])


@app.get("/")
def health_check():
    return {"status": "ok"}
