import hashlib
import re

from response import Response
from session_manager import SessionManager
from user_manager import UserManager


def _validate_name(name):
    return bool(re.match("^[a-zA-Z -]+$", name))


def _validate_email(email):
    # A simple email validation using regular expression
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))


def _validate_password(password):
    # Password should contain at least one letter and one number, with a minimum length of 5 characters
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$", password))


def _hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    hashed_password = sha256_hash.hexdigest()

    return hashed_password


def signup_user_form(
    session_mngr: SessionManager,
    user_mngr: UserManager,
    user_signup_form: dict,
):
    name = user_signup_form["name"]
    email = user_signup_form["email"]
    password = user_signup_form["password"]

    response = Response()

    if session_mngr.is_session:
        response.is_error = True
        response.message += "A user is using this session already.\
            \nLog out to be able to signup"

        return response

    if not _validate_name(name):
        response.is_error = True
        response.message += "Invalid name. Name should only contain alphabets.\n"

    if not _validate_email(email):
        response.is_error = True
        response.message += "Invalid email address.\n"

    if not _validate_password(password):
        response.is_error = True
        response.message += "Invalid password. Password should contain at least one letter and one number, with a minimum length of 5 characters.\n"

    if response.is_error:
        return response

    result = user_mngr.retrieve_user(email)
    if result is not None:
        response.is_error = True
        response.message = "User already exists."

        return response

    user_data = {}
    user_data["name"] = name
    user_data["email"] = email
    user_data["password"] = _hash_password(password)

    result = user_mngr.create_user(user_data)
    if result:
        session_mngr.start_session(user_data)
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
    email = user_login_form["email"]
    password = user_login_form["password"]

    response = Response()

    if session_mngr.is_session:
        response.is_error = True
        response.message += "A user is using this session already.\
            \nLog out to be able to login."

        return response

    if not _validate_email(email):
        response.is_error = True
        response.message += "Invalid email address.\n"

    if not _validate_password(password):
        response.is_error = True
        response.message += "Invalid password.\n"

    if response.is_error:
        return response

    retrieved_user = user_mngr.retrieve_user(email)
    if retrieved_user is None:
        response.is_error = True
        response.message = "User does not exists."
        session_mngr.stop_session()

        return response

    if _hash_password(password) == retrieved_user["password"]:
        user_data = {}
        user_data["name"] = retrieved_user["name"]
        user_data["email"] = retrieved_user["user"]
        user_data["password"] = retrieved_user["password"]

        session_mngr.start_session(user_data)
        response.message = f"User {user_data['email']} logged in."

    else:
        response.is_error = True
        response.message = "Password is not correct."

    return response


def logout_user_form(session_mngr: SessionManager):
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    session_mngr.stop_session()
    response.message("Logged out.")

    return response


def update_password_of_user_form(
    session_mngr: SessionManager,
    user_mngr: UserManager,
    password_form: dict,
):
    old_password = password_form["old_password"]
    new_password = password_form["new_password"]

    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    if _hash_password(old_password) != session_mngr.user_data["password"]:
        response.is_error = True
        response.message = "Old password does not match existing password."

        return response

    if not _validate_password(new_password):
        response.is_error = True
        response.message = "Invalid password."

        return response

    email = session_mngr.user_data["email"]
    retrieved_user = user_mngr.retrieve_user(email)

    if retrieved_user is None:
        response.is_error = True
        response.message = "User does not exists."
        session_mngr.stop_session()

        return response

    password_data = {"password": _hash_password(new_password)}
    result = user_mngr.update_user(email, password_data)

    if result:
        session_mngr.user_data["password"]
        response.message = f"User {session_mngr.user_data['email']} password changed."

    else:
        response.is_error = True
        response.message = "Could not change user password."

    return response


def delete_user_form(
    session_mngr: SessionManager,
    user_mngr: UserManager,
    user_email_input,
):
    email = user_email_input
    response = Response()

    if not session_mngr.is_session:
        response.is_error = True
        response.message = "No active session is ongoing."

        return response

    if not _validate_email(email):
        response.is_error = True
        response.message = "Invalid email address."

        return response

    if email != session_mngr.user_data["email"]:
        response.is_error = True
        response.message = "User email input does not match current session email."

        return response

    # TODO: Add results
    session_mngr.transaction_mngr.delete_user_transactions()
    session_mngr.balance_mngr.delete_user_balance()
    session_mngr.budget_mngr.delete_user_budgets()
    session_mngr.stop_session()

    result = user_mngr.delete_user(email)
    if result:
        response.message = "User has been deleted."
    else:
        response.is_error = True
        response.message = "User could not be deleted."

    return response


def show_user_information_view(session_mngr: SessionManager):
    response = Response()

    if session_mngr.is_session:
        response.message = f"Name: {session_mngr.user_data['name']}\
            \nEmail: {session_mngr.user_data['email']}"

    else:
        response.is_error = True
        response.message = "No active session is ongoing."

    return response
