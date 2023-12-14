from balance_manager import BalanceManager
from budget_manager import BudgetManager
from response import Response
from transaction_manager import TransactionManager
from utils import validate_amount, validate_date_not_less


def add_transaction(username, transaction):
    description = transaction["description"]
    amount = transaction["amount"]
    category = transaction["category"]
    date = transaction["date"]

    r = Response()

    if not description:
        r.message = "Invalid description. Description cannot be empty."
        r.is_error = True
        return r

    balance_mngr = BalanceManager(username)
    amount = abs(float(amount))
    get_balance_result = balance_mngr.get_balance()

    if get_balance_result is None:
        r.is_error = True
        r.message = "Could not find user balance."
        return r

    current_balance = get_balance_result["amount"]
    new_balance = -1

    if category == "Expense":
        if amount > current_balance:
            r.is_error = True
            r.message = "Invalid amount.\nAmount entered is greater than balance."
            return r
        else:
            new_balance = current_balance - amount

    elif category == "Income":
        new_balance = current_balance + amount

    update_balance_result = balance_mngr.update_balance(new_balance)
    if update_balance_result is None:
        r.is_error = True
        r.message = "Could not update balance of user."
    else:
        r.message = "User's balance has been updated."

    budget_mngr = BudgetManager(username)
    item = description
    retrieve_budget_result = budget_mngr.retrieve_budget(item)

    if retrieve_budget_result is not None:
        current_budget_spent = retrieve_budget_result["spent"]
        budget_data = {"spent": current_budget_spent + amount}
        budget_mngr.update_budget(item, budget_data)

    transaction_mngr = TransactionManager(username)
    transaction_data = {
        "description": description,
        "amount": amount,
        "category": category,
        "date": date,
    }

    create_transaction_result = transaction_mngr.create_transaction(transaction_data)
    if create_transaction_result is None:
        r.is_error = True
        r.message = "Could not add transaction."
    else:
        r.message = "Transaction successfully added."

    return r


def get_transactions(username):
    r = Response()

    transaction_mngr = TransactionManager(username)
    retrieve_transactions_result = transaction_mngr.retrieve_transactions()

    if not retrieve_transactions_result:
        r.is_error = True
        r.message = "No transactions exist for the user."
        return r

    r.data = {"Description": [], "Amount": [], "Category": [], "Date": []}
    for transaction in retrieve_transactions_result:
        r.data["Description"].append(transaction["description"])
        r.data["Amount"].append(transaction["amount"])
        r.data["Category"].append(transaction["category"])
        r.data["Date"].append(transaction["date"])

    r.message = "Retrieved user transactions."
    return r


def set_balance(username, amount):
    r = Response()

    if not validate_amount(amount):
        r.message = "Invalid amount. Amount entered is not a number."
        r.is_error = True
        return r

    amount = abs(float(amount))

    balance_mngr = BalanceManager(username)
    set_balance_result = balance_mngr.set_balance(amount)

    if set_balance_result is None:
        r.is_error = True
        r.message = "Could not set the balance of the user."
    else:
        r.message = "User's balance has been set."

    return r


def get_balance(username):
    r = Response()

    balance_mngr = BalanceManager(username)
    get_balance_result = balance_mngr.get_balance()

    if get_balance_result is None:
        r.is_error = True
        r.message = "User's balance was not available."
    else:
        r.data = get_balance_result["amount"]

    return r
