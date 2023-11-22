from database import ping
from user_forms import signup_user_from_form, login_user_from_form
from transactions_and_balance_forms import add_transaction_form, set_balance_form
from session_data import SessionData

COMMANDS = ["signup", "login", "logout", "transact", "quit"]
current_session_data = SessionData()

while True:
    print("Nancy has been started.")
    command = input("Enter command: ")
    if command == "signup":
        user_signup_form = {}
        user_signup_form["name"] = input("Enter name: ")
        user_signup_form["email"] = input("Enter email: ")
        user_signup_form["password"] = input("Enter password: ")
        print()

        response = signup_user_from_form(user_signup_form)
        if response.is_error:
            print(response.error_message)

        else:
            current_session_data.start_session_data(response.data["_id"])

            while True:
                balance_form = {}
                balance_form["amount"] = input("Enter balance: ")
                print()

                response = set_balance_form(current_session_data, balance_form)
                if response.is_error:
                    print(response.error_message)

                else:
                    print("User's balance has been set.")
                    break

            print("User has been signed up.")

    elif command == "login":
        user_login_form = {}
        user_login_form["email"] = input("Enter email: ")
        user_login_form["password"] = input("Enter password: ")
        print()

        response = login_user_from_form(user_login_form)
        if response.is_error:
            print(response.error_message)

        else:
            current_session_data.start_session_data(response.data["_id"])
            print("User has been logged in.")

    elif command == "logout":
        current_session_data.stop_session_data()

    elif command == "transact":
        transaction_form = {}
        transaction_form["description"] = input("Enter description: ")
        transaction_form["amount"] = input("Enter amount: ")

        category_input = input(
            "Enter category ([i for 'income'] or [e for 'expense']): "
        )
        if category_input.lower == "e":
            transaction_form["category"] = "Expense"
        else:
            transaction_form["category"] = "Income"

        date = transaction_form["date"]

    elif command == "quit":
        current_session_data.stop_session_data()
        print("Nancy has been stopped.")
        break

    else:
        print("Wrong command entered.")
