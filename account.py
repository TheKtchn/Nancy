import json
import pandas
import pprint

class Account:
    def __init__(self) -> None:
        self.username = input('What is your username(unique ID)? ')
        self.name = None        
        self.user_id_data()
        self.data = self.user_account_data()

    # User account ID creation and management
    def user_id_data(self) -> None:
        try:
            id = open(f"user_{self.username}.txt", 'r')
        except FileNotFoundError:
            id = open(f"user_{self.username}.txt", 'w')
            print("Creating your account...\n")
            self.name = input('What is your name? ')
            id.write(f"{self.name} ")
            id.write(f"{self.username}")
            print(f"ID created for {self.username}.")
            id.close()
        else:
            print("Account sign-in complete. Retrieving data\n")
            acct = id.readlines()
            acct = acct[0].split(' ')[:-1]
            self.name = f"{acct[0]} {acct[1]}"
            id.close()
        return self.name, self.username
            
    # User wallets creation and management
    def user_account_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_data.csv", index_col=[0, 1])
        except FileNotFoundError:
            print("Creating your wallet(s). Enter relevant info.\n")
            wallet_info = [[], []] # wallet info contains names of wallets and sub-wallets
            wallet_amounts = [] # wallet amounts contains amount in each wallets

            while True: # wallets
                wallet_names = []
                wallet_name = input("Enter the name of the wallet(q to end): ").lower().replace(" ", "_")
                if wallet_name == 'q':
                    break
                wallet_names.append(wallet_name)
                sub_wallet_names = []
                sub_wallet_amounts = []

                # sub_wallets
                if input("Does the wallet have sub-wallets(y/n)? ") == 'y':
                    while True:
                        sub_wallet_name = input("Enter the name of the sub-wallet(q to end): ").lower().replace(" ", "_")
                        if (sub_wallet_name == 'q'):
                            sub_wallet_names.append("total")
                            sub_wallet_amounts.append(sum(sub_wallet_amounts))
                            break
                        sub_wallet_names.append(sub_wallet_name)
                        wallet_names.append(wallet_name)
                        while True:
                            try:
                                sub_wallet_amount = float(input("Enter the amount in the sub-wallet: "))
                            except ValueError:
                                print("Value entered is not a number.\n") 
                            else:
                                sub_wallet_amounts.append(sub_wallet_amount)
                                break

                # wallet without sub_wallet
                else: 
                    sub_wallet_names.append("total")
                    while True:
                            try:
                                wallet_amount = float(input("Enter the amount in the wallet: "))
                            except ValueError:
                                print("Value entered is not a number.\n") 
                            else:
                                sub_wallet_amounts.append(wallet_amount)
                                break
                                

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
        wllts = list(self.data.index.values)
        try:
            with open(f"user_{self.username}_formulae.json") as formulae:
                f = json.load(formulae)
        except FileNotFoundError:
            with open(f"user_{self.username}_formulae.json", "w") as formulae:
                json.dump({}, formulae)
        else:
            formula_name = input("Enter the name of your formula: ")
            try:
                formula = f[formula_name]            
            # formula creator
            except KeyError:
                print("Formula doesn't exist. Creating a new one.\n")
                formula_variables = {}
                for wllt, s_wllt in wllts:
                    formula_variables.setdefault(wllt, []).append(s_wllt)

                print("wallet: [sub_wallets]")
                pprint.pp(formula_variables)
                print("\n\n")

                print("Formula format:")
                print("variable operation variable etc.")
                print("variable could be wallet(wallet:subwallet) or value")
                print("operation is arithmetic\n")

                # checks if formula entered contains valid wallets
                while True:
                    formula = input("Enter the formula: ")
                    formula = formula.split(" ")
                    print(formula)
                    complete = True
                    for i in range(0, len(formula), 2):
                        var = tuple(formula[i].split(":"))
                        if var not in wllts:
                            complete = False
                            print("Wrong formula entered.\n")
                            break
                    if complete:
                        break
                
                with open(f"user_{self.username}_formulae.json", "w") as formulae:
                    f[formula_name] = formula
                    json.dump(f, formulae)
            
            # formula calculator
            else:
                for i in range(0, len(formula), 2):
                    var = formula[i].split(":")
                    if len(var) == 2:
                        formula[i] = str(self.data.loc[var[0], var[1]]["amount"])

                formula_str = ""
                for i in formula:
                    formula_str += i
                print(eval(formula_str))
