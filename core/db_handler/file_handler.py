from core.db.db_sqlite import DbSession
from core.model.file_data import FileData
from core.utils.common import md5hex


def add_file(url, content, httpCode, info):
    with DbSession(info.domain) as db:
        id = md5hex(url)
        dbItem = FileData(id=id, url=url, content=content, httpCode=httpCode)
        db.add(dbItem)
        db.commit()
        return id


def get_file(id, info):
    with DbSession(info.domain) as db:
        r = db.query(FileData).filter(FileData.id == id).first()
        if r:
            return r.content
