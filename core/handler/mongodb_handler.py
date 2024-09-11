from pymongo import MongoClient, UpdateOne
from loguru import logger
from core.model.article_detail import ArticleDetail
import config
import time


class MongoHandler(object):
    def __init__(self, *args, **kwargs):
        self.client = MongoClient(host=config.get("DB", "MONGO_DB"), authMechanism="SCRAM-SHA-1", connect=False)
        self.db = self.client.get_database(config.get("DB", "MONGO_DB_NAME"))
        self.retryCount = 3

    def __new__(cls, *args, **kwargs):
        if not hasattr(MongoHandler, "_instance"):
            MongoHandler._instance = object.__new__(cls)

        return MongoHandler._instance

    def replaceItem(self, collection, item, _count=0):
        try:
            coll = self.db.get_collection(collection)
            return coll.replace_one({"_id": item["_id"]}, item, True)
        except Exception as e:
            if _count < self.retryCount:
                time.sleep(1)
                self.replaceItem(collection, item, _count + 1)
            else:
                logger.error(str(e))
                raise e

    def addOrReplace(self, item: ArticleDetail):
        return self.replaceItem("article_detail", item.to_dict())

    def updateContent(self, id, content, _count=0):
        try:
            coll = self.db.get_collection("article_detail")
            return coll.update_one({"_id": id}, {"$set": {"content": content}}, True)
        except Exception as e:
            if _count < self.retryCount:
                time.sleep(1)
                self.updateContent(id, content, _count + 1)
            else:
                logger.error(str(e))
                raise e

    def getArticle(self, id):
        return self.db.get_collection("article_detail").find_one({"_id": id})
