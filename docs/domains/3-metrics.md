# Domain: Metrics

Read-only, computed on demand. No persistence.

## Endpoint

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/metrics | Aggregated stats |

## Response Fields

| Field | Type | Notes |
|-------|------|-------|
| todo_count | int | |
| in_progress_count | int | |
| done_count | int | |
| total_count | int | |
| avg_time_to_close_hours | float \| null | null if no closed tickets |

## Tests

- metrics_empty_db — all zeros, avg null
- metrics_counts_correct
- metrics_avg_time_calculation
- metrics_avg_null_when_no_closed

## API Summary

1 endpoint, 4 tests.

```
GET    /api/v1/metrics
```
