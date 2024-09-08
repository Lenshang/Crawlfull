from loguru import logger
import config

if __name__ == "__main__":
    logger.add("log/downloader/{time}.log", rotation="1 day", retention="7 days")
    logger.info("Downloader Service start")
