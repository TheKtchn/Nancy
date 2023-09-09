import datetime
import json
import os


class Transactions:
    TEMPLATE = {}

    def __init__(self, database_directory) -> None:
        self.transactions_directory = os.path.join(
            database_directory, "transactions.json"
        )
        self.transactions_table = None
        self.read_transactions_table()

    def read_transactions_table(self):
        if os.path.exists(self.transactions_directory):
            with open(self.transactions_directory, "r") as transactions_file:
                self.transactions_table = json.load(transactions_file)
        else:
            self.transactions_table = self.TEMPLATE
            self.write_transactions_table()

    def write_transactions_table(self):
        with open(self.transactions_directory, "w") as transactions_file:
            json.dump(self.transactions_table, transactions_file)

    def add_transaction(self, **transaction):
        if not transaction["Date"]:
            transaction["Date"] = datetime.date().strftime("dd/mm/yyyy")

        self.transactions_table.append(transaction)
        self.write_transactions_table()
