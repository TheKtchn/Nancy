from database import db


class BalanceManager:
    def __init__(self, username) -> None:
        self.username = username
        self.balance = db["balance"]

    def set_balance(self, amount):
        result = self.balance.insert_one(
            {
                "username": self.username,
                "amount": amount,
            }
        )
        return result

    def update_balance(self, amount):
        query = {"username": self.username}
        result = self.balance.update_one(query, {"$set": {"amount": amount}})
        return result

    def get_balance(self):
        query = {"username": self.username}
        result = self.balance.find_one(query)
        return result

    def delete_user_balance(self):
        query = {"username": self.username}
        result = self.balance.delete_one(query)
        return result
