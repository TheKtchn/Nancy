from balance_manager import BalanceManager
from budget_manager import BudgetManager
from transaction_manager import TransactionManager


class SessionManager:
    def __init__(self) -> None:
        self.is_session = False
        self.user_data = None
        self.transaction_mngr = None
        self.balance_mngr = None
        self.budget_mngr = None

    def start_session(self, user_data):
        self.is_session = True
        self.user_data = user_data
        user_email = user_data["email"]
        self.transaction_mngr = TransactionManager(user_email)
        self.balance_mngr = BalanceManager(user_email)
        self.budget_mngr = BudgetManager(user_email)

    def stop_session(self):
        self.is_session = False
        self.user_data = None
        self.transaction_mngr = None
        self.balance_mngr = None
        self.budget_mngr = None
