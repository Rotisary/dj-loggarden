from loggarden.queue.factory import get_queue
from loggarden.utils import LoguruNormalizer
from loggarden.config.logs import internal_logger

try:
    from loguru import logger
except ImportError:
    logger = None

queue = get_queue()


def loguru_sink(message):
    try:
        record = message.record
        log_data = LoguruNormalizer.normalize_loguru_record(record)
        queue.enqueue(log_data)
    except Exception:
        internal_logger.error(
            f"Loguru handler failed to handle log: {record}", exc_info=True
        )

def setup_loguru():

    if logger is None:
        raise ImportError(
            "loguru is not installed. Install it with: pip install loguru"
        )
    
    logger.add(loguru_sink)