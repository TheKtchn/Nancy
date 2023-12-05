from response import Response
from session_manager import SessionManager
from utils import validate_amount, validate_date_not_less


def add_transaction_form(
    session_mngr: SessionManager, transaction_form: dict
) -> Response:
    """
    Adds a transaction based on the provided transaction form.

    Args:
        session_mngr (SessionManager): The session manager instance.
        transaction_form (dict): The transaction form containing transaction data.

    Returns:
        Response: A response object indicating the result of the transaction addition.
    """
    item = transaction_form["item"]
    amount = transaction_form["amount"]
    category = transaction_form["category"]
    date = transaction_form["date"]

    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Validate item
    if not item:
        response.message += "Invalid item. Item cannot be empty.\n"
        response.is_error = True

    # Validate amount
    if not validate_amount(amount):
        response.message += "Invalid amount. Amount entered is not a number.\n"
        response.is_error = True

    # Validate date
    is_valid_date, error_message = validate_date_not_less(date)
    if not is_valid_date:
        response.is_error = True
        response.message += error_message

    if response.is_error:
        return response

    amount = abs(float(amount))
    get_balance_result = session_mngr.balance_mngr.get_balance()

    # Check if the user's balance exists
    if get_balance_result is None:
        response.is_error = True
        response.message = "Could not find user balance."
        return response

    current_balance = get_balance_result["amount"]
    new_balance = -1

    # Update the balance based on the transaction category
    if category == "Expense":
        if amount > current_balance:
            response.is_error = True
            response.message = (
                "Invalid amount.\nAmount entered is greater than balance."
            )
            return response
        else:
            new_balance = current_balance - amount
    elif category == "Income":
        new_balance = current_balance + amount

    # Update the user's balance
    update_balance_result = session_mngr.balance_mngr.update_balance(new_balance)
    if update_balance_result is None:
        response.is_error = True
        response.message = "Could not update balance of user."
    else:
        response.message = "User's balance has been updated."

    # Create transaction data
    transaction_data = {
        "item": item,
        "amount": amount,
        "category": category,
        "date": date,
    }

    # Create the transaction
    create_transaction_result = session_mngr.transaction_mngr.create_transaction(
        transaction_data
    )
    if create_transaction_result is None:
        response.is_error = True
        response.message = (
            "No transactions exist for the user or could not retrieve the list."
        )
    else:
        response.message = "Transaction successfully added."

    return response


def retrieve_list_of_transactions_view(session_mngr: SessionManager) -> Response:
    """
    Retrieves a list of transactions for the user associated with the active session.

    Args:
        session_mngr (SessionManager): The session manager instance.

    Returns:
        Response: A response object indicating the result of the transaction retrieval.
    """
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Retrieve transactions for the user
    retrieve_transactions_result = session_mngr.transaction_mngr.retrieve_transactions()

    # Check if transactions exist or could be retrieved
    if retrieve_transactions_result is None:
        response.is_error = True
        response.message = (
            "No transactions exist for the user or could not retrieve the list."
        )
        return response

    transactions = ""

    # Format transactions for display
    for transaction in retrieve_transactions_result:
        item = transaction["item"]
        amount = transaction["amount"]
        category = transaction["category"]
        date = transaction["date"]

        transactions += f"{item} | {amount} | {category} | {date}\n"

    return response


def set_balance_form(session_mngr: SessionManager, amount) -> Response:
    """
    Sets the balance for the user associated with the active session.

    Args:
        session_mngr (SessionManager): The session manager instance.
        amount (str): The amount to set as the user's balance.

    Returns:
        Response: A response object indicating the result of the balance setting operation.
    """
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Validate the amount
    if not validate_amount(amount):
        response.message += "Invalid amount. Amount entered is not a number.\n"
        response.is_error = True

    amount = abs(float(amount))

    # Set the user's balance
    set_balance_result = session_mngr.balance_mngr.set_balance(amount)

    # Check if the balance could be set
    if set_balance_result is None:
        response.is_error = True
        response.message = "Could not set the balance of the user."
    else:
        response.message = "User's balance has been set."

    return response


def get_balance_view(session_mngr: SessionManager) -> Response:
    """
    Retrieves and displays the balance for the user associated with the active session.

    Args:
        session_mngr (SessionManager): The session manager instance.

    Returns:
        Response: A response object indicating the result of the balance retrieval.
    """
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Retrieve the user's balance
    get_balance_result = session_mngr.balance_mngr.get_balance()

    # Check if the balance could be retrieved
    if get_balance_result is None:
        response.is_error = True
        response.message = "User's balance was not available."
    else:
        response.message = f"User's balance: {get_balance_result['amount']}"

    return response
