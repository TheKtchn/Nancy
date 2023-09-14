from database import db, ping


class Collection:
    def __init__(self, collection_name: str):
        self.db = db
        self.collection = db[collection_name]

    def create(self, query):
        self.collection.insert_one(query)

    def read(self, query):
        result = self.collection.find_one(query)
        return result is not None
