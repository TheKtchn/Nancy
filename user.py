import bcrypt
import re

from response import Response
from database import db, ping


class UserDatabaseManager:
    PRIMARY_KEY = "email"

    def __init__(self) -> None:
        self.users = db["users"]

    def create_user(self, user_data):
        result = self.users.insert_one(user_data)
        return result

    def retrieve_user(self, key):
        query = {self.PRIMARY_KEY: key}
        user = self.users.find_one(query)

        return user

    def update_user(self, key, data):
        query = {self.PRIMARY_KEY: key}
        result = self.users.update_one(query, {"$set": data})

        return result

    def delete_user(self, key):
        query = {self.PRIMARY_KEY: key}
        result = self.users.delete_one(query)

        return result


# user_dbm = UserDatabaseManager()


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


def create_user_from_form(user_create_form: dict):
    if not ping():
        print("Not connected!")
        return

    name = user_create_form["name"]
    email = user_create_form["email"]
    password = user_create_form["password"]

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


if __name__ == "__main__":
    user_dbm = UserDatabaseManager()
    is_pinging = ping()
    print(f"Ping: {is_pinging}")

    if is_pinging:
        # create_user_data0 = {
        #     "name": "Victor Momodu",
        #     "email": "vmomodu@email.com",
        #     "password": "vmomodu123",
        # }

        # create_user_data1 = {
        #     "name": "Daniel Ogunsola",
        #     "email": "dogunsola@email.com",
        #     "password": "dogunsola123",
        # }

        # create_user_data2 = {
        #     "name": "Anjola Akinyemi",
        #     "email": "aakinyemi@email.com",
        #     "password": "aakinyemi123",
        # }

        # create_user_from_form(create_user_data0)
        # create_user_from_form(create_user_data1)
        # create_user_from_form(create_user_data2)

        invalid_login_user_data = {
            "email": "somerandomuser@gmail.com",
            "password": "somepassword123",
        }

        wrong_password_login_user_data = {
            "email": "aakinyemi@email.com",
            "password": "aakinyemi1234",
        }

        correct_password_login_user_data = {
            "email": "aakinyemi@email.com",
            "password": "aakinyemi123",
        }

        print(login_user_from_form(invalid_login_user_data))
        print(login_user_from_form(wrong_password_login_user_data))
        print(login_user_from_form(correct_password_login_user_data))

