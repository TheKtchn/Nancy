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
        print(
            """
███    ██  █████  ███    ██  ██████ ██    ██ 
████   ██ ██   ██ ████   ██ ██       ██  ██  
██ ██  ██ ███████ ██ ██  ██ ██        ████   
██  ██ ██ ██   ██ ██  ██ ██ ██         ██    
██   ████ ██   ██ ██   ████  ██████    ██ ██ 
              """
        )
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
        print("\n=== SIGNUP FORM ===")
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
        response.display()

    elif command == "login":
        print("\n=== LOGIN FORM ===")
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
        response.display()

    elif command == "logout":
        response: Response = logout_user_form(session_mngr=session_mngr)
        response.display()

    elif command == "update_password":
        print("\n=== UPDATE PASSWORD FORM ===")
        user_password_user_form = {
            "old_password": input("Enter existing password: "),
            "new_password": input("Enter new password: "),
        }

        response: Response = update_password_of_user_form(
            session_mngr=session_mngr,
            user_mngr=user_mngr,
            user_password_update_form=user_password_user_form,
        )
        response.display()

    elif command == "delete_user":
        print("\n=== DELETE USER FORM ===")
        delete_user_form = {"email": input("Enter email: ")}

        response: Response = delete_user_form(
            session_mngr=session_mngr,
            user_mngr=user_mngr,
            user_email_input=delete_user_form["email"],
        )
        response.display()

    elif command == "add_transaction":
        print("\n=== ADD TRANSACTION FORM ===")
        transaction_form = {
            "item": input("Enter item: "),
            "amount": input("Enter amount: "),
            "category": input("Enter category ('i' for Income, 'e' for Expense): "),
            "date": input("Enter date (DD-MM-YYYY): "),
        }

        response: Response = add_transaction_form(
            session_mngr=session_mngr,
            transaction_form=transaction_form,
        )
        response.display()

    elif command == "retrieve_transactions":
        print("\n=== RETRIEVE TRANSACTION VIEW ===")

        response: Response = retrieve_list_of_transactions_view(
            session_mngr=session_mngr
        )
        response.display()

    elif command == "set_balance":
        print("\n=== SET BALANCE FORM ===")
        balance_set_form = {
            "email": input("Enter email: "),
            "amount": input("Enter balance: "),
        }

        response: Response = set_balance_form(
            session_mngr=session_mngr,
            balance_set_form=balance_set_form,
        )
        response.display()

    elif command == "get_balance":
        print("\n=== GET BALANCE VIEW ===")
        balance_form = {"amount": input("Enter balance: ")}

        response: Response = get_balance_view(session_mngr=session_mngr)
        response.display()

    elif command == "create_budget":
        print("\n=== CREATE BUDGET FORM ===")
        budget_create_form = {
            "item": input("Enter item: "),
            "amount": input("Enter amount: "),
            "due_date": input("Enter due date (DD-MM-YYYY): "),
        }

        response: Response = create_budget_form(
            session_mngr=session_mngr,
            budget_create_form=budget_create_form,
        )
        response.display()

    elif command == "retrieve_budgets":
        print("\n=== RETRIEVE BUDGETS VIEW ===")

        response: Response = retrieve_list_of_budgets_view(session_mngr=session_mngr)
        response.display()

    elif command == "update_budget":
        print("\n=== UPDATE BUDGET FORM ===")
        budget_update_form = {
            "item": input("Enter item: "),
            "amount": input("Enter amount: "),
            "due_date": input("Enter due date (DD-MM-YYYY): "),
        }

        response: Response = update_budget_form(
            session_mngr=session_mngr,
            budget_update_form=budget_update_form,
        )
        response.display()

    elif command == "update_budget_spent":
        print("\n=== UPDATE BUDGET SPENT FORM ===")
        budget_update_spent_form = {
            "item": input("Enter item: "),
            "spent": input("Enter amount spent: "),
        }

        response: Response = update_budget_spent_form(
            session_mngr=session_mngr,
            budget_update_spent_form=budget_update_spent_form,
        )
        response.display()

    elif command == "delete_budget":
        print("\n=== DELETE BUDGET FORM ===")
        budget_delete_form = {"item": input("Enter item: ")}

        response: Response = delete_budget_form(
            session_mngr=session_mngr,
            item=budget_delete_form["item"],
        )
        response.display()

    else:
        print("Invalid command.")
