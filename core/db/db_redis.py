import config
from redis import Redis

client = Redis(
    host=config.get("DB", "REDIS_HOST"),
    port=config.get("DB", "REDIS_PORT"),
    db=config.get("DB", "REDIS_DB"),
    password=config.get("DB", "REDIS_PASSWORD"),
)


def get_redis_client() -> Redis:
    return client
