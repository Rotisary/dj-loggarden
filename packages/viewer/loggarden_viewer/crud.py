from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import LogEntry


def build_query(db: Session, filters: dict):
    query = db.query(LogEntry)

    if filters.get("level"):
        query = query.filter(LogEntry.level.lower() == filters["level"])

    if filters.get("user_id"):
        query = query.filter(LogEntry.user_id == filters["user_id"])

    if filters.get("request_id"):
        query = query.filter(LogEntry.request_id == filters["request_id"])

    if filters.get("search"):
        query = query.filter(LogEntry.message.ilike(f"%{filters['search']}%"))

    if filters.get("start_time"):
        query = query.filter(LogEntry.timestamp >= filters["start_time"])

    if filters.get("end_time"):
        query = query.filter(LogEntry.timestamp <= filters["end_time"])

    return query


def get_logs(db: Session, filters: dict, limit: int, offset: int):
    query = build_query(db, filters)

    return (
        query.order_by(LogEntry.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_log_by_id(db: Session, log_id: int):
    return db.query(LogEntry).filter(LogEntry.id == log_id).first()


def get_level_stats(db: Session):
    return dict(
        db.query(LogEntry.level, func.count())
        .group_by(LogEntry.level)
        .all()
    )