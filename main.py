import pprint
import time

from budget_functions import (
    create_budget_form,
    delete_budget_form,
    retrieve_list_of_budgets_view,
    update_budget_form,
    update_budget_spent_form,
)
from database import ping
from response import Response
from session_manager import SessionManager
from transaction_and_balance_functions import (
    add_transaction_form,
    get_balance_view,
    retrieve_list_of_transactions_view,
    set_balance_form,
)
from user_functions import (
    delete_user_form,
    login_user_form,
    logout_user_form,
    signup_user_form,
    update_password_of_user_form,
)
from user_manager import UserManager

HELP = {}

user_mngr = UserManager()
session_mngr = SessionManager()


def instructions():
    with open("help.txt", "r") as help_file:
        print()
        print(help_file.read())
        print()


is_started = False

while True:
    if not is_started:
        print("=== START ===")
        instructions()
        is_started = True

    command = input("Enter command ('quit' to end program, 'help' for help): ")

    if command == "quit":
        if session_mngr.is_session:
            response: Response = logout_user_form(session_mngr=session_mngr)
            print(response.message, end="\n")

        print("Closing program...")
        time.sleep(3)
        print("END")
        break

    elif command == "help":
        instructions()

    elif command == "signup":
        if ping():
            print("\n=== SIGNUP FORM ===\n")
            user_signup_form = {
                "name": input("Enter name:\n>>> "),
                "email": input("Enter email:\n>>> "),
                "password": input(
                    "Enter password (at least 5 characters, 1 letter and 1 number):\n>>> "
                ),
            }

            response: Response = signup_user_form(
                session_mngr=session_mngr,
                user_mngr=user_mngr,
                user_signup_form=user_signup_form,
            )
            print(response.message, end="\n")

        else:
            print("Can't signup user due to no internet connection.")

    elif command == "login":
        if ping():
            print("\n=== LOGIN FORM ===\n")
            user_login_form = {
                "email": input("Enter email:\n>>> "),
                "password": input(
                    "Enter password (at least 5 characters, 1 letter and 1 number):\n>>> "
                ),
            }

            response: Response = login_user_form(
                session_mngr=session_mngr,
                user_mngr=user_mngr,
                user_login_form=user_login_form,
            )
            print(response.message, end="\n")

        else:
            print("Can't login user due to no internet connection.")

    elif command == "logout":
        response: Response = logout_user_form(session_mngr=session_mngr)
        print(response.message, end="\n")

    elif command == "update_password":
        if ping():
            print("\n=== UPDATE PASSWORD FORM ===\n")
            user_password_user_form = {
                "old_password": input("Enter existing password: "),
                "new_password": input("Enter new password: "),
            }

            response: Response = update_password_of_user_form(
                session_mngr=session_mngr,
                user_mngr=user_mngr,
                user_password_update_form=user_password_user_form,
            )
            print(response.message, end="\n")

        else:
            print("Cannot update password as there is no internet connection.")

    elif command == "delete_user":
        if ping():
            print("\n=== DELETE USER FORM ===\n")
            delete_user_form = {"email": input("email: ")}

            response: Response = delete_user_form(
                session_mngr=session_mngr,
                user_mngr=user_mngr,
                user_email_input=delete_user_form["email"],
            )
            print(response.message, end="\n")

        else:
            print("Cannot delete user as there is no internet connection.")

    else:
        print("Invalid command.")
