from database import db


class BalanceDatabaseManager:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.balance = db["balance"][user_id]

    def set_balance(self, amount):
        result = self.balance.insert_one({"amount": amount})
        return result

    def update_balance(self, amount):
        query = {"user_id": self.user_id}
        result = self.balance.update_one(query, {"$set": {"amount": amount}})

        return result

    def get_balance(self):
        query = {"user_id": self.user_id}
        return self.balance.find_one(query)
