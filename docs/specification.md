# Vibe Tracker Backend — Technical Specification

## Overview

Lightweight REST API for task tracking. Prototype — no auth, single-tenant.

**Stack:** Python 3.12, FastAPI, Pydantic, SQLAlchemy 2.x (sync), PostgreSQL 16, pytest, Docker Compose

**Patterns:**
- Sync SQLAlchemy with sync FastAPI endpoints
- pydantic-settings for configuration
- No migrations — `create_all()` on startup
- Pydantic v2 schemas

---

## Configuration

Manage via pydantic-settings `Settings` class in `config.py`.

| Variable | Type | Default                                                   | Description |
|----------|------|-----------------------------------------------------------|-------------|
| database_url | str | postgresql://postgres:postgres@localhost:5432/vibetracker | Connection string |
| debug | bool | false                                                     | Debug mode |

Settings loaded from environment variables with `.env` file support.

---

## Project Structure

```
vibe-tracker/
├── README.md
├── .gitignore
├── pyproject.toml
├── Dockerfile
├── .dockerignore
├── compose.yml
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py   # Environment settings
│   │   └── ...
│   ├── db/
│   │   ├── session.py  # Database setup
│   │   └── models/     # Database models
│   ├── schemas/        # DTOs
│   └── api/            # API routes
│       └── ...
└── tests/
    └── ...
```

---

## Dependencies

**Runtime:** fastapi, uvicorn[standard], sqlalchemy, psycopg2-binary, pydantic, pydantic-settings

**Dev:** pytest, httpx, factory-boy, ruff

---

## Testing

- Use in-memory SQLite for tests
- Override database dependency in conftest
- factory-boy for model factories
- httpx TestClient for API tests

---

## CI/CD

GitHub Actions workflow in `.github/workflows/test.yml`

**Triggers:**
- Push to `main`, `dev`
- Pull requests to `main`, `dev`

**Job: test**
- Runs on: ubuntu-latest
- Python 3.12
- Install dependencies from pyproject.toml (including dev)
- Run pytest

No deployment — tests only.

---

## Docker

**Dockerfile:** Python 3.12 slim, install from pyproject.toml, run uvicorn on port 8000

**docker-compose.yml:**
- `api` service: builds from Dockerfile, depends on db, exposes 8000
- `db` service: postgres:16-alpine, healthcheck, persistent volume
