import json
from django.conf import settings

from loggarden.redis_client import get_redis_client


class RedisQueue:
    def __init__(self):
        self.client = get_redis_client()
        self.queue_name = "loggarden:logs"

    def enqueue(self, item):
        try:
            self.client.lpush(
                self.queue_name, json.dumps(item, default=str)
            )
        except:
            pass

    def dequeue_batch(self, max_items):
        items = []

        for _ in range(max_items):
            data = self.client.rpop(self.queue_name)
            if not data:
                break
            items.append(json.loads(data))

        return items