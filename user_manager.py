from database import db


class UserManager:
    """
    Manager class for interacting with the 'users' collection in the MongoDB database.
    """

    PRIMARY_KEY = "email"

    def __init__(self) -> None:
        """
        Initializes the UserManager instance.

        The 'users' attribute is set to the 'users' collection in the MongoDB database.

        Returns:
            None
        """
        self.users = db["users"]

    def create_user(self, user_data):
        """
        Creates a new user in the 'users' collection.

        Args:
            user_data (dict): The data of the user to be created.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        result = self.users.insert_one(user_data)
        return result

    def retrieve_user(self, key):
        """
        Retrieves a user from the 'users' collection based on the provided key.

        Args:
            key (str): The value of the primary key (email) for the user.

        Returns:
            dict: The user data if found, None otherwise.
        """
        query = {self.PRIMARY_KEY: key}
        user = self.users.find_one(query)
        return user

    def update_user(self, key, data):
        """
        Updates a user in the 'users' collection based on the provided key.

        Args:
            key (str): The value of the primary key (email) for the user to be updated.
            data (dict): The updated data for the user.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        query = {self.PRIMARY_KEY: key}
        result = self.users.update_one(query, {"$set": data})
        return result

    def delete_user(self, key):
        """
        Deletes a user from the 'users' collection based on the provided key.

        Args:
            key (str): The value of the primary key (email) for the user to be deleted.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        query = {self.PRIMARY_KEY: key}
        result = self.users.delete_one(query)
        return result


if __name__ == "__main__":
    user_mngr = UserManager()

    user_form = {
        "name": "John Jones",
        "email": "jj@email.com",
        "password": "john123",
    }

    print("Creating user:")
    print(user_mngr.create_user(user_form))
    print()

    print("Retrieving user:")
    print(user_mngr.retrieve_user(user_form["email"]))
    print()

    print("Updating user:")
    print(
        user_mngr.update_user(
            user_form["email"], {"name": "Janet Jules", "password": "janet123"}
        )
    )
    print("Updated user info:")
    print(user_mngr.retrieve_user(user_form["email"]))
    print()

    print("Deleting user:")
    print(user_mngr.delete_user(user_form["email"]))
    print()

    print("Retrieving non-existent user:")
    print(user_mngr.retrieve_user(user_form["email"]))
    print()

    print("Deleting non-existent user:")
    print(user_mngr.delete_user(user_form["email"]))
    print()

    print("Updating non_existent user:")
    print(user_mngr.update_user(user_form["email"], {"password": "john123"}))
