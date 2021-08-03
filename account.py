import json
import pandas
import pprint

class Account:
    def __init__(self) -> None:
        self.name = input('What is your name? ')
        self.username = input('What is your username? ')
        self.user_id_data()
        self.data = self.user_account_data()

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
            print("Account already exists. Retrieving data\n")
            acct = id.readlines()
            acct = acct[0].split(' ')[:-1]
            self.name = f"{acct[0]} {acct[1]}"
            id.close()
            
    # User wallets creation and management
    def user_account_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_data.csv", index_col=[0, 1])
        except FileNotFoundError:
            print("Creating your wallet(s). Enter relevant info.\n")
            wallet_info = [[], []] #wallet info contains names of wallets and sub-wallets
            wallet_amounts = []
            while True:
                wallet_names = []
                wallet_name = input("Enter the name of the wallet(q to end): ").lower().replace(" ", "_")
                if wallet_name == 'q':
                    break
                wallet_names.append(wallet_name)
                sub_wallet_names = []
                sub_wallet_amounts = []
                if input("Does the wallet have sub-wallets(y/n)? ") == 'y':
                    while True:
                        sub_wallet_name = input("Enter the name of the sub-wallet(q to end): ").lower().replace(" ", "_")
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
                data = pandas.DataFrame(wallet_amounts, index=index, columns=["amount"])
                print(data)
                data.to_csv(f"user_{self.username}_data.csv")
        else:
            print(data)
            print("\n\n")
            

        return data
    def formula(self) -> None:
        try:
            with open(f"user_{self.username}_formulae.json") as formulae:
                f = json.load(formulae)
        except FileNotFoundError:
            with open(f"user_{self.username}_formulae.json", "w") as formulae:
                json.dump({}, formulae)
        else:
            try:
                formula_name = input("Enter the name of your formula: ")
                formula = f[formula_name]
            except KeyError:
                print("Formula doesn't exist. Creating a new one.\n")
                formula_variables = {}
                for wllt, s_wllt in self.data.index.values:
                    formula_variables.setdefault(wllt, []).append(s_wllt)

                print("wallet: [sub_wallets]")
                pprint.pp(formula_variables)
                print("\n\n")

                print("Formula format:")
                print("variable operation variable etc.")
                print("variable could be wallet(wallet:subwallet) or value")
                print("operation is arithmetic\n")

                formula = input("Enter the formula: ")
                with open(f"user_{self.username}_formulae.json", "w") as formulae:
                    f[formula_name] = formula
                    json.dump(f, formulae)
                # cash_in_hand:total * 2 + savings:cowrywise
            else:
                pass
            finally:
                formula = formula.split(" ")
                for i in range(0, len(formula), 2):
                    var = formula[i].split(":")
                    if len(var) == 2:
                        formula[i] = str(self.data.loc[var[0], var[1]]["amount"])

                formula_str = ""
                for i in formula:
                    formula_str += i
                print(eval(formula_str))


checks = Account()
checks.formula()