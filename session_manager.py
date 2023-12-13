from balance_manager import BalanceManager
from budget_manager import BudgetManager
from conversation_manager import ConversationManager
from transaction_manager import TransactionManager


class SessionManager:
    """
    Manager class for handling user sessions.

    This class manages the user session state and provides access to specific managers
    (BalanceManager, BudgetManager, TransactionManager) for interacting with data related
    to the user's financial activities.
    """

    def __init__(self) -> None:
        """
        Initializes the SessionManager instance.

        The session starts as inactive, and the user data and managers are set to None.

        Returns:
            None
        """
        self.is_session = False
        self.user_data = None
        self.transaction_mngr = None
        self.balance_mngr = None
        self.budget_mngr = None
        self.conversation_mngr = None

    def start_session(self, user_data):
        """
        Start a user session.

        Activates the session and initializes managers with the provided user data.

        Args:
            user_data (dict): User data containing information about the user.

        Returns:
            None
        """
        self.is_session = True
        self.user_data = user_data
        user_email = user_data["email"]
        self.transaction_mngr = TransactionManager(user_email)
        self.balance_mngr = BalanceManager(user_email)
        self.budget_mngr = BudgetManager(user_email)
        self.conversation_mngr = ConversationManager(user_email)

    def stop_session(self):
        """
        Stop the current user session.

        Deactivates the session and sets user data and managers to None.

        Returns:
            None
        """
        self.is_session = False
        self.user_data = None
        self.transaction_mngr = None
        self.balance_mngr = None
        self.budget_mngr = None
        self.conversation_mngr = None
