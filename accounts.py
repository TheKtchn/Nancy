import os
import json


class Accounts:
    TEMPLATE = {"Expenditure": 0, "Savings": {}, "Goals": {}, "Investments": {}}

    def __init__(self, database_directory) -> None:
        self.accounts_directory = os.path.join(database_directory, "accounts.json")
        self.accounts_table = None
        self.read_accounts_table()

    def read_accounts_table(self):
        if os.path.exists(self.accounts_directory):
            with open(self.accounts_directory, "r") as accounts_file:
                self.accounts_table = json.load(accounts_file)
        else:
            self.accounts_table = self.TEMPLATE
            self.write_accounts_table()

    def write_accounts_table(self):
        with open(self.accounts_directory, "w") as accounts_file:
            json.dump(self.accounts_table, accounts_file)

    def set_expenditure(self, amount: float):
        self.accounts_table["Expenditure"] = amount
        self.write_accounts_table()

    def create_account(self, **account):
        account_Type = None
        account_details = None
        account_name = None

        if account["Type"] == "Savings":
            account_Type = "Savings"
            account_name = account["Name"]
            account_details = {"Amount": account["Amount"]}

        elif account["Type"] == "Goals":
            account_Type = "Goals"
            account_name = account["Name"]
            account_details = {
                "Saved Amount": account["Saved Amount"],
                "Target Amount": account["Target Amount"],
                "Due Date": account["Due Date"],
            }

        elif account["Type"] == "Investments":
            account_Type = "Investments"
            account_name = account["Name"]
            account_details = {
                "Amount": account["Amount"],
                "Interest Rate": account["Interest Rate"],
                "Due Date": account["Due Date"],
            }

        else:
            print("Error: Invalid 'Type' entered.")

        if account_Type is not None:
            self.accounts_table[account_Type][account_name] = account_details

        self.write_accounts_table()

    def update_accounts(self, **transaction):
        if transaction["Type"] == "Income":
            self.accounts_table["Expenditure"] += transaction["Amount"]

        elif transaction["Type"] == "Expense":
            self.accounts_table["Expenditure"] -= transaction["Amount"]

        elif transaction["Type"] == "Deposit":
            account_name = transaction["Name"]
            account_category = self.find_account(account_name)
            self.accounts_table["Expenditure"] -= transaction["Amount"]
            self.accounts_table[account_category][account_name][
                "Amount"
            ] += transaction["Amount"]

        elif transaction["Type"] == "Withdrawal":
            account_name = transaction["Name"]
            account_category = self.find_account(account_name)
            self.accounts_table["Expenditure"] += transaction["Amount"]
            self.accounts_table[account_category][account_name][
                "Amount"
            ] -= transaction["Amount"]

        else:
            print("Error: Invalid 'Type' entered.")

        self.write_accounts_table()

    def delete_account(self, name):
        account_category = self.find_account(name)
        if account_category is not None:
            del self.accounts_table[account_category][name]
            self.write_accounts_table()

    def find_account(self, name):
        account_category = None
        categories = ["Savings", "Investments", "Goals"]

        for category in categories:
            category_name_list = list(self.accounts_table[category].keys())

            if name in category_name_list:
                account_category = category
                break

        return account_category
