from django.conf import settings
from .in_memory import MemoryQueue
from .redis import RedisQueue

_queue_instance = None


def get_queue():
    global _queue_instance

    if _queue_instance is not None:
        return _queue_instance

    use_redis = getattr(settings, "LOGGARDEN_USE_REDIS", False)

    if use_redis:
        _queue_instance = RedisQueue()
    else:
        maxsize = getattr(settings, "LOGGARDEN_QUEUE_MAX_SIZE", 10000)
        _queue_instance = MemoryQueue(maxsize=maxsize)

    return _queue_instance