from loguru import logger
from creator import debug_creator
from core.db.db_core import DbSession
from core.handler.queue_handler import add_download_task
from creator.main import start_master_loop, start_worker_loop
from multiprocessing import Process, Value
import spiders  # 动态加载所有爬虫

logger.add("log/creator/{time}.log", rotation="1 day", retention="7 days")


def start():
    pass


def debug():
    with DbSession() as db:
        for item in debug_creator(db):
            try:
                if item:
                    db.add(item)
                    db.commit()
                    add_download_task(item.id)
            except Exception as e:
                logger.error(e)


if __name__ == "__main__":
    logger.info("Creator Service start")
    running = Value("d", 1)
    loop_process = Process(target=start_master_loop, args=(running,))
    loop_process.start()
    start_worker_loop(running)

    # if config.get("COMMON", "ENV") == "dev":
    #     debug()
