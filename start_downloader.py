from loguru import logger
from core.db.db_core import DbSession
from core.handler.queue_handler import get_download_task, add_parse_task
from core.handler.article_handler import get_article_info
from core.model.article_info import ArticleInfo
from downloader.main import download_task
from downloader.service import create_service
import config
import uvicorn

logger.add("log/downloader/{time}.log", rotation="1 day", retention="7 days")


def debug():
    with DbSession() as db:
        while True:
            r = get_download_task()
            if not r:
                break
            [id, tp] = r.split(" ")
            info = get_article_info(db, id)
            if not info:
                continue
            download_task(db, info, tp)


if __name__ == "__main__":
    # if config.get("COMMON", "ENV") == "dev":
    #     debug()

    app = create_service()
    logger.info("Downloader RestApi start")
    uvicorn.run(app, host=config.get("DOWNLOADER", "DOWNLOADER_SERVICE_HOST"), port=config.getint("DOWNLOADER", "DOWNLOADER_SERVICE_PORT"))
