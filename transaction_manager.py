from database import db


class TransactionManager:
    """
    Manager class for interacting with the 'transactions' collection in the MongoDB database.
    """

    def __init__(self, user_email) -> None:
        """
        Initializes the TransactionManager instance.

        The 'user_id' attribute is set to the provided user email, and the 'transactions'
        attribute is set to the 'transactions' subcollection for the specific user in the MongoDB database.

        Args:
            user_email (str): The email of the user associated with the transactions.

        Returns:
            None
        """
        self.user_id = user_email
        self.transactions = db["transactions"][user_email]

    def create_transaction(self, transaction_data):
        """
        Creates a new transaction record in the 'transactions' collection for the associated user.

        Args:
            transaction_data (dict): The data of the transaction to be created.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        result = self.transactions.insert_one(transaction_data)
        return result

    def retrieve_transactions(self):
        """
        Retrieves all transaction records for the associated user from the 'transactions' collection.

        Returns:
            list: List of transaction records for the user.
        """
        transaction_records = [record for record in self.transactions.find()]
        return transaction_records

    def delete_user_transactions(self):
        """
        Deletes all transaction records for the associated user from the 'transactions' collection.

        Returns:
            pymongo.results.CollectionDeleteResult: The result of dropping the 'transactions' subcollection.
        """
        return db.drop_collection(self.transactions)


if __name__ == "__main__":
    transaction_mngr = TransactionManager("someemail@email.com")
    # print("Create transactions:")
    # transaction_mngr.create_transaction({"item": "some thing", "amount": 1000})
    # transaction_mngr.create_transaction({"item": "another thing", "amount": 2000})
    # print()

    # print("Transactions:")
    # print(transaction_mngr.retrieve_transactions())
    # print()

    print("Delete user transactions:")
    print(transaction_mngr.delete_user_transactions())
