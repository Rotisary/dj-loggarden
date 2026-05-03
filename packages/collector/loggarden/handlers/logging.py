import logging

from loggarden.queue.factory import get_queue
from loggarden.config.logs import internal_logger
from loggarden.utils import LoggerNormalizer


class LoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.queue = get_queue()

    def emit(self, record):
        try:
            log_data = LoggerNormalizer.normalize_log_record(record)
            self.queue.enqueue(log_data)
        except Exception:
            self.handleError(record)
            internal_logger.error(
                f"Logging handler failed to handle log: {record}", exc_info=True
            )