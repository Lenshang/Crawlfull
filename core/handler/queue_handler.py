from core.db.db_redis import get_redis_client
from loguru import logger
import traceback


def add(k, v):
    try:
        client = get_redis_client()
        client.lrem(k, 0, v)
        client.rpush(k, v)
    except Exception as e:
        logger.error(traceback.format_exc())


def add_download_task(id, type="html"):
    add("download_task", id + " " + type)


def get_download_task():
    try:
        r = get_redis_client().lpop("download_task")
        return r.decode("utf-8") if r else None
    except Exception as e:
        logger.error(traceback.format_exc())


def add_parse_task(id):
    add("parse_task", id)


def get_parse_task():
    try:
        r = get_redis_client().lpop("parse_task")
        return r.decode("utf-8") if r else None
    except Exception as e:
        logger.error(traceback.format_exc())
