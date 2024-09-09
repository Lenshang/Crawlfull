# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text, func, Index
from sqlalchemy.dialects.mysql import TINYINT, BIGINT, TEXT
from core.model import Base


class ArticleInfo(Base):
    __tablename__ = "article_info"
    id = Column(String(32), primary_key=True, comment="文章id")
    url = Column(String(256), nullable=False, comment="文章URL")
    domain = Column(String(64), nullable=False, comment="站点Domain", index=True)
    title = Column(String(256), server_default=text("''"), comment="文章标题")
    description = Column(String(256), server_default=text("''"), comment="文章描述")
    publishTime = Column(BIGINT(13), nullable=False, comment="文章发布时间 13位时间戳", index=True)
    author = Column(String(64), server_default=text("''"), comment="文章作者")
    language = Column(String(10), server_default=text("'zh-Hans'"), comment="文章语言")
    addInfo = Column(TEXT, nullable=True, comment="额外信息(json格式)")
    state = Column(
        TINYINT(3), server_default=text("'0'"), nullable=False, index=True, comment="状态 0=初始化 1=已抓取 2=已解析入库 -1=抓取失败"
    )
    downloader = Column(String(16), server_default=text("'default'"), comment="下载器,默认default为request下载器")
    parser = Column(String(16), server_default=text("'default'"), comment="解析器,默认default则走URL正则匹配")
    errMsg = Column(String(255), nullable=True, comment="错误信息")
    createdTime = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updateTime = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (Index("domain_publishTime", "domain", "publishTime"),)