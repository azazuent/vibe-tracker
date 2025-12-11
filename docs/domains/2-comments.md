# Domain: Comments

Flat, immutable comments on tickets. No edit, only delete.

## Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, server-generated |
| ticket_id | UUID | FK → tickets.id, ON DELETE CASCADE |
| author | String(100) | NOT NULL |
| content | Text | NOT NULL |
| created_at | DateTime | NOT NULL, server-generated, UTC |

## Endpoints

| Method | Path | Description | Success |
|--------|------|-------------|---------|
| POST | /api/v1/tickets/{ticket_id}/comments | Create | 201 / 404 (ticket) |
| GET | /api/v1/tickets/{ticket_id}/comments | List for ticket | 200 |
| DELETE | /api/v1/tickets/{ticket_id}/comments/{id} | Delete | 204 / 404 |

## Tests

- create_comment_success
- create_comment_ticket_not_found — 404
- create_comment_empty_content — 422
- list_comments
- list_comments_empty
- delete_comment
- delete_comment_not_found — 404

## API Summary

3 endpoints, 7 tests.

```
POST   /api/v1/tickets/{ticket_id}/comments
GET    /api/v1/tickets/{ticket_id}/comments
DELETE /api/v1/tickets/{ticket_id}/comments/{id}
```