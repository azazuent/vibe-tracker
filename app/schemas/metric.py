from pydantic import BaseModel


class MetricsResponse(BaseModel):
    todo_count: int
    in_progress_count: int
    done_count: int
    total_count: int
    avg_time_to_close_hours: float | None
