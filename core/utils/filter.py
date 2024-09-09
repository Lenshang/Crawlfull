from core.db.db_redis import get_redis_client


def url_addfilter(url):
    get_redis_client().sadd("urlfilter", url)


def url_exist(url):
    return get_redis_client().sismember("urlfilter", url) == 1
