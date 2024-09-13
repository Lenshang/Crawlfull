from core.db.db_sqlite import DbSession
from core.db.db_redis import get_redis_client
from core.model.file_data import FileData
from core.utils.common import md5hex, clean_url
from loguru import logger
from threading import RLock
import traceback


def reg_downloader_node(node_name, node_url):
    """注册下载节点信息到REDIS"""
    try:
        get_redis_client().set("downloader_node:" + node_name, node_url)
    except Exception as e:
        logger.error(traceback.format_exc())


def get_downloader_node(node_name):
    """获取下载节点信息"""
    try:
        return get_redis_client().get("downloader_node:" + node_name)
    except Exception as e:
        logger.error(traceback.format_exc())


def reg_master_node(node_name):
    try:
        get_redis_client().set("master_node", node_name, ex=60)
    except Exception as e:
        logger.error(traceback.format_exc())


def get_master_node():
    """获取master节点信息"""
    try:
        return get_redis_client().get("master_node")
    except Exception as e:
        logger.error(traceback.format_exc())
