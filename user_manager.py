from database import db


class UserManager:
    """
    Manager class for interacting with the 'users' collection in the MongoDB database.
    """

    PRIMARY_KEY = "username"

    def __init__(self) -> None:
        self.users = db["users"]

    def create_user(self, user_data):
        result = self.users.insert_one(user_data)
        return result

    def retrieve_user(self, key):
        query = {self.PRIMARY_KEY: key}
        user = self.users.find_one(query)
        return user

    def update_user(self, key, data):
        query = {self.PRIMARY_KEY: key}
        result = self.users.update_one(query, {"$set": data})
        return result

    def delete_user(self, key):
        query = {self.PRIMARY_KEY: key}
        result = self.users.delete_one(query)
        return result
