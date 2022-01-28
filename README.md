### Project Title:
## Nancy

_Finance managment made easy_

Nancy CLI is a CLI implementation of finance (majorly budgeting)  management tool using Python as the scripted language and pandas as the data structures.

Files
Program overview

* - incomplete

_account.py_
Account creates and manages wallets. A wallets simply its name and the amount of money corresponding to it. A wallet could have an extra layer called the sub-wallet, in which case the wallet is a super-wallet. A sub-wallet has the same characteristics as a wallet except that the amount allocated to it is a fraction of the super-wallet. Transfer can be made between, into, and out of wallets.

_formula.py*_
Wallets, budgetlist and wishlist items, credit and debit can be aggregated together using formula. The aforementioned classes just require and their indicator be written alongside any arithmetic operation.

_budget_and_wishlist.py*_
Budget helps keep track of what items have been stipulated for purchased. Reminders can be set indicate that an item needs be purchased. Priority can also be set to indicate whether or not the item needs be purchased urgently.
Wishlist keeps track of items you wish to purchase at a later time and helps you save towards them.

_credit_and_debit.py_
This keeps track of who is owed and who owes.
