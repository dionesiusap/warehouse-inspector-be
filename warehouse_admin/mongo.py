from pymongo import ASCENDING, DESCENDING, MongoClient
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import json


class MongoHandle:
    def __init__(self, db_name, host, port) -> None:
        self.client = MongoClient(host=host,
                                  port=int(port))
        self.db = self.client[db_name]


class MongoUtils:
    def __init__(self) -> None:
        pass

    def find(self, collection, query, sort=None):
        cursor = collection.find(query)
        if sort:
            if sort[1] == 0:
                cursor = cursor.sort(sort[0], ASCENDING)
            elif sort[1] == 1:
                cursor = cursor.sort(sort[0], DESCENDING)
        return json.loads(dumps(cursor))
    
    def find_one_by_id(self, collection, id):
        result = collection.find_one({"_id": ObjectId(id)})
        if result is not None:
            return json.loads(dumps(result))
        else:
            return {}


mongo_utils = MongoUtils()
mongo_handle = MongoHandle("warehousedb", "localhost", 27017)