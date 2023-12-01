import re
from datetime import datetime, date, timedelta

from response import Response
from session_manager import SessionManager


def _validate_amount(amount):
    try:
        abs(float(amount))
    except ValueError:
        return False

    return True


def _validate_date(date_string):
    pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    if not pattern.match(date_string):
        return False, "Invalid date format. Please use dd-mm-yyyy.\n"
    try:
        parsed_date = datetime.strptime(date_string, "%d-%m-%Y").date()
    except ValueError:
        return False, "Invalid date. Please enter a valid date.\n"

    today = date.today()
    upper_bound = today + timedelta(days=3 * 30)

    if today <= parsed_date <= upper_bound:
        return True, "Valid date."
    else:
        return (
            False,
            f"Date must be between today and {upper_bound.strftime('%d-%m-%Y')}.\n",
        )


def create_budget_form(session_mngr: SessionManager, budget_create_form: dict):
    item = budget_create_form["item"]
    amount = budget_create_form["amount"]
    due_date = budget_create_form["due_date"]

    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    if not item:
        response.message += "Invalid item. Item cannot be empty.\n"
        response.is_error = True

    if not _validate_amount(amount):
        response.message += "Invalid amount. Amount entered is not a number.\n"
        response.is_error = True

    is_valid_date, error_message = _validate_date(due_date)
    if not is_valid_date:
        response.is_error = True
        response.message += error_message

    if response.is_error:
        return response

    amount = abs(float(amount))
    result = session_mngr.budget_mngr.retrieve_budget(item)
    if result is not None:
        response.is_error = True
        response.message = "Item already exists."

        return response

    budget_data = {}
    budget_data["item"] = item
    budget_data["amount"] = amount
    budget_data["spent"] = 0
    budget_data["due_date"] = due_date

    result = session_mngr.budget_mngr.create_budget(budget_data)

    if result is None:
        response.is_error = True
        response.message = "Budget item could not be created."

    else:
        response.message = "Item has been created."

    return response


def retrieve_list_of_budgets_view(session_mngr: SessionManager):
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    result = session_mngr.budget_mngr.retrieve_budgets()
    if result is None:
        response.is_error = True
        response.message = "No budgets exists for user or could not retrieve list."

        return response

    budgets = ""
    for budget in result:
        item = budget["item"]
        amount = budget["amount"]
        spent = budget["spent"]
        date = budget["due_date"]
        percent = spent / amount

        budgets += f"{item} | {amount} | {spent} | {percent:2f} |{date}\n"

    return response


def update_budget_form(session_mngr: SessionManager, budget_update_form):
    item = budget_update_form["item"]
    amount = budget_update_form["amount"]
    due_date = budget_update_form["due_date"]

    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    if not item:
        response.message += "Invalid item. Item cannot be empty.\n"
        response.is_error = True

    if not _validate_amount(amount):
        response.message += "Invalid amount. Amount entered is not a number.\n"
        response.is_error = True

    is_valid_date, error_message = _validate_date(due_date)
    if not is_valid_date:
        response.is_error = True
        response.message += error_message

    if response.is_error:
        return response

    amount = abs(float(amount))
    result = session_mngr.budget_mngr.retrieve_budget(item)
    if result:
        response.is_error = True
        response.message = "Item does not exists."

        return response

    budget_data = {}
    budget_data["amount"] = amount
    budget_data["spent"] = 0
    budget_data["due_date"] = due_date

    result = session_mngr.budget_mngr.update_budget(item, budget_data)

    if result is None:
        response.is_error = True
        response.message = "Budget item could not be updated."

    else:
        response.message = "Item has been updated."

    return response

def update_budget_spent_form(session_mngr: SessionManager, budget_update_spent_form):
    item = budget_update_spent_form["item"]
    spent = budget_update_spent_form["spent"]
    

    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    if not item:
        response.message += "Invalid item. Item cannot be empty.\n"
        response.is_error = True

    if not _validate_amount(spent):
        response.message += "Invalid amount. Amount entered is not a number.\n"
        response.is_error = True

    if response.is_error:
        return response

    spent = abs(float(spent))
    result = session_mngr.budget_mngr.retrieve_budget(item)
    if result:
        response.is_error = True
        response.message = "Item does not exists."

        return response

    budget_data = {}
    budget_data["spent"] = spent

    result = session_mngr.budget_mngr.update_budget(item, budget_data)
    if result is None:
        response.is_error = True
        response.message = "Budget item spent could not be updated."

    else:
        response.message = "Amount spent on item has been updated."

    return response


def delete_budget_form(session_mngr: SessionManager, item):
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response
    
    if not item:
        response.message = "Invalid item. Item cannot be empty."
        response.is_error = True

        return response
    
    result = session_mngr.budget_mngr.delete_budget(item)
    if result is None:
        response.is_error = True
        response.message = "Could not delete budget item."
    else:
        response.message = f"Deleted {item} from budgets."

    return response

