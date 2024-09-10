from typing import Generator
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from core.model.file_data import FileData
import config
import os


class DbSession:
    def __init__(self, name) -> None:
        full_path = os.path.join(config.get("FS", "FS_BASE_PATH"), name.replace(".", "_") + ".db")
        engine = None
        engine = create_engine("sqlite:///" + full_path, pool_size=100, pool_recycle=7200)

        _Seesion = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        self.session = _Seesion()

        if not inspect(engine).has_table(FileData.__tablename__):
            FileData.metadata.create_all(engine)

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, *args):
        try:
            self.session.close()
        except:
            pass
