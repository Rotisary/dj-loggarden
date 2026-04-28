from abc import ABC, abstractmethod


class BaseQueue(ABC):
    @abstractmethod
    def enqueue(self, item: dict):
        pass

    @abstractmethod
    def dequeue_batch(self, max_items: int):
        pass