from core.db.db_redis import get_redis_client
from loguru import logger
import traceback

# 基于Redis实现的多WORKER任务队列，
# key为任务类型，value为任务ID
# 修改此处可更换为其他MQ实现


def _add(k, v):
    try:
        client = get_redis_client()
        client.lrem(k, 0, v)
        client.rpush(k, v)
    except Exception as e:
        logger.error(traceback.format_exc())


def _get(k):
    try:
        r = get_redis_client().lpop(k)
        return r.decode("utf-8") if r else None
    except Exception as e:
        logger.error(traceback.format_exc())


def add_download_task(id, type="html"):
    _add("download_task", id + " " + type)


def get_download_task():
    return _get("download_task")


def add_parse_task(id):
    _add("parse_task", id)


def get_parse_task():
    return _get("parse_task")


def add_process_task(id):
    _add("process_task", id)


def get_process_task():
    return _get("process_task")


def add_create_task(id):
    _add("create_task", id)


def get_create_task():
    return _get("process_task")
