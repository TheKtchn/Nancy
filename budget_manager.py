from database import db, ping


class BudgetManager:
    PRIMARY_KEY = "item"

    def __init__(self, user_email) -> None:
        self.user_id = user_email
        self.budgets = db["budgets"][user_email]

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
        db.drop_collection(self.budgets)
