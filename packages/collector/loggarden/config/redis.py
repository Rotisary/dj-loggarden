import redis
from django.conf import settings

_redis_client = None


def get_redis_client():
    global _redis_client

    if _redis_client is None:
        redis_url = getattr(settings, "LOGGARDEN_REDIS_URL", "redis://")
        _redis_client = redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )

    return _redis_client