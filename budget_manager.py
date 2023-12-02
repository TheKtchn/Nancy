from database import db, ping


class BudgetManager:
    """
    Manager class for interacting with the 'budgets' collection in the MongoDB database.
    """

    PRIMARY_KEY = "item"

    def __init__(self, user_email) -> None:
        """
        Initializes the BudgetManager instance.

        The 'user_id' attribute is set to the provided user email, and the 'budgets'
        attribute is set to the 'budgets' subcollection for the specific user in the MongoDB database.

        Args:
            user_email (str): The email of the user associated with the budgets.

        Returns:
            None
        """
        self.user_id = user_email
        self.budgets = db["budgets"][user_email]

    def create_budget(self, budget_data):
        """
        Creates a new budget record in the 'budgets' collection for the associated user.

        Args:
            budget_data (dict): The data of the budget to be created.

        Returns:
            pymongo.results.InsertOneResult: The result of the insert operation.
        """
        result = self.budgets.insert_one(budget_data)
        return result

    def retrieve_budget(self, key):
        """
        Retrieves a budget record from the 'budgets' collection based on the provided key.

        Args:
            key (str): The value of the primary key (item) for the budget.

        Returns:
            dict: The budget data if found, None otherwise.
        """
        query = {self.PRIMARY_KEY: key}
        result = self.budgets.find_one(query)
        return result

    def retrieve_budgets(self):
        """
        Retrieves all budget records for the associated user from the 'budgets' collection.

        Returns:
            list: List of budget records for the user.
        """
        budget_records = [record for record in self.budgets.find()]
        return budget_records

    def update_budget(self, key, data):
        """
        Updates a budget record in the 'budgets' collection based on the provided key.

        Args:
            key (str): The value of the primary key (item) for the budget to be updated.
            data (dict): The updated data for the budget.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        query = {self.PRIMARY_KEY: key}
        result = self.budgets.update_one(query, {"$set": data})
        return result

    def delete_budget(self, key):
        """
        Deletes a budget record from the 'budgets' collection based on the provided key.

        Args:
            key (str): The value of the primary key (item) for the budget to be deleted.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        query = {self.PRIMARY_KEY: key}
        result = self.budgets.delete_one(query)
        return result

    def delete_user_budgets(self):
        """
        Deletes all budget records for the associated user from the 'budgets' collection.

        Returns:
            pymongo.results.CollectionDeleteResult: The result of dropping the 'budgets' subcollection.
        """
        result = db.drop_collection(self.budgets)
        return result
