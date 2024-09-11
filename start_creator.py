from loguru import logger
from creator import debug_creator
from core.db.db_core import DbSession
from core.utils.filter import url_addfilter, url_exist
from core.handler.queue_handler import add_download_task
import config
import spiders

logger.add("log/creator/{time}.log", rotation="1 day", retention="7 days")


def start():
    pass


def debug():
    with DbSession() as db:
        for item in debug_creator():
            try:
                if item:
                    db.add(item)
                    db.commit()
                    add_download_task(item.id)
                    # if not url_exist(item.id):
                    #     db.add(item)
                    #     db.commit()
                    #     url_addfilter(item.id)
            except Exception as e:
                logger.error(e)


if __name__ == "__main__":
    logger.info("Creator Service start")
    if config.get("COMMON", "ENV") == "dev":
        debug()
