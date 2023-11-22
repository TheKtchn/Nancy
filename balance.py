from database import db


class BalanceDatabaseManager:
    def __init__(self, user_email) -> None:
        self.user_email = user_email
        self.balance = db["balance"]

    def set_balance(self, amount):
        result = self.balance.insert_one(
            {"user_email": self.user_email, "amount": amount}
        )
        return result

    def update_balance(self, amount):
        query = {"user_email": self.user_email}
        result = self.balance.update_one(query, {"$set": {"amount": amount}})

        return result

    def get_balance(self):
        query = {"user_email": self.user_email}
        return self.balance.find_one(query)
