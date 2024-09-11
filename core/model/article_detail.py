from dataclasses import dataclass, field
from core.model.article_info import ArticleInfo
from .item import CrawlfItem
import json


@dataclass
class ArticleDetail(CrawlfItem):
    _id: str = field(default="")
    title: str = field(default="")
    content: list = field(default=None)
    author: str = field(default="")
    publishTime: int = field(default=None)
    domain: str = field(default="")
    url: str = field(default="")
    content_url: str = field(default="")
    addInfo: dict = field(default=None)

    @staticmethod
    def from_article_info(articleinfo: ArticleInfo):
        _item = ArticleDetail()
        _item._id = articleinfo.id
        _item.title = articleinfo.title
        _item.author = articleinfo.author
        _item.publishTime = articleinfo.publishTime
        _item.domain = articleinfo.domain
        _item.url = articleinfo.url
        _item.content_url = articleinfo.content_url
        if articleinfo.addInfo:
            try:
                _item.addInfo = json.loads(articleinfo.addInfo)
            except:
                _item.addInfo = {"_raw": articleinfo.addInfo}
        return _item
