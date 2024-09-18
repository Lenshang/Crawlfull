from core.db.db_core import DbSession
from core.handler.node_handler import get_master_node, reg_master_node
from core.handler.queue_handler import add_download_task, add_create_task, get_create_task
from core.handler.spider_handler import get_spider_info
from core.model.article_info import ArticleInfo
from core.model.enum import SpiderState
from core.model.spider_info import SpiderInfo
from core.utils.common import clean_url, get_pid_tid, md5hex, get_next_runtime, now_ts
from sqlalchemy.orm import Session
from loguru import logger
from core.utils.filter import url_addfilter, url_exist
from creator import get_spider_list
from croniter import croniter
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
                    nextRunTime=get_next_runtime(spider["cron"], now_ts()) if spider["cron"] else -1,
                    enable=SpiderState.enable.value if spider["enable"] else SpiderState.disabled.value,
                    addOptions=json.dumps(spider["addOptions"]),
                )
            )
    for item in spider_items:
        if item.id not in all_spider_ids_code:
            # 当代码中不存在库里已有爬虫时，标记为禁用
            item.enable = SpiderState.disabled.value

    db.commit()


def _master(db: Session):
    """主节点：从数据库中获取需要执行的爬虫任务，并添加到队列中"""
    now = now_ts()
    for item in (
        db.query(SpiderInfo)
        .filter(SpiderInfo.enable == SpiderState.enable.value, SpiderInfo.nextRunTime <= now, SpiderInfo.nextRunTime > 0)
        .all()
    ):
        if not item.cron:
            continue
        add_create_task(item.id)
        item.nextRunTime = get_next_runtime(item.cron, item.nextRunTime)
    db.commit()


def _worker(db: Session, func, spider_info: SpiderInfo):
    for item in func(spider_info):
        try:
            if item:
                item.spiderId = spider_info.id
                if not url_exist(item.id):
                    db.add(item)
                    db.commit()
                    url_addfilter(item.id)
        except Exception as e:
            logger.error(e)


def start_master_loop(stop_flag):
    """自动选举主节点，定时查询数据进行任务分发工作"""
    logger.info("Spider AutoMaster Loop start")
    # 检查是否为主节点
    init = False
    while stop_flag.value > 0:
        master_node_id = get_master_node()
        if master_node_id == NODE_ID:
            # 做主节点该做的事情
            reg_master_node(NODE_ID)  # 刷新主节点时间
            with DbSession() as db:
                if not init:
                    init_db(db)
                _master(db)
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
        time.sleep(5)


def start_worker_loop(stop_flag):
    """爬虫任务消费队列"""
    logger.info("Spider Worker Loop start")
    with DbSession() as db:
        while stop_flag.value > 0:
            try:
                r = get_create_task()
                if not r:
                    time.sleep(3)
                    continue
                func_info = get_spider_list().get(r)
                if not func_info:
                    logger.error(f"spider func not found:{r}")
                    continue
                spider_info = get_spider_info(db, r)
                _worker(db, func_info["func"], spider_info)
            except Exception as e:
                logger.error(e)
