from budget_manager import BudgetManager
from response import Response


def add_budget(username, budget):
    item = budget["item"]
    amount = budget["amount"]
    due_date = budget["due_date"]

    r = Response()

    if not item:
        r.message += "Invalid item. Item cannot be empty."
        r.is_error = True
        return r

    budget_mngr = BudgetManager(username)
    retrieve_budget_result = budget_mngr.retrieve_budget(item)

    if retrieve_budget_result is not None:
        r.is_error = True
        r.message = "Item already exists."
        return r

    budget_data = {"item": item, "amount": amount, "spent": 0, "due_date": due_date}
    create_budget_result = budget_mngr.create_budget(budget_data)

    if create_budget_result is None:
        r.is_error = True
        r.message = "Budget item could not be created."
    else:
        r.message = "Item has been created."

    return r


def get_budgets(username):
    r = Response()

    budget_mngr = BudgetManager(username)
    retrieve_budgets_result = budget_mngr.retrieve_budgets()

    if not retrieve_budgets_result:
        r.is_error = True
        r.message = "No budgets exist for the user."
        return r

    r.data = {"Item": [], "Amount": [], "Spent": [], "Percent": [], "Due Date": []}
    for budget in retrieve_budgets_result:
        r.data["Item"] = budget["item"]
        r.data["Amount"] = budget["amount"]
        r.data["Spent"] = budget["spent"]
        r.data["Percent"] = budget["percent"]
        r.data["Due Date"] = budget["due_date"]

    r.message = "Retrieved user budgets."
    return r


def update_budget(username, budget):
    item = budget["item"]
    amount = budget["amount"]
    due_date = budget["due_date"]

    r = Response()

    if not item:
        r.message += "Invalid item. Item cannot be empty.\n"
        r.is_error = True

    budget_mngr = BudgetManager(username)
    retrieve_budget_result = budget_mngr.retrieve_budget(item)

    if not retrieve_budget_result:
        r.is_error = True
        r.message = "Item does not exist."
        return r

    budget_data = {"amount": amount, "spent": 0, "due_date": due_date}
    update_budget_result = budget_mngr.update_budget(item, budget_data)

    if update_budget_result is None:
        r.is_error = True
        r.message = "Budget item could not be updated."
    else:
        r.message = "Item has been updated."

    return r


def delete_budget(username, item):
    r = Response()

    if not item:
        r.message = "Invalid item. Item cannot be empty."
        r.is_error = True
        return r

    budget_mngr = BudgetManager(username)
    delete_budget_result = budget_mngr.delete_budget(item)

    if delete_budget_result is None:
        r.is_error = True
        r.message = "Could not delete budget item."
    else:
        r.message = f"Deleted {item} from budgets."

    return r
