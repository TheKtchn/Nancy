from database import db


class BalanceManager:
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

    def delete_user_balance(self):
        query = {"user_email": self.user_email}
        self.balance.delete_one(query)


if __name__ == "__main__":
    balance_mngr = BalanceManager("someemail@email.com")
    balance_mngr.set_balance(10000)
    print(balance_mngr.get_balance())
    balance_mngr.update_balance(20000)
    print(balance_mngr.get_balance())
    balance_mngr.delete_user_balance()
