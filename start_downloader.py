from loguru import logger
from core.db.db_core import DbSession
from core.db_handler.queue_handler import get_download_task
from core.db_handler.article_handler import get_article_info
from core.model.article_info import ArticleInfo
from downloader.main import download_task
from sqlalchemy.orm import Session
import config

logger.add("log/downloader/{time}.log", rotation="1 day", retention="7 days")


def debug():
    with DbSession() as db:
        while True:
            r = get_download_task()
            if not r:
                continue
            info = get_article_info(db, r)
            if not info:
                continue
            download_task(db, info)


if __name__ == "__main__":
    logger.info("Downloader Service start")
    if config.get("COMMON", "ENV") == "dev":
        debug()
