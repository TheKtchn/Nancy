import pandas

class Account:
    def __init__(self) -> None:
        self.name = input('What is your name? ')
        self.username = input('What is your username? ')
        self.user_id_data()
        self.user_account_data()

    # User account ID creation and management
    def user_id_data(self) -> None:
        try:
            id = open(f"user_{self.username}.txt", 'r')
        except FileNotFoundError:
            id = open(f"user_{self.username}.txt", 'w')
            id.write(f"{self.name} ")
            id.write(f"{self.username}")
            print(f"ID created for {self.username}.")
            id.close()
        else:
            print("Account already exists. Retrieving data")
            acct = id.readlines()
            acct = acct[0].split(' ')[:-1]
            self.name = f"{acct[0]} {acct[1]}"
            id.close()
            
    # User wallets creation and management
    def user_account_data(self) -> None:
        # pass
        try:
            data = pandas.read_csv(f"user_{self.username}_data.csv")
        except FileNotFoundError:
            wallets = {"wallet_name": [], 
                       "wallet_amount": []}
            while True:
                wallet_name = input("Enter the name of the wallet: ")
                if wallet_name == "q":
                    break
                wallets["wallet_name"].append(wallet_name)
                while True:
                    try:
                        wallet_amount = float(input("Enter the amount in the wallet: "))
                    except ValueError:
                        print("You entered a wrong value!")
                    else:
                        wallets["wallet_amount"].append(wallet_amount)
                        break
                    print("\n")
            data = pandas.DataFrame(wallets)
            data.to_csv(f"user_{self.username}_data.csv")
        else:
            print(data)
