from balance_manager import BalanceManager
from database import ping
from response import Response
from transaction_manager import TransactionManager
from user_manager import UserManager
from utils import hash_password, validate_email, validate_name, validate_password

user_mngr = UserManager()


def signup_user_form(user_signup_form: dict) -> Response:
    name = user_signup_form["name"]
    email = user_signup_form["email"]
    password = user_signup_form["password"]

    response = Response()

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
        response.message = f"User {user_data['email']} signed up."
        response.data = user_data
    else:
        response.is_error = True
        response.message = "Could not signup user."

    return response


def login_user_form(user_login_form: dict):
    email = user_login_form["email"]
    password = user_login_form["password"]

    response = Response()

    # Validate email
    if not validate_email(email=email):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid email address."

    # Validate password
    if not validate_password(password=password):
        response.is_error = True
        if response.message:
            response.message += "\n"
        response.message += "Invalid password."

    if response.is_error:
        return response

    # Retrieve user by email
    retrieve_user_result = user_mngr.retrieve_user(key=email)
    if retrieve_user_result is None:
        response.is_error = True
        response.message = "User does not exist."

        return response

    # Check if the entered password matches the stored password
    if hash_password(password=password) == retrieve_user_result["password"]:
        user_data = {}
        user_data["name"] = retrieve_user_result["name"]
        user_data["email"] = retrieve_user_result["email"]
        user_data["password"] = retrieve_user_result["password"]

        response.message = f"User {user_data['email']} logged in."
        response.data = user_data

    else:
        response.is_error = True
        response.message = "Password is not correct."

    return response


def logout_user_form():
    response = Response()
    response.message = "Logged out."
    response.data = None

    return response


def update_password_of_user_form(user_password_update_form: dict, user_data: dict):
    old_password = user_password_update_form["old_password"]
    new_password = user_password_update_form["new_password"]

    response = Response()

    # Check if the old password matches the existing password
    if hash_password(password=old_password) != user_data["password"]:
        response.is_error = True
        response.message = "Old password does not match existing password."

        return response

    # Validate the new password
    if not validate_password(password=new_password):
        response.is_error = True
        response.message = "Invalid new password entered.\
            \nPassword should be at least 5 characters long and contain a letter and number."

        return response

    email = user_data["email"]

    # Retrieve user by email
    retrieve_user_result = user_mngr.retrieve_user(key=email)
    if retrieve_user_result is None:
        response.is_error = True
        response.message = "User does not exist.\nContact developers."

        return response

    hashed_password = hash_password(password=new_password)
    password_data = {"password": hashed_password}

    update_user_result = user_mngr.update_user(key=email, data=password_data)

    if update_user_result:
        user_data["password"] = hashed_password
        response.message = f"User {user_data['email']} password changed."
        response.data = user_data

    else:
        response.is_error = True
        response.message = "Could not change user password."

    return response


# def delete_user_form(user_delete_form: dict, user_data: dict):
#     email = user_delete_form["email"]
#     password = user_delete_form["password"]

#     response = Response()

#     # Check if the provided email matches the current session email
#     if email != user_data["email"]:
#         response.is_error = True
#         response.message = "User email input does not match current session email."

#         return response

#     # Check if the provided password matches the current session
#     if hash_password(password=password) != user_data["password"]:
#         response.is_error = True
#         response.message = "User password input is incorrect."

#         return response


#     transaction_mngr = TransactionManager(email=user_data["email"])
#     # Delete user transactions
#     delete_user_transactions_result = (
#         transaction_mngr.delete_user_transactions()
#     )
#     if delete_user_transactions_result is None:
#         response.is_error = True
#         response.message += "Could not delete user transactions."

#     # Delete user balance
#     delete_user_balance_result = session_mngr.balance_mngr.delete_user_balance()
#     if delete_user_balance_result is None:
#         response.is_error = True
#         response.message += "Could not delete user balance."

#     # Delete user budgets
#     delete_user_budgets_result = session_mngr.budget_mngr.delete_user_budgets()
#     if delete_user_budgets_result:
#         response.is_error = True
#         response.message += "Could not delete user budgets."

#     # Delete user conversations
#     delete_user_conversations_result = (
#         session_mngr.conversation_mngr.delete_user_conversations()
#     )
#     if delete_user_conversations_result:
#         response.is_error = True
#         response.message += "Could not delete user conversations."

#     # Stop the session
#     session_mngr.stop_session()

#     if response.is_error:
#         return response

#     # Delete the user
#     result = user_mngr.delete_user(email)
#     if result:
#         response.message = "User has been deleted."
#     else:
#         response.is_error = True
#         response.message = "User could not be deleted."

#     return response


# def show_user_information_view(session_mngr: SessionManager):
#     """Displays the user's information.

#     Args:
#         session_mngr (SessionManager): The session manager object.

#     Returns:
#         Response: The response object containing the user's information or an error message.
#     """

#     response = Response()

#     # Check if a session is active
#     if session_mngr.is_session:
#         response.message = f"Name: {session_mngr.user_data['name']}\
#             \nEmail: {session_mngr.user_data['email']}"

#     else:
#         response.is_error = True
#         response.message = "No active session is ongoing."

#     return response
