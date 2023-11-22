import bcrypt
import re

from response import Response

from user import UserDatabaseManager

user_dbm = UserDatabaseManager()


def validate_name(name):
    return bool(re.match("^[a-zA-Z -]+$", name))


def validate_email(email):
    # A simple email validation using regular expression
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))


def validate_password(password):
    # Password should contain at least one letter and one number, with a minimum length of 5 characters
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$", password))


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))


def signup_user_from_form(user_signup_form: dict):
    name = user_signup_form["name"]
    email = user_signup_form["email"]
    password = user_signup_form["password"]

    response = Response()
    response.data = {}

    if not validate_name(name):
        response.error_message += "Invalid name. Name should only contain alphabets.\n"
        response.is_error = True

    if not validate_email(email):
        response.error_message += "Invalid email address.\n"
        response.is_error = True

    if not validate_password(password):
        response.error_message += "Invalid password. Password should contain at least one letter and one number, with a minimum length of 5 characters.\n"
        response.is_error = True

    if response.is_error:
        return response

    retrieved_user = user_dbm.retrieve_user(email)
    if retrieved_user is not None:
        response.error_message += "User already exists."
        response.is_error = True

    if not response.is_error:
        response.data["name"] = name
        response.data["email"] = email
        response.data["password"] = hash_password(password)

        user_dbm.create_user(response.data)

    return response


def login_user_from_form(user_login_form):
    email = user_login_form["email"]
    password = user_login_form["password"]

    response = Response()
    response.data = {}

    if not validate_email(email):
        response.error_message += "Invalid email address.\n"
        response.is_error = True

    if not validate_password(password):
        response.error_message += "Invalid password.\n"
        response.is_error = True

    if response.is_error:
        return response

    retrieved_user = user_dbm.retrieve_user(email)
    if retrieved_user is None:
        response.error_message += "User does not exists.\n"
        response.is_error = True

    if not response.is_error:
        if hash_password(password) != retrieved_user["password"]:
            response.error_message += "Invalid password.\n"
            response.is_error = True
        else:
            response.data = retrieved_user

    return response
