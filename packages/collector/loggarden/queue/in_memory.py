from queue import Queue, Empty

from .base import BaseQueue
from loggarden.config.logs import internal_logger


class MemoryQueue(BaseQueue):
    def __init__(self, maxsize=10000):
        self.queue = Queue(maxsize=maxsize)

    def enqueue(self, item):
        try:
            self.queue.put_nowait(item)
        except:
            internal_logger.error(
                f"Failed to add log_data to memory queue: {item}", exc_info=True
            )

    def dequeue_batch(self, max_items):
        items = []
        for _ in range(max_items):
            try:
                items.append(self.queue.get_nowait())
            except Empty:
                internal_logger.error(
                    "Info: Empty queue", exc_info=True
                )
                break
        return items