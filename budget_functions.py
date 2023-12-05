from response import Response
from session_manager import SessionManager
from utils import validate_amount, validate_date_not_greater


def create_budget_form(
    session_mngr: SessionManager, budget_create_form: dict
) -> Response:
    """
    Creates a budget item based on the provided budget creation form.

    Args:
        session_mngr (SessionManager): The session manager instance.
        budget_create_form (dict): The budget creation form containing budget data.

    Returns:
        Response: A response object indicating the result of the budget creation.
    """
    item = budget_create_form["item"]
    amount = budget_create_form["amount"]
    due_date = budget_create_form["due_date"]

    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Validate item
    if not item:
        response.message += "Invalid item. Item cannot be empty."
        response.is_error = True

    # Validate amount
    if not validate_amount(amount):
        if response.message:
            response.message += "\n"
        response.message += "Invalid amount. Amount entered is not a number."
        response.is_error = True

    # Validate due date
    is_valid_date, error_message = validate_date_not_greater(due_date)
    if not is_valid_date:
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += error_message

    if response.is_error:
        return response

    amount = abs(float(amount))

    # Retrieve the budget item
    retrieve_budget_result = session_mngr.budget_mngr.retrieve_budget(item)

    # Check if the budget item already exists
    if retrieve_budget_result is not None:
        response.is_error = True
        response.message = "Item already exists."
        return response

    # Create budget data
    budget_data = {"item": item, "amount": amount, "spent": 0, "due_date": due_date}

    # Create the budget item
    create_budget_result = session_mngr.budget_mngr.create_budget(budget_data)

    if create_budget_result is None:
        response.is_error = True
        response.message = "Budget item could not be created."
    else:
        response.message = "Item has been created."

    return response


def retrieve_list_of_budgets_view(session_mngr: SessionManager) -> Response:
    """
    Retrieves and displays the list of budgets for the user associated with the active session.

    Args:
        session_mngr (SessionManager): The session manager instance.

    Returns:
        Response: A response object indicating the result of the budget retrieval.
    """
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Retrieve budgets for the user
    retrieve_budgets_result = session_mngr.budget_mngr.retrieve_budgets()

    # Check if budgets exist or could be retrieved
    if retrieve_budgets_result is None:
        response.is_error = True
        response.message = (
            "No budgets exist for the user or could not retrieve the list."
        )
        return response

    budgets = ""

    # Format budgets for display
    for budget in retrieve_budgets_result:
        item = budget["item"]
        amount = budget["amount"]
        spent = budget["spent"]
        date = budget["due_date"]
        percent = spent / amount

        budgets += f"{item} | {amount} | {spent} | {percent:.2f} | {date}\n"

    return response


def update_budget_form(
    session_mngr: SessionManager,
    budget_update_form: dict,
) -> Response:
    """
    Updates a budget item based on the provided budget update form.

    Args:
        session_mngr (SessionManager): The session manager instance.
        budget_update_form (dict): The budget update form containing updated budget data.

    Returns:
        Response: A response object indicating the result of the budget update.
    """
    item = budget_update_form["item"]
    amount = budget_update_form["amount"]
    due_date = budget_update_form["due_date"]

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

    # Validate due date
    is_valid_date, error_message = validate_date_not_greater(due_date)
    if not is_valid_date:
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += error_message

    if response.is_error:
        return response

    amount = abs(float(amount))

    # Retrieve the budget item
    retrieve_budget_result = session_mngr.budget_mngr.retrieve_budget(item)

    # Check if the budget item exists
    if not retrieve_budget_result:
        response.is_error = True
        response.message = "Item does not exist."
        return response

    # Prepare updated budget data
    budget_data = {"amount": amount, "spent": 0, "due_date": due_date}

    # Update the budget item
    update_budget_result = session_mngr.budget_mngr.update_budget(item, budget_data)

    if update_budget_result is None:
        response.is_error = True
        response.message = "Budget item could not be updated."
    else:
        response.message = "Item has been updated."

    return response


def update_budget_spent_form(
    session_mngr: SessionManager, budget_update_spent_form: dict
) -> Response:
    """
    Updates the amount spent on a budget item based on the provided update spent form.

    Args:
        session_mngr (SessionManager): The session manager instance.
        budget_update_spent_form (dict): The budget update spent form containing the item and spent amount.

    Returns:
        Response: A response object indicating the result of the budget item spent update.
    """
    item = budget_update_spent_form["item"]
    spent = budget_update_spent_form["spent"]

    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Validate item
    if not item:
        response.message += "Invalid item. Item cannot be empty."
        response.is_error = True

    # Validate spent amount
    if not validate_amount(spent):
        if response.message:
            response.message += "\n"
        response.message += "Invalid amount. Amount entered is not a number."
        response.is_error = True

    if response.is_error:
        return response

    spent = abs(float(spent))

    # Retrieve the budget item
    retrieve_budget_result = session_mngr.budget_mngr.retrieve_budget(item)

    # Check if the budget item exists
    if not retrieve_budget_result:
        response.is_error = True
        response.message = "Item does not exist."
        return response

    # Prepare updated budget data with spent amount
    budget_data = {"spent": spent}

    # Update the budget item spent amount
    update_budget_result = session_mngr.budget_mngr.update_budget(item, budget_data)

    if update_budget_result is None:
        response.is_error = True
        response.message = "Budget item spent could not be updated."
    else:
        response.message = "Amount spent on item has been updated."

    return response


def delete_budget_form(session_mngr: SessionManager, item: str) -> Response:
    """
    Deletes a budget item based on the provided item name.

    Args:
        session_mngr (SessionManager): The session manager instance.
        item (str): The name of the budget item to be deleted.

    Returns:
        Response: A response object indicating the result of the budget item deletion.
    """
    response = Response()

    # Check if an active session is ongoing
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."
        return response

    # Validate item
    if not item:
        response.message = "Invalid item. Item cannot be empty."
        response.is_error = True
        return response

    # Delete the budget item
    delete_budget_result = session_mngr.budget_mngr.delete_budget(item)

    # Check if the budget item could be deleted
    if delete_budget_result is None:
        response.is_error = True
        response.message = "Could not delete budget item."
    else:
        response.message = f"Deleted {item} from budgets."

    return response
