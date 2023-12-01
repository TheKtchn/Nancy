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
    lower_bound = today - timedelta(days=3 * 30)

    if lower_bound <= parsed_date <= today:
        return True, "Valid date."
    else:
        return (
            False,
            f"Date must be between {lower_bound.strftime('%d-%m-%Y')} and today.\n",
        )


def add_transaction_form(session_mngr: SessionManager, transaction_form: dict):
    item = transaction_form["item"]
    amount = transaction_form["amount"]
    category = transaction_form["category"]
    date = transaction_form["date"]

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

    is_valid_date, error_message = _validate_date(date)
    if not is_valid_date:
        response.is_error = True
        response.message += error_message

    if response.is_error:
        return response

    amount = abs(float(amount))
    result = session_mngr.balance_mngr.get_balance()
    if result is None:
        response.is_error = True
        response.message = "Could not find user balance."

        return response

    current_balance = result["amount"]
    new_balance = -1

    if category == "Expense":
        if amount > current_balance:
            response.is_error = True
            response.message = "Invalid amount.\
                \nAmount entered is greater than balance."

            return response

        else:
            new_balance = current_balance - amount

    elif category == "Income":
        new_balance = current_balance + amount

    result = session_mngr.balance_mngr.update_balance(new_balance)
    if result is None:
        response.is_error = True
        response.message = "Could not update balance of user."
    else:
        response.message = "User's balance has been updated."

    transaction_data = {}
    transaction_data["item"] = item
    transaction_data["amount"] = amount
    transaction_data["category"] = category
    transaction_data["date"] = date

    result = session_mngr.transaction_mngr.create_transaction(transaction_data)
    if result is None:
        response.is_error = True
        response.message = "No transactions exists for user or could not retrieve list."

    else:
        response.message = "Transaction successfully added."

    return response


def retrieve_list_of_transactions_view(session_mngr: SessionManager):
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    result = session_mngr.transaction_mngr.retrieve_transactions()
    if result is None:
        response.is_error = True
        response.message = "No transactions exists for user or could not retrieve list."

        return response

    transactions = ""
    for transaction in result:
        item = transaction["item"]
        amount = transaction["amount"]
        category = transaction["category"]
        date = transaction["date"]

        transactions += f"{item} | {amount} | {category} | {date}\n"

    return response


def set_balance_form(session_mngr: SessionManager, amount):
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    if not _validate_amount(amount):
        response.message += "Invalid amount. Amount entered is not a number.\n"
        response.is_error = True

    amount = abs(float(amount))

    result = session_mngr.balance_mngr.set_balance(amount)
    if result is None:
        response.is_error = True
        response.message = "Could not set balance of user."
    else:
        response.message = "User's balance has been set."

    return response


def get_balance_view(session_mngr: SessionManager):
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    result = session_mngr.balance_mngr.get_balance()
    if result is None:
        response.is_error = True
        response.message = result["balance"]
    else:
        response.message = "User's balance was not available."

    return response
