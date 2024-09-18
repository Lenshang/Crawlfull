# 财联社新闻
from core.http.client_request import ClientRequest
from core.model.article_detail import ArticleDetail
from core.model.article_info import ArticleInfo
from core.model.file_data import FileData
from core.model.spider_info import SpiderInfo
from core.utils.htmlparse import article_node_parser, _article_node_parser
from creator import reg_spider
from parser import reg_parser
from ExObject.ExObject import ExObject
from ExObject.ExParsel import ExSelector
from urllib.parse import urljoin, urlencode
import config
import json

from core.utils.common import clean_url, md5hex


@reg_spider("www.cls.cn", cron="0 22 * * ?", enable=True, debug=True)  # 每天22点执行
def crawler(spider_info: SpiderInfo):
    """www.cls.cn"""
    client = ClientRequest()
    urls = [
        f"https://www.cls.cn/v3/depth/home/assembled/1000",
    ]
    for base_url in urls:
        resp = client.get(base_url)
        jObj = ExObject.loadJson(resp.text)
        items = []
        items.extend(jObj["?data"]["?top_article"])
        items.extend(jObj["?data"]["?depth_list"])
        for item in items:
            url = item["?id"].ToCleanString()
            if not url:
                continue
            url = urljoin("https://www.cls.cn/detail/", url)

            dbItem = ArticleInfo(
                **{
                    "id": md5hex(clean_url(url)),
                    "url": url,
                    "domain": spider_info.domain,
                    "title": item["?title"].ToCleanString(),
                    "description": item["?brief"].ToCleanString(),
                }
            )
            addInfo = {}
            pub_date = item["?ctime"].ToOriginal()
            if pub_date:
                dbItem.publishTime = pub_date * 1000
            img = item["?img"].ToCleanString()
            if img:
                addInfo["cover"] = img

            addInfo["source"] = item["?source"].ToCleanString()
            addInfo["reading_num"] = item["?reading_num"].ToCleanString()
            dbItem.addInfo = json.dumps(addInfo)
            yield dbItem


@reg_parser("\/\/www\.cls\.cn\/detail\/")
def parser(parse_info, articleinfo: ArticleInfo, fileinfo: FileData):
    response = fileinfo.content.decode("utf-8")
    item = ArticleDetail.from_article_info(articleinfo)
    selector = ExSelector(response)
    # 解析文章
    contentNode = selector.xpath("//div[@class='clearfix content-main-box']/div[@class='f-l content-left']/node()")

    def filter_node(name, tag: ExSelector):
        cls_str = tag.xpath("@class").FirstOrDefaultString()
        return cls_str in ["m-b-20 f-s-14 l-h-2 c-999 clearfix"]

    def stop_on(name, tag: ExSelector):
        cls_str = tag.xpath("@class").FirstOrDefaultString()
        return cls_str in ["bg-c-fff detail-option-box"]

    content = article_node_parser(contentNode, True, filter=filter_node, stop_on=stop_on)
    item.content = content
    if item.addInfo and item.addInfo.get("source"):
        item.author = item.addInfo["source"]
    return item
