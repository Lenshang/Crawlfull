# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text, func, Index
from sqlalchemy.dialects.mysql import TINYINT, BIGINT, TEXT
from core.model import Base


class SpiderInfo(Base):
    __tablename__ = "spider_info"
    id = Column(String(32), primary_key=True, comment="爬虫ID")
    domain = Column(String(64), nullable=False, comment="站点Domain", index=True)
    description = Column(String(256), server_default=text("''"), comment="站点描述描述")
    language = Column(String(10), server_default=text("'zh-CHS'"), comment="站点语言")
    downloader = Column(String(16), server_default=text("'default'"), comment="下载器,默认default为request下载器")
    parser = Column(String(16), server_default=text("'default'"), comment="解析器,默认default则走URL正则匹配")
    processer = Column(String(16), server_default=text("'default'"), comment="后续处理器,默认default则走默认文章分类提取以及关键词提取")
    maxDepth = Column(TINYINT(1), server_default=text("'0'"), comment="最大抓取深度")
    cron = Column(String(64), server_default=text("''"), comment="cron表达式")
    nextRunTime = Column(BIGINT(13), nullable=False, comment="下次运行时间 13位时间戳")
    skipMediaDownload = Column(TINYINT(1), server_default=text("'0'"), comment="是否跳过媒体下载 0=否 1=是")
    skipProcess = Column(TINYINT(1), server_default=text("'0'"), comment="是否跳过后续处理器 0=否 1=是")
    enabled = Column(TINYINT(1), server_default=text("'1'"), comment="是否启用 0=否 1=是")
    addOptions = Column(TEXT, nullable=True, comment="额外配置(json格式)")
    createdTime = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updateTime = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
