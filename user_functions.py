from response import Response
from session_manager import SessionManager
from user_manager import UserManager
from utils import hash_password, validate_email, validate_name, validate_password

def signup_user_form(
    # DEBUG # session_mngr: SessionManager, 
    user_mngr: UserManager,
    user_signup_form: dict,
) -> Response:
    """
    Sign up a user based on the provided user signup form.

    Args:
        session_mngr (SessionManager): The session manager instance.
        user_mngr (UserManager): The user manager instance.
        user_signup_form (dict): The user signup form containing user data.

    Returns:
        Response: A response object indicating the result of the signup operation.
    """
    name = user_signup_form["name"]
    email = user_signup_form["email"]
    password = user_signup_form["password"]

    response = Response()

    # Check if a user is already using the session
    # DEBUG
    # if session_mngr.is_session:
    #     response.is_error = True
    #     response.message = (
    #         "A user is using this session already.\nLog out to be able to signup"
    #     )
    #     return response
    # DEBUG

    # Validate name
    if not validate_name(name):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid name. Name should only contain alphabets."

    # Validate email
    if not validate_email(email):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid email address."

    # Validate password
    if not validate_password(password):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid password. Password should contain at least one letter and one number, with a minimum length of 5 characters."

    if response.is_error:
        return response

    # Check if the user already exists
    retrieve_user_result = user_mngr.retrieve_user(email)
    if retrieve_user_result is not None:
        response.is_error = True
        response.message = "User already exists."
        return response

    # Create user data
    user_data = {"name": name, "email": email, "password": hash_password(password)}

    # Create user
    create_user_result = user_mngr.create_user(user_data)
    if create_user_result:
        # DEBUG # session_mngr.start_session(user_data)
        response.message = f"User {user_data['email']} signed up."
    else:
        response.is_error = True
        response.message = "Could not signup user."

    return response


def login_user_form(
    session_mngr: SessionManager,
    user_mngr: UserManager,
    user_login_form: dict,
):
    """Logs in a user using the provided login form data.

    Args:
        session_mngr (SessionManager): The session manager object.
        user_mngr (UserManager): The user manager object.
        user_login_form (dict): The user login form data.

    Returns:
        Response: The response object indicating the success or failure of the login operation.
    """

    email = user_login_form["email"]
    password = user_login_form["password"]

    response = Response()

    # Check if a session is already active
    if session_mngr.is_session:
        response.is_error = True
        response.message += "A user is using this session already.\
            \nLog out to be able to login."

        return response

    # Validate email
    if not validate_email(email):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid email address."

    # Validate password
    if not validate_password(password):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid password."

    if response.is_error:
        return response

    # Retrieve user by email
    retrieve_user_result = user_mngr.retrieve_user(email)
    if retrieve_user_result is None:
        response.is_error = True
        response.message = "User does not exist."
        session_mngr.stop_session()

        return response

    # Check if the entered password matches the stored password
    if hash_password(password) == retrieve_user_result["password"]:
        user_data = {}
        user_data["name"] = retrieve_user_result["name"]
        user_data["email"] = retrieve_user_result["email"]
        user_data["password"] = retrieve_user_result["password"]

        session_mngr.start_session(user_data)
        response.message = f"User {user_data['email']} logged in."

    else:
        response.is_error = True
        response.message = "Password is not correct."

    return response


def logout_user_form(session_mngr: SessionManager):
    """Logs out the user from the active session.

    Args:
        session_mngr (SessionManager): The session manager object.

    Returns:
        Response: The response object indicating the success or failure of the logout operation.
    """

    response = Response()

    # Check if a session is active
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    # Stop the session
    session_mngr.stop_session()
    response.message = "Logged out."

    return response


def update_password_of_user_form(
    session_mngr: SessionManager,
    user_mngr: UserManager,
    user_password_update_form: dict,
):
    """Updates the password of the user using the provided form data.

    Args:
        session_mngr (SessionManager): The session manager object.
        user_mngr (UserManager): The user manager object.
        user_password_update_form (dict): The user password update form data.

    Returns:
        Response: The response object indicating the success or failure of the password update operation.
    """

    old_password = user_password_update_form["old_password"]
    new_password = user_password_update_form["new_password"]

    response = Response()

    # Check if a session is active
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing.\
            \nYou should signup or login."

        return response

    # Check if the old password matches the existing password
    if hash_password(old_password) != session_mngr.user_data["password"]:
        response.is_error = True
        response.message = "Old password does not match existing password."

        return response

    # Validate the new password
    if not validate_password(new_password):
        response.is_error = True
        response.message = "Invalid new password entered.\
            \nPassword should be at least 5 characters long and contain a letter and number."

        return response

    email = session_mngr.user_data["email"]

    # Retrieve user by email
    retrieve_user_result = user_mngr.retrieve_user(email)
    if retrieve_user_result is None:
        response.is_error = True
        response.message = "User does not exist.\nContact developers."
        session_mngr.stop_session()

        return response

    password_data = {"password": hash_password(new_password)}

    # Update the user's password
    update_user_result = user_mngr.update_user(email, password_data)

    if update_user_result:
        session_mngr.user_data["password"] = password_data["password"]
        response.message = f"User {session_mngr.user_data['email']} password changed."

    else:
        response.is_error = True
        response.message = "Could not change user password."

    return response


def delete_user_form(
    session_mngr: SessionManager,
    user_mngr: UserManager,
    user_delete_form: dict,
):
    """Deletes a user and associated data using the provided form data.

    Args:
        session_mngr (SessionManager): The session manager object.
        user_mngr (UserManager): The user manager object.
        user_email_input (str): The user email input.

    Returns:
        Response: The response object indicating the success or failure of the user deletion operation.
    """

    email = user_delete_form["email"]
    password = user_delete_form["password"]
    response = Response()

    # Check if a session is active
    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    # Check if the provided email matches the current session email
    if email != session_mngr.user_data["email"]:
        response.is_error = True
        response.message = "User email input does not match current session email."

        return response

    # Check if the provided password matches the current session
    if hash_password(password) != session_mngr.user_data["password"]:
        response.is_error = True
        response.message = "User password input is incorrect."

        return response

    # Delete user transactions
    delete_user_transactions_result = (
        session_mngr.transaction_mngr.delete_user_transactions()
    )
    if delete_user_transactions_result is None:
        response.is_error = True
        response.message += "Could not delete user transactions."

    # Delete user balance
    delete_user_balance_result = session_mngr.balance_mngr.delete_user_balance()
    if delete_user_balance_result is None:
        response.is_error = True
        response.message += "Could not delete user balance."

    # Delete user budgets
    delete_user_budgets_result = session_mngr.budget_mngr.delete_user_budgets()
    if delete_user_budgets_result:
        response.is_error = True
        response.message += "Could not delete user budgets."

    # Delete user conversations
    delete_user_conversations_result = (
        session_mngr.conversation_mngr.delete_user_conversations()
    )
    if delete_user_conversations_result:
        response.is_error = True
        response.message += "Could not delete user conversations."

    # Stop the session
    session_mngr.stop_session()

    if response.is_error:
        return response

    # Delete the user
    result = user_mngr.delete_user(email)
    if result:
        response.message = "User has been deleted."
    else:
        response.is_error = True
        response.message = "User could not be deleted."

    return response


def show_user_information_view(session_mngr: SessionManager):
    """Displays the user's information.

    Args:
        session_mngr (SessionManager): The session manager object.

    Returns:
        Response: The response object containing the user's information or an error message.
    """

    response = Response()

    # Check if a session is active
    if session_mngr.is_session:
        response.message = f"Name: {session_mngr.user_data['name']}\
            \nEmail: {session_mngr.user_data['email']}"

    else:
        response.is_error = True
        response.message = "No active session is ongoing."

    return response
