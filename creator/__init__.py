import re
import os
import importlib
import traceback
import config
from ExObject.ExParsel import ExSelector
from sqlalchemy.orm import Session
from urllib.parse import urljoin

from core.handler.spider_handler import get_spider_info

_spiders = {}


def reg_spider(
    id,
    domain="",
    cron="",
    description="",
    skipMediaDownload=False,
    skipProcess=False,
    downloader="default",
    parser="default",
    processer="default",
    language="zh-CHS",
    addOptions={},
    enable=True,
    debug=False,
):
    """
    @id: 爬虫ID,请确保唯一性,不然可能出现无法预估的问题 \n
    @domain: 爬虫初始化域名 \n
    @cron: 爬虫初始化cron表达式 \n
    @description: 爬虫描述 \n
    @skipMediaDownload: 是否跳过媒体下载 \n
    @skipProcess: 是否跳过后续处理器 \n
    @downloader: 下载器 默认default \n
    @parser: 解析器 默认default \n
    @processer: 后续处理器 默认default \n
    @language: 抓取站点语言 默认zh-CHS \n
    @addOptions: 额外配置项(dict) \n
    @enable: 是否启用 \n
    @debug: 是否为调试模式
    """

    def decorator(func):
        _spiders[id] = {
            "func": func,
            "id": id,
            "domain": domain if domain else id,
            "cron": cron,
            "description": description,
            "skipMediaDownload": skipMediaDownload,
            "skipProcess": skipProcess,
            "downloader": downloader,
            "parser": parser,
            "processer": processer,
            "language": language,
            "addOptions": addOptions,
            "enable": enable,
            "debug": debug,
        }
        # TODO INIT DB
        return func

    return decorator


def debug_creator(db: Session):
    # TODO 调试模式下创建数据库
    for key in _spiders.keys():
        item = _spiders[key]
        if not item["debug"]:
            pass
        else:
            try:
                spider_info = get_spider_info(db, item["id"])
                for item in item["func"](item):
                    if item:
                        yield item
            except:
                traceback.print_exc()


def get_spider_list() -> dict[str, any]:
    return _spiders
