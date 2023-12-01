from database import db


class TransactionManager:
    def __init__(self, user_email) -> None:
        self.user_id = user_email
        self.transactions = db["transactions"][user_email]

    def create_transaction(self, transaction_data):
        result = self.transactions.insert_one(transaction_data)
        return result

    def retrieve_transactions(self):
        transaction_records = [record for record in self.transactions.find()]
        return transaction_records

    def delete_user_transactions(self):
        db.drop_collection(self.transactions)


if __name__ == "__main__":
    transaction_mngr = TransactionManager("someemail@email.com")
    transaction_mngr.create_transaction({"item": "some thing", "amount": 1000})
    transaction_mngr.create_transaction({"item": "another thing", "amount": 2000})
    print(transaction_mngr.retrieve_transactions())
    transaction_mngr.delete_user_transactions()
