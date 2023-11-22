from balance import BalanceDatabaseManager
from transactions import TransactionsDatabaseManager

class SessionData:
    def __init__(self) -> None:
        self.is_session = False
        self.transactions_dbm = None
        self.balance_dbm = None
        
    def start_session_data(self, user_id):
        self.is_session = True
        self.transactions_dbm = TransactionsDatabaseManager(user_id)
        self.balance_dbm = BalanceDatabaseManager(user_id)
        
    def stop_session_data(self):
        self.is_session = False
        self.transactions_dbm = None
        self.balance_dbm = None