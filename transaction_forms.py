import re
from datetime import datetime, date, timedelta

from response import Response
from session_data import SessionData

def validate_amount(amount):
    try:
        float(amount)
    except ValueError:
        return False

    return True


def validate_date(date_string):
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


def add_transaction(session_data: SessionData, transaction_form):
    if session_data.is_session:
        description = transaction_form["description"]
        amount = transaction_form["amount"]
        category = transaction_form["category"]
        date = transaction_form["date"]

        response = Response()
        response.data = {}

        if not description:
            response.error_message += (
                "Invalid description. Description cannot be empty.\n"
            )
            response.is_error = True

        if not validate_amount(amount):
            response.error_message += (
                "Invalid amount. Amount entered is not a number.\n"
            )
            response.is_error = True

        is_valid_date, error_message = validate_date(date)
        if not is_valid_date:
            response.error_message += error_message
            response.is_error = True

        if response.is_error:
            return response

        if category == "Expense":
            if amount >session_data.balance_dbm["amount"]:
                response.error_message += (
                    "Invalid amount. Amount entered is greater than balance.\n"
                )
                response.is_error = True
            else:
                session_data.balance_dbm.update_balance(session_data.balance_dbm["amount"] - amount)

        elif category == "Income":
            session_data.balance_dbm.update_balance(session_data.balance_dbm["amount"] + amount)

        if not response.is_error:
            session_data.transactions_dbm.create_transaction(transaction_form)

        return response
