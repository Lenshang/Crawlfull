from loguru import logger
from core.site import get_creator

logger.add("log/creator/{time}.log", rotation="1 day", retention="7 days")


def start():
    for item in get_creator():
        try:
            # TODO 写数据库
            pass
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    logger.info("Creator Service start")
