from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.model.article_info import ArticleInfo
import config

engine = create_engine(config.get("DB", "CORE_DB"), pool_recycle=7200)
Session = sessionmaker(engine)
session = Session()
if __name__ == "__main__":
    ArticleInfo.metadata.create_all(engine)