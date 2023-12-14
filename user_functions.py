from balance_manager import BalanceManager
from budget_manager import BudgetManager
from conversation_manager import ConversationManager
from response import Response
from transaction_manager import TransactionManager
from user_manager import UserManager
from utils import validate_name

user_mngr = UserManager()


def authenticate_user(username: str):
    r = Response()
    if not validate_name(username):
        r.is_error = True
        r.message = "Invalid name. Name should only contain alphabets."
        return r

    retrieve_user_result = user_mngr.retrieve_user(username)
    print(retrieve_user_result)
    if retrieve_user_result is not None:
        r.message = f"{username} has been logged in."
        return r

    create_user_result = user_mngr.create_user({"username": username})
    if create_user_result:
        r.message = f"{username} has been signed up."

    return r


def remove_user(username: str):
    r = Response()
    if not validate_name(username):
        r.is_error = True
        r.message = "Invalid name. Name should only contain alphabets."
        return r

    transaction_mngr = TransactionManager(username)
    delete_user_transactions_result = transaction_mngr.delete_user_transactions()
    if delete_user_transactions_result is None:
        r.is_error = True
        r.message += "Could not delete user transactions."

    balance_mngr = BalanceManager(username)
    delete_user_balance_result = balance_mngr.delete_user_balance()
    if delete_user_balance_result is None:
        r.is_error = True
        r.message += "Could not delete user balance."

    budget_mngr = BudgetManager(username)
    delete_user_budgets_result = budget_mngr.delete_user_budgets()
    if delete_user_budgets_result:
        r.is_error = True
        r.message += "Could not delete user budgets."

    conversation_mngr = ConversationManager(username)
    delete_user_conversations_result = conversation_mngr.delete_user_conversations()
    if delete_user_conversations_result:
        r.is_error = True
        r.message += "Could not delete user conversations."

    if r.is_error:
        return r

    delete_user_result = user_mngr.delete_user(username)
    if delete_user_result:
        r.message = "User has been deleted."
    else:
        r.is_error = True
        r.message = "User could not be deleted."

    return r
