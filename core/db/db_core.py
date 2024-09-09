from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import config

_Seesion = sessionmaker(
    bind=create_engine(config.get("DB", "CORE_DB"), pool_size=100, pool_recycle=7200), autoflush=False, autocommit=False
)


def get_db() -> Generator[Session, None, None]:
    session = _Seesion()
    try:
        yield session
    finally:
        session.close()


class DbSession:
    def __init__(self) -> None:
        self.session = _Seesion()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, *args):
        try:
            self.session.close()
        except:
            pass
