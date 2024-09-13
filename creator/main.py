from core.db.db_core import DbSession
from core.handler.node_handler import get_master_node, reg_master_node
from core.handler.queue_handler import add_download_task
from core.model.article_info import ArticleInfo
from core.model.enum import SpiderState
from core.model.spider_info import SpiderInfo
from core.utils.common import clean_url, get_pid_tid, md5hex
from sqlalchemy.orm import Session
from loguru import logger
from creator import get_spider_list
import time
import spiders
import json

NODE_ID = get_pid_tid()


def save_article_info(db: Session, item: ArticleInfo):
    if not item.id:
        item.id = md5hex(clean_url(item.url))
    db.add(item)
    db.commit()
    add_download_task(item.id)


def init_db(db: Session):
    """同步爬虫列表"""
    spider_items = db.query(SpiderInfo).all()
    all_spider_ids_db = [item.id for item in spider_items]
    all_spider_ids_code = list(get_spider_list().keys())
    for key, spider in get_spider_list().items():
        if key not in all_spider_ids_db:
            db.add(
                SpiderInfo(
                    id=key,
                    domain=spider["domain"],
                    description=spider["description"],
                    cron=spider["cron"],
                    maxDepth=spider["max_depth"],
                    downloader=spider["downloader"],
                    parser=spider["parser"],
                    processer=spider["processer"],
                    language=spider["language"],
                    skipMediaDownload=spider["skipMediaDownload"],
                    skipProcess=spider["skipProcess"],
                    enabled=SpiderState.enabled.value if spider["enabled"] else SpiderState.disabled.value,
                    addOptions=json.dumps(spider["addOptions"]),
                )
            )
    for item in spider_items:
        if item.id not in all_spider_ids_code:
            # 当代码中不存在库里已有爬虫时，标记为禁用
            item.enabled = SpiderState.disabled.value

    db.commit()


def start_master_thread():
    # 检查是否为主节点
    init = False
    while True:
        master_node_id = get_master_node()
        if master_node_id == NODE_ID:
            # 做主节点该做的事情
            reg_master_node(NODE_ID)  # 刷新主节点时间
            with DbSession() as db:
                if not init:
                    init_db(db)
            init = True
            pass
        elif not master_node_id:
            # 尝试注册为主节点
            logger.info(f"regist master:{NODE_ID}")
            reg_master_node(NODE_ID)
        else:
            # 其他节点该做的事
            init = True
            pass
        time.sleep(10)
