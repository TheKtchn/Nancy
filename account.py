import numpy
import pandas

class Account:
    def __init__(self) -> None:
        self.name = input('What is your name? ')
        self.username = input('What is your username? ')
        self.acct = None
        self.user_id_data()
        self.user_account_data()

    def user_id_data(self) -> None:
        try:
            id = open(f"{self.username}.txt", 'r')
        except FileNotFoundError:
            id = open(f"{self.username}.txt", 'w')
            id.write(f"{self.name}")
            id.write(f"{self.username}")
            print(f"id created for {self.username}.")
            id.close()
        else:
            print("Account already exists. Retrieving data")
            self.acct = id.readlines()
            id.close()

    def user_account_data(self) -> None:
        try:
            data = pandas.read_csv(f"{self.username}.csv")
        except FileNotFoundError:
            wallets = []
            while True:
                wallet_name = input("Enter the name of the wallet: ")
                if wallet_name == "q":
                    break
                while True:
                    try:
                        wallet_amount = int(input("Enter the amount in the wallet: "))
                    except ValueError:
                        print("You entered a wrong value!")
                    else:
                        wallets.append([wallet_name, wallet_amount])
                        break
                    print("\n")
            data = pandas.DataFrame(wallets, columns=["wallet name", "wallet amount"])
            data.to_csv(f"{self.username}.csv")
        else:
            print(data)
