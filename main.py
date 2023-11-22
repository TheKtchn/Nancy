from database import ping
from user import create_user_from_form, login_user_from_form
from transactions import TransactionsDatabaseManager


# user_create_form0 = {
#     "name": "Victor Momodu",
#     "email": "vmomodu@email.com",
#     "password": "vmomodu123",
# }

# user_create_form1 = {
#     "name": "Daniel Ogunsola",
#     "email": "dogunsola@email.com",
#     "password": "dogunsola123",
# }

# response0 = create_user_from_form(user_create_form0)
# response1 = create_user_from_form(user_create_form1)

# print(f"Response0: {response0.data['_id']}")
# print(f"Response1: {response1.data['_id']}")

user_login_form = {
    "email": "dogunsola@email.com",
    "password": "dogunsola123",
}

response = login_user_from_form(user_login_form)

transactions_dbm = TransactionsDatabaseManager(response.data["_id"])
transactions_dbm.create_transaction(
    {
        "description": "Some transaction",
        "amount": 12450,
        "category": "Income",
        "date": "22/11/2023",
    }
)

transactions_dbm.create_transaction(
    {
        "description": "Another transaction",
        "amount": 12450,
        "category": "Income",
        "date": "22/11/2023",
    }
)
