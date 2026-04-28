from queue import Queue, Empty

from .base import BaseQueue


class MemoryQueue(BaseQueue):
    def __init__(self, maxsize=10000):
        self.queue = Queue(maxsize=maxsize)

    def enqueue(self, item):
        try:
            self.queue.put_nowait(item)
        except:
            # drop log if full
            pass

    def dequeue_batch(self, max_items):
        items = []
        for _ in range(max_items):
            try:
                items.append(self.queue.get_nowait())
            except Empty:
                break
        return items