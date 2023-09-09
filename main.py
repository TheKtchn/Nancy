from accounts import Accounts
from futures import Futures
from profile_ import Profile
from transactions import Transactions
from user import User

if __name__ == "__main__":
    profile = Profile("Victor Momodu")
    accounts = Accounts(profile.database_directory)
    accounts.set_expenditure(10_000_000.00)
