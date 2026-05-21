from pydantic import BaseModel, Field
from datetime import datetime


class LogEntryResponse(BaseModel):
    id: int
    timestamp: datetime
    level: str
    message: str
    logger_name: str

    user_id: str | None
    request_id: str | None
    path: str | None

    class Config:
        from_attributes = True


class LogEntryFilterParams(BaseModel):
    level: str | None = None
    user_id: str | None = None
    request_id: str | None = None
    search: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None