import json
from django.conf import settings

from loggarden.config.redis import get_redis_client
from loggarden.config.logs import internal_logger
from .base import BaseQueue


class RedisQueue(BaseQueue):
    def __init__(self, maxsize):
        self.client = get_redis_client()
        self.queue_name = "loggarden:logs"
        self.maxsize = maxsize

    def enqueue(self, item):
        try:
            payload = json.dumps(item, default=str)

            pipe = self.client.pipeline()
            pipe.lpush(self.queue_name, payload)

            if self.maxsize:
                pipe.ltrim(self.queue_name, 0, self.maxsize - 1)

            pipe.execute()

        except Exception as e:
            internal_logger.error(
                f"Failed to add log_data to redis queue: {item}", exc_info=True
            )

    def dequeue_batch(self, max_items):
        items = []

        # block for first item
        first = self.client.brpop(self.queue_name, timeout=1)
        if not first:
            return items

        _, data = first
        items.append(json.loads(data))

        # drain rest without blocking
        for _ in range(max_items - 1):
            data = self.client.rpop(self.queue_name)
            if not data:
                break
            items.append(json.loads(data))

        return items

    
class DeadLetterQueue:
    def __init__(self):
        self.client = get_redis_client()
        self.queue_name = "loggarden:failed_logs"

    def enqueue_batch(self, batch):
        if not batch:
            return

        pipe = self.client.pipeline()
        for item in batch:
            pipe.lpush(self.queue_name, json.dumps(item, default=str))

        pipe.execute()

    def dequeue_batch(self, max_items=100):
        items = []

        first = self.client.brpop(self.queue_name, timeout=1)
        if not first:
            return items

        _, data = first
        items.append(json.loads(data))

        for _ in range(max_items - 1):
            data = self.client.rpop(self.queue_name)
            if not data:
                break
            items.append(json.loads(data))

        return items

    def size(self):
        return self.client.llen(self.queue_name)