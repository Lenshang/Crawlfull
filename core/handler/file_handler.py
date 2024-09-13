from core.db.db_sqlite import DbSession
from core.db.db_redis import get_redis_client
from core.model.file_data import FileData
from core.utils.common import md5hex, clean_url
from loguru import logger
from threading import RLock
import traceback

lock = RLock()


def add_file(url, content, contentType, httpCode, db_name):
    with lock:
        with DbSession(db_name) as db:
            id = md5hex(clean_url(url))
            dbItem = FileData(id=id, url=url, content=content, contentType=contentType, httpCode=httpCode)
            db.add(dbItem)
            db.commit()
            return f"cffs://{db_name}/{id}"


def get_file(id, db_name):
    with DbSession(db_name) as db:
        r = db.query(FileData).filter(FileData.id == id).first()
        return r
