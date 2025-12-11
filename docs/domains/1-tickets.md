# Domain: Tickets

## Model

| Field | Type | Constraints                     |
|-------|------|---------------------------------|
| id | UUID | PK, server-generated            |
| title | String(255) | NOT NULL                        |
| description | Text | nullable                        |
| assignee | String(100) | nullable                        |
| priority | Enum(LOW, MEDIUM, HIGH) | NOT NULL, default MEDIUM        |
| status | Enum(TODO, IN_PROGRESS, DONE) | NOT NULL, default TODO          |
| due_date | Date | nullable                        |
| created_at | DateTime | NOT NULL, server-generated, UTC |
| closed_at | DateTime | nullable                        |

**Rules:**
- `closed_at` auto-set when status transitions to DONE
- `closed_at` auto-cleared when status transitions from DONE

## Endpoints

| Method | Path | Description | Success | Filters |
|--------|------|-------------|---------|---------|
| POST | /api/v1/tickets | Create | 201 | — |
| GET | /api/v1/tickets | List | 200 | assignee, status, priority |
| GET | /api/v1/tickets/{id} | Get one | 200 / 404 | — |
| PATCH | /api/v1/tickets/{id} | Partial update | 200 / 404 | — |
| DELETE | /api/v1/tickets/{id} | Delete (cascades comments) | 204 / 404 | — |

## Tests

- create_ticket_minimal — only title
- create_ticket_full — all fields
- create_ticket_missing_title — 422
- get_ticket_success
- get_ticket_not_found — 404
- list_tickets_empty
- list_tickets_with_filters — assignee, status, priority
- update_ticket_partial
- update_ticket_status_to_done — verify closed_at set
- update_ticket_status_from_done — verify closed_at cleared
- delete_ticket
- delete_ticket_cascades_comments

## API Summary

5 endpoints, 12 tests.

```
POST   /api/v1/tickets
GET    /api/v1/tickets
GET    /api/v1/tickets/{id}
PATCH  /api/v1/tickets/{id}
DELETE /api/v1/tickets/{id}
```
