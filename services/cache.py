import redis
from URL_Shortener.core.config import settings

# Converts byte responses (b"url") directly into Python strings ("url")
r = redis.from_url(settings.REDIS_URL, decode_responses=True)
