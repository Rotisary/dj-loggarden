import time
from django.conf import settings
from django.db import transaction

from .queue.factory import get_queue
from .models import LogEntry
from .queue.redis import DeadLetterQueue
from loggarden.config.logs import internal_logger


class LogWorker:
    def __init__(self):
        self.queue = get_queue()
        self.batch_size = getattr(settings, "LOGGARDEN_BATCH_SIZE", 100)
        self.max_retries = getattr(settings, "LOGGARDEN_MAX_RETRIES", 3)
        self.retry_delay = getattr(settings, "LOGGARDEN_RETRY_DELAY", 1.0)
        self.dlq = DeadLetterQueue()

    def run(self):
        try:
            batch = self.queue.dequeue_batch(self.batch_size)
            if batch:
                self._process_batch(batch)
        except Exception as e:
            internal_logger.error(
                "failed to run worker", exc_info=True
            )

    def _process_batch(self, batch):
        for attempt in range(self.max_retries):
            try:
                self._write_batch(batch)
                return
            except Exception as e:
                internal_logger.error(
                    "batch write failed", exc_info=True
                )
                time.sleep(self.retry_delay)

        # after retries exhausted
        self._handle_failed_batch(batch)

    def _write_batch(self, batch):
        objs = [LogEntry(**item) for item in batch]

        with transaction.atomic():
            LogEntry.objects.bulk_create(objs, batch_size=self.batch_size)

    def _handle_failed_batch(self, batch):
        self.dlq.push_batch(batch)