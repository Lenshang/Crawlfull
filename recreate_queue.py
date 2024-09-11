from core.db.db_core import DbSession
from core.handler.queue_handler import add_parse_task, add_download_task
from core.model.article_info import ArticleInfo


if __name__ == "__main__":
    with DbSession() as db:
        r = db.query(ArticleInfo).filter(ArticleInfo.state >= 0, ArticleInfo.state < 3).all()
        for item in r:
            if item.state == 0:
                add_download_task(item.id, "html")
            elif item.state == 1:
                add_parse_task(item.id)
            elif item.state == 2:
                add_download_task(item.id, "content_img")
