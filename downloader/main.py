from loguru import logger
from core.db.db_core import DbSession
from core.db_handler.file_handler import add_file, get_file
from core.db_handler.queue_handler import get_download_task
from core.db_handler.article_handler import get_article_info
from core.model.article_info import ArticleInfo
from downloader.downloader_map import downloaderMapper
from sqlalchemy.orm import Session
import config


def download_task(db: Session, info: ArticleInfo):
    logger.info(f"开始下载:{info.url}")
    try:
        _Downloader = None
        if not info.downloader or info.downloader == "default":
            _Downloader = downloaderMapper.get("default")
        else:
            _Downloader = downloaderMapper.get(info.downloader)
            if not _Downloader:
                raise Exception("下载器不存在!")
        resp = _Downloader().get(info.url)
        add_file(info.url, resp.content, resp.status_code, info)

    except Exception as e:
        logger.error(f"下载失败:{info.url}")
