from core.db.db_core import DbSession
from sqlalchemy.orm import sessionmaker, Session
from core.model.article_info import ArticleInfo
from loguru import logger
import traceback


def get_article_info(db: Session, id):
    try:
        return db.query(ArticleInfo).filter(ArticleInfo.id == id).first()
    except:
        logger.error(traceback.format_exc())
