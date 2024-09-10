from core.db.db_redis import get_redis_client
from loguru import logger
import traceback


def add_download_task(id):
    try:
        get_redis_client().rpush("download_task", id)
    except Exception as e:
        logger.error(traceback.format_exc())


def get_download_task():
    try:
        r = get_redis_client().lpop("download_task")
        return r.decode("utf-8") if r else None
    except Exception as e:
        logger.error(traceback.format_exc())


def add_parse_task(id):
    try:
        get_redis_client().rpush("parse_task", id)
    except Exception as e:
        logger.error(traceback.format_exc())


def get_parse_task():
    try:
        r = get_redis_client().lpop("parse_task")
        return r.decode("utf-8") if r else None
    except Exception as e:
        logger.error(traceback.format_exc())
