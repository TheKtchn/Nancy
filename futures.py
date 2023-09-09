import os
import json


class Futures:
    TEMPLATE = {"Credit": {}, "Debt": {}}

    def __init__(self, database_directory) -> None:
        self.futures_directory = os.path.join(database_directory, "futures.json")
        self.futures_table = None
        self.read_futures_table()

    def read_futures_table(self):
        if os.path.exists(self.futures_directory):
            with open(self.futures_directory, "r") as futures_file:
                self.futures_table = json.load(futures_file)
        else:
            self.futures_table = self.TEMPLATE
            self.write_futures_table()

    def write_futures_table(self):
        with open(self.futures_directory, "w") as futures_file:
            json.dump(self.futures_table, futures_file)

    def create_account(self, **account):
        self.futures_table[account["Type"]][account["name"]] = account["Amount"]
        self.write_futures_table()

    def update_account(self, **transaction):
        transact_name = transaction["Name"]
        transact_type = self.find_account(transact_name)
        if transact_type is not None:
            transact_direction = transaction["Direction"]

            transact_amount = (
                transaction["Amount"]
                if transact_direction == "+"
                else -transaction["Amount"]
            )

            self.futures_table[transact_type][transact_name] += transact_amount
            self.write_futures_table()

    def find_account(self, name):
        account_category = None
        categories = ["Credit", "Debt"]

        for category in categories:
            category_name_list = list(self.accounts_table[category].keys())

            if name in category_name_list:
                account_category = category
                break

        return account_category
