from loguru import logger
from core.db.db_core import DbSession
from core.handler.file_handler import add_file
from core.handler.mongodb_handler import MongoHandler
from core.handler.queue_handler import get_download_task, add_parse_task
from core.handler.article_handler import get_article_info
from core.model.article_info import ArticleInfo
from downloader import downloaderMapper
from sqlalchemy.orm import Session
import config
import time


def download_img(info: ArticleInfo):
    client = downloaderMapper.get("default")()
    mongo = MongoHandler()
    detail = mongo.getArticle(info.id)
    if not detail:
        raise Exception("MONGODB文章不存在!")
    content = detail["content"]
    has_img = False
    for ele in content:
        if ele[0] == "img":
            has_img = True
            resp = client.get(ele[1])
            fs_url = add_file(ele[1], resp.content, resp.contentType, resp.code, config.get("DOWNLOADER", "NODE_NAME"))
            ele[1] = fs_url
    if has_img:
        mongo.updateContent(info.id, content)


def download_task(db: Session, info: ArticleInfo, tp: str):

    try:
        if tp == "html":
            _Downloader = None
            if not info.downloader or info.downloader == "default":
                _Downloader = downloaderMapper.get("default")
            else:
                _Downloader = downloaderMapper.get(info.downloader)
                if not _Downloader:
                    raise Exception("下载器不存在!")
            resp = _Downloader().get(info.url)
            fs_url = add_file(info.url, resp.content, resp.contentType, resp.code, config.get("DOWNLOADER", "NODE_NAME"))
            info.content_url = fs_url
            info.state = 1
            logger.info(f"下载完成:{info.url}")
        elif tp == "content_img":
            # TODO 从MONGODB 读取文章 替换文章IMG
            download_img(info)
            info.state = 3
            pass
        else:
            raise Exception("不支持的类型的下载!")
    except Exception as e:
        logger.error(f"下载失败:{info.url} 原因:{e}")
        info.errMsg = str(e)
        info.state = -1
    finally:
        db.commit()
        if tp == "html":
            add_parse_task(info.id)


def start_loop(stop_flag):
    logger.info("Downloader Loop start")
    # 创建单例对象，防止多线程下重复创建对象
    MongoHandler()
    with DbSession() as db:
        while stop_flag.value > 0:
            r = get_download_task()
            if not r:
                time.sleep(3)
                continue
            [id, tp] = r.split(" ")
            info = get_article_info(db, id)
            if not info:
                continue
            download_task(db, info, tp)
