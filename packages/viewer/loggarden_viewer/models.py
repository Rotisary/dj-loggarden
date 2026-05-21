from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LogEntry(Base):
    __tablename__ = "loggarden_logentry"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    level = Column(String(32), index=True)
    message = Column(Text)
    logger_name = Column(String(255))

    user_id = Column(String(255), index=True)
    request_id = Column(String(128), index=True)

    path = Column(Text)
    method = Column(String(16))
    ip = Column(String)

    module = Column(String(255))
    function = Column(String(255))
    line = Column(Integer)
    file = Column(Text)

    exception_type = Column(String(255))
    exception_message = Column(Text)
    traceback = Column(Text)

    # extra = Column(JSONB)