from database import db


class BudgetManager:
    PRIMARY_KEY = "item"

    def __init__(self, username) -> None:
        self.budgets = db["budgets"][username]

    def create_budget(self, budget_data):
        result = self.budgets.insert_one(budget_data)
        return result

    def retrieve_budget(self, key):
        query = {self.PRIMARY_KEY: key}
        result = self.budgets.find_one(query)
        return result

    def retrieve_budgets(self):
        budget_records = [record for record in self.budgets.find()]
        return budget_records

    def update_budget(self, key, data):
        query = {self.PRIMARY_KEY: key}
        result = self.budgets.update_one(query, {"$set": data})
        return result

    def delete_budget(self, key):
        query = {self.PRIMARY_KEY: key}
        result = self.budgets.delete_one(query)
        return result

    def delete_user_budgets(self):
        result = db.drop_collection(self.budgets)
        return result
