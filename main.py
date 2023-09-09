from person import Profile
from accounts import Accounts


if __name__ == "__main__":
    profile = Profile("Victor Momodu")
    accounts = Accounts(profile.database_directory)
    accounts.set_expenditure(10_000_000.00)

    