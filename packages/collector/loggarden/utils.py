import traceback
from django.utils.timezone import datetime
from .context import get_context


def normalize_log_record(record):
    context = get_context()

    return {
        "timestamp": datetime.fromtimestamp(record.created).isoformat(),
        "level": record.levelname,
        "message": record.getMessage(),
        "logger_name": record.name,

        "module": record.module,
        "function": record.funcName,
        "line": record.lineno,
        "file": record.pathname,

        "user_id": context.get("user_id"),
        "request_id": context.get("request_id"),

        "path": context.get("path"),
        "method": context.get("method"),
        "ip": context.get("ip"),

        "exception_type": _get_exc_type(record),
        "exception_message": _get_exc_message(record),
        "traceback": _get_traceback(record),

        "extra": _extract_extra(record),
    }


def _get_traceback(record):
    if record.exc_info:
        return "".join(traceback.format_exception(*record.exc_info))
    return None


def _get_exc_type(record):
    if record.exc_info:
        return record.exc_info[0].__name__
    return None


def _get_exc_message(record):
    if record.exc_info:
        return str(record.exc_info[1])
    return None


def _extract_extra(record):

    standard_attrs = {
        "name", "msg", "args", "levelname", "levelno", "pathname",
        "filename", "module", "exc_info", "exc_text", "stack_info",
        "lineno", "funcName", "created", "msecs", "relativeCreated",
        "thread", "threadName", "processName", "process"
    }

    return {
        k: v for k, v in record.__dict__.items()
        if k not in standard_attrs
    }

def normalize_loguru_record(record):
    context = get_context()

    return {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "logger_name": record["name"],

        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
        "file": record["file"].path,

        "user_id": context.get("user_id"),
        "request_id": context.get("request_id"),

        "path": context.get("path"),
        "method": context.get("method"),
        "ip": context.get("ip"),

        "exception_type": _get_exc_type(record),
        "exception_message": _get_exc_message(record),
        "traceback": _get_traceback(record),

        "extra": record.get("extra", {}),
    }


def _get_traceback(record):
    if record["exception"]:
        return str(record["exception"])
    return None


def _get_exc_type(record):
    if record["exception"]:
        return record["exception"].type.__name__
    return None


def _get_exc_message(record):
    if record["exception"]:
        return str(record["exception"].value)
    return None