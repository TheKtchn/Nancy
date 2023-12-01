from database import db


class UserManager:
    PRIMARY_KEY = "email"

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


if __name__ == "__main__":
    user_mngr = UserManager()

    user_form = {
        "name": "Halsey Hinata",
        "email": "hh@email.com",
        "password": "halsey123",
    }

    print("Creating user:")
    print(user_mngr.create_user(user_form))

    print("Retrieving user:")
    print(user_mngr.retrieve_user(user_form["email"]))

    print("Updating user:")
    print(user_mngr.update_user(user_form["email"], {"password": "john123"}))
    print("Update user info:")
    print(user_mngr.retrieve_user(user_form["email"]))

    print("Deleting user:")
    print(user_mngr.delete_user(user_form["email"]))
