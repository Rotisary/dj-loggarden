import logging
from loggarden.utils import normalize_log_record
import logging

from loggarden.queue.factory import get_queue


class LoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.queue = get_queue()

    def emit(self, record):
        try:
            log_data = normalize_log_record(record)
            self.queue.enqueue(log_data)
        except Exception:
            self.handleError(record)