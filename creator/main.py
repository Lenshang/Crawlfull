from core.handler.queue_handler import add_download_task
from core.model.article_info import ArticleInfo
from core.utils.common import clean_url, md5hex
from sqlalchemy.orm import Session


def save_article_info(db: Session, item: ArticleInfo):
    if not item.id:
        item.id = md5hex(clean_url(item.url))
    db.add(item)
    db.commit()
    add_download_task(item.id)
