# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text, func, Index
from sqlalchemy.dialects.sqlite import INTEGER, BLOB, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileData(Base):
    __tablename__ = "file_data"
    id = Column(String(32), primary_key=True, comment="id")
    url = Column(String(256), nullable=False, comment="URL")
    httpCode = Column(SMALLINT, nullable=False, comment="http状态码")
    contentType = Column(String(64), server_default=text("''"), comment="文件类型")
    content = Column(BLOB, comment="文件内容")
    createdTime = Column(TIMESTAMP, nullable=False, server_default=func.now())
