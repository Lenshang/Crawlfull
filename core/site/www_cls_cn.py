# 财联社新闻
from core.http.client_request import ClientRequest
from core.site import reg_creator
from core.model.article_info import ArticleInfo
from ExObject.ExObject import ExObject
from urllib.parse import urljoin, urlencode
import config
import json

from core.utils.common import clean_url, md5hex


@reg_creator("www.cls.cn", cron="", enable=True, debug=True)
def crawler(info):
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
                    "domain": info["domain"],
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
