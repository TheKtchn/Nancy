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

HELP = {
    "signup": "To signup a user into a session.",
    "login": "To login a user into a session.",
    "logout": "Logout a user from a session.",
    "help": "Show help.",
    "quit": "End program.",
}

user_mngr = UserManager()
session_mngr = SessionManager()


def help():
    print("HELP")
    pprint.pprint(HELP)
    print()


is_started = False

while True:
    if not is_started:
        print("=== START ===")
        help()
        is_started = True

    command = input("Enter command ('quit' to end program, 'help' for help): ")

    if command == "quit":
        if session_mngr.is_session:
            response: Response = logout_user_form(session_mngr=session_mngr)
            pprint.pprint(response.message)

        print("Closing program...")
        time.sleep(3)
        print("END")
        break

    elif command == "help":
        help()

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

            print(response.message)

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

            print(response.message)

        else:
            print("Can't login user due to no internet connection.")

    elif command == "logout":
        response: Response = logout_user_form(session_mngr=session_mngr)
        print(response.message)

    else:
        print("Invalid command.")
