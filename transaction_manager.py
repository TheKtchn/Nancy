from database import db


class TransactionManager:
    """
    Manager class for interacting with the 'transactions' collection in the MongoDB database.
    """

    def __init__(self, username) -> None:
        self.user_id = username
        self.transactions = db["transactions"][username]

    def create_transaction(self, transaction_data):
        result = self.transactions.insert_one(transaction_data)
        return result

    def retrieve_transactions(self):
        transaction_records = [record for record in self.transactions.find()]
        return transaction_records

    def delete_user_transactions(self):
        return db.drop_collection(self.transactions)
