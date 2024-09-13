import config

from core.handler.spider_handler import get_spider_info
import spiders
import concurrent.futures
import time
from core.db.db_core import DbSession
from core.handler.queue_handler import add_download_task, get_parse_task
from core.handler.file_handler import get_file
from core.handler.article_handler import get_article_info
from core.handler.mongodb_handler import MongoHandler
from core.model.article_info import ArticleInfo
from core.model.article_detail import ArticleDetail
from parser import get_parser
from loguru import logger
from sqlalchemy.orm import Session
from urllib.parse import urlparse

MAX_THREAD = config.getint("PARSER", "MAX_THREAD")


def save_task(item: ArticleDetail):
    if not item.content or len(item.content) == 0:
        raise Exception("文章内容为空!")
    MongoHandler().addOrReplace(item)


def parse_task(article_id):
    with DbSession() as db:
        try:
            article_info = get_article_info(db, article_id)
            if not article_info or not article_info.content_url:
                raise Exception("找不到对应文章信息,或文章信息中content_url为空!")
            spider_info = get_spider_info(db, article_info.spiderId)
            if not spider_info:
                raise Exception("找不到对应爬虫信息!是否修改过爬虫ID?")
            content_url = urlparse(article_info.content_url)
            download_nodename = content_url.netloc
            download_id = content_url.path[1:]
            file_info = get_file(download_id, download_nodename)
            if not file_info:
                raise Exception("文件系统中找不到对应文件!")
            parser_info = get_parser(article_info)
            if not parser_info:
                raise Exception("找不带对应解析器Parser!")
            result = parser_info["func"](parser_info, article_info, file_info)
            genLinks = None
            if type(result) is tuple:
                result, genLinks = result

            if not parser_info["skip_vertical_crawl"] and genLinks:
                # TODO: 生成更深层链接。
                pass
            if result:
                save_task(result)
            else:
                raise Exception("解析器返回数据为空!")

            # 判断是否跳过图片下载以及解析
            if spider_info.skipMediaDownload == 1:
                if spider_info.skipProcess == 1:
                    article_info.state = 100
                else:
                    article_info.state = 3
            else:
                article_info.state = 2
                # 添加任务到downloader 队列
                add_download_task(article_info.id, "content_img")
        except Exception as e:
            logger.error(e)
            article_info.state = -1
            article_info.errMsg = str(e)
            return
        finally:
            db.commit()


def start_loop():
    logger.info("Parser Loop start")
    # 创建单例对象，防止多线程下重复创建对象
    MongoHandler()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
        while True:
            # 获取任务
            article_ids = []
            for i in range(0, MAX_THREAD):
                article_id = get_parse_task()
                if article_id is None:
                    break
                article_ids.append(article_id)
            if len(article_ids) == 0:
                logger.debug("没有任务,休息3秒...")
                time.sleep(3)
            else:
                results = executor.map(parse_task, article_ids)
                list(results)
