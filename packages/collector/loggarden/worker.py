import time
from django.conf import settings
from django.db import transaction

from .queue.factory import get_queue
from .models import LogEntry


class LogWorker:
    def __init__(self):
        self.queue = get_queue()

        self.batch_size = getattr(settings, "LOGGARDEN_BATCH_SIZE", 100)
        self.flush_interval = getattr(settings, "LOGGARDEN_FLUSH_INTERVAL", 1.0)

        self.max_retries = getattr(settings, "LOGGARDEN_MAX_RETRIES", 3)
        self.retry_delay = getattr(settings, "LOGGARDEN_RETRY_DELAY", 1.0)

    def run(self):
        buffer = []
        last_flush = time.time()

        while True:
            try:
                batch = self.queue.dequeue_batch(self.batch_size)

                if batch:
                    buffer.extend(batch)

                now = time.time()

                should_flush = (
                    len(buffer) >= self.batch_size or
                    (buffer and (now - last_flush) >= self.flush_interval)
                )

                if should_flush:
                    self._process_batch(buffer)
                    buffer.clear()
                    last_flush = now

            except Exception as e:
                pass

    def _process_batch(self, batch):
        for attempt in range(self.max_retries):
            try:
                self._write_batch(batch)
                return

            except Exception as e:
                time.sleep(self.retry_delay)

        # after retries exhausted
        self._handle_failed_batch(batch)

    def _write_batch(self, batch):
        objs = [LogEntry(**item) for item in batch]

        with transaction.atomic():
            LogEntry.objects.bulk_create(objs, batch_size=self.batch_size)

    def _handle_failed_batch(self, batch):
        pass