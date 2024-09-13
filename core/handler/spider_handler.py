from core.db.db_core import DbSession
from sqlalchemy.orm import sessionmaker, Session
from core.model.article_info import ArticleInfo
from core.model.spider_info import SpiderInfo
from loguru import logger
import traceback

spider_cache = {}


def get_spider_info(db: Session, id, force=False):
    try:
        if id in spider_cache and not force:
            return spider_cache[id]
        else:
            spider_info = db.query(SpiderInfo).filter(SpiderInfo.id == id).first()
            spider_cache[id] = spider_info
            return spider_info
    except:
        logger.error(traceback.format_exc())
