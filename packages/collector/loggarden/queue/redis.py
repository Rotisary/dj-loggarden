import json
from django.conf import settings

from loggarden.redis_client import get_redis_client
from .base import BaseQueue


class RedisQueue(BaseQueue):
    def __init__(self):
        self.client = get_redis_client()
        self.queue_name = "loggarden:logs"
        self.maxsize = getattr(settings, "LOGGARDEN_QUEUE_MAX_SIZE", None)

    def enqueue(self, item):
        try:
            payload = json.dumps(item, default=str)

            pipe = self.client.pipeline()
            pipe.lpush(self.queue_name, payload)

            if self.maxsize:
                pipe.ltrim(self.queue_name, 0, self.maxsize - 1)

            pipe.execute()

        except:
            pass

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