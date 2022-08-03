from pymongo import MongoClient


class MongoHandle:
    def __init__(self, db_name, host, port, username, password) -> None:
        self.client = MongoClient(host=host,
                                  port=int(port),
                                  username=username,
                                  password=password)
        self.handle = self.client[db_name]