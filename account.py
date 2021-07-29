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
        try:
            data = pandas.read_csv(f"user_{self.username}_data.csv")
        except FileNotFoundError:
            wallet_info = [[], []]
            wallet_amounts = []
            while True:
                wallet_names = []
                wallet_name = input("Enter the name of the wallet: ")
                if wallet_name == 'q':
                    break
                wallet_names.append(wallet_name)
                sub_wallet_names = []
                sub_wallet_amounts = []
                if input("Does the wallet have sub-wallets(y/n)? ") == 'y':
                    while True:
                        sub_wallet_name = input("Enter the name of the sub-wallet: ")
                        if (sub_wallet_name == 'q'):
                            sub_wallet_names.append("total")
                            sub_wallet_amounts.append(sum(sub_wallet_amounts))
                            break
                        sub_wallet_names.append(sub_wallet_name)
                        wallet_names.append(wallet_name)
                        
                        sub_wallet_amount = float(input("Enter the amount in the sub-wallet: "))
                        sub_wallet_amounts.append(sub_wallet_amount)
                else:
                    sub_wallet_names.append("total")
                    sub_wallet_amounts.append(input("Enter the amount in the wallet: "))

                wallet_info[0] += wallet_names
                wallet_info[1] += sub_wallet_names
                wallet_amounts += sub_wallet_amounts
            if len(wallet_info[0]) > 0:
                tuples = list(zip(*wallet_info))  
                index = pandas.MultiIndex.from_tuples(tuples=tuples, names=["wallet", "sub_wallet"])
                data = pandas.DataFrame(wallet_amounts, index=index)
                print(data)
                data.to_csv(f"user_{self.username}_data.csv")
        else:
            print(data)

        @staticmethod
        def error_catcher(cls):
            pass