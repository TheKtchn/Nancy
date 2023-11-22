from database import db


class TransactionsDatabaseManager:
    def __init__(self, user_email) -> None:
        self.user_id = user_email
        self.transactions = db["transactions"][user_email]

    def create_transaction(self, transaction_data):
        result = self.transactions.insert_one(transaction_data)
        return result

    def retrieve_transactions(self):
        return self.transactions
