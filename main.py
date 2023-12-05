import pprint
import time

from budget_functions import (
    create_budget_form,
    delete_budget_form,
    retrieve_list_of_budgets_view,
    update_budget_form,
    update_budget_spent_form,
)
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
    "quit": "End program.",
}

user_mngr = UserManager()
session_mngr = SessionManager()

while True:
    print("START")
    command = input("Enter command ('quit' to end program, 'help' for help): ")

    if command == "quit":
        print("Closing program...")
        time.sleep(3)
        print("END")
        break

    if command == "help":
        print()
        pprint.pprint(HELP)
        print()
