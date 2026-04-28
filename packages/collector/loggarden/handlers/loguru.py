from loguru import logger
from loggarden.queue.factory import get_queue
from loggarden.utils import normalize_loguru_record

queue = get_queue()


def loguru_sink(message):
    try:
        record = message.record
        log_data = normalize_loguru_record(record)
        queue.enqueue(log_data)
    except Exception:
        pass


def setup_loguru():
    logger.add(loguru_sink)