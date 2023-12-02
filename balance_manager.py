from database import db


class BalanceManager:
    """
    Manager class for interacting with the 'balance' collection in the MongoDB database.
    """

    def __init__(self, user_email) -> None:
        """
        Initializes the BalanceManager instance.

        The 'user_email' attribute is set to the provided user email, and the 'balance'
        attribute is set to the 'balance' collection in the MongoDB database.

        Args:
            user_email (str): The email of the user associated with the balance.

        Returns:
            None
        """
        self.user_email = user_email
        self.balance = db["balance"]

    def set_balance(self, amount):
        """
        Sets the balance for the associated user in the 'balance' collection.

        Args:
            amount (float): The balance amount to be set.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        result = self.balance.insert_one(
            {
                "user_email": self.user_email,
                "amount": amount,
            }
        )
        return result

    def update_balance(self, amount):
        """
        Updates the balance for the associated user in the 'balance' collection.

        Args:
            amount (float): The new balance amount.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        query = {"user_email": self.user_email}
        result = self.balance.update_one(query, {"$set": {"amount": amount}})
        return result

    def get_balance(self):
        """
        Retrieves the balance for the associated user from the 'balance' collection.

        Returns:
            dict: The balance data if found, None otherwise.
        """
        query = {"user_email": self.user_email}
        result = self.balance.find_one(query)
        return result

    def delete_user_balance(self):
        """
        Deletes the balance record associated with the user from the 'balance' collection.

        This method removes the balance record for the user identified by the 'user_email'
        attribute from the 'balance' collection in the MongoDB database.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        query = {"user_email": self.user_email}
        result = self.balance.delete_one(query)
        return result


if __name__ == "__main__":
    balance_mngr = BalanceManager("someemail@email.com")

    print(f"Set Balance: {balance_mngr.set_balance(10000)}\n")

    print(f"Get Balance: {balance_mngr.get_balance()}\n")

    print(f"Update Balance: {balance_mngr.update_balance(20000)}\n")

    print(f"Updated Balance: {balance_mngr.get_balance()}\n")

    print(f"Delete User Balance: {balance_mngr.delete_user_balance()}")
