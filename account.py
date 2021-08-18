import json
import pandas
import pprint
import itertools
 
class Account:
    def __init__(self) -> None:
        self.username = input('What is your username(unique ID)? ')
        self.name = None        
        self.user_id_data()
        self.data, self.formulae = self.user_account_data()

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
        # wallet data file initialiser
        try:
            data = pandas.DataFrame(pandas.read_csv(f"user_{self.username}_wallets.csv", index_col=[0, 1]))
        except FileNotFoundError:
            data = pandas.DataFrame(columns=["wallet", "sub_wallet", "amount"])
            data.to_csv(f"user_{self.username}_wallets.csv")
            print(f"Created a wallet file for user {self.username}!")
        else:
            print("\nAccount ID details retrieved.")
            # print(data)

        # formulae data file initialiser
        try:
            with open(f"user_{self.username}_formulae.json") as file:
                formulae = json.load(file)
        except FileNotFoundError:
            with open(f"user_{self.username}_formulae.json", "w") as file:
                formulae = {}
                json.dump(formulae, file)
        else:
            print("\nFormulae retrieved.")
            # print(formulae)
            
        return (data, formulae)

    def add_wallet(self):
        wllt_names = {}
        for wllt, s_wllt in list(self.data.index.values):
            wllt_names.setdefault(wllt, []).append(s_wllt)
        wallet_info = {wllt_name: self.data.loc[wllt_name] for wllt_name in list(wllt_names.keys())}
        while True:
            wallet_name = input("Enter the name of the wallet(q to end): ").lower().replace(" ", "_")
            if wallet_name == "q":
                print("Wallet(s) successfully created!")
                break
            elif wallet_name in wllt_names:
                print(f"Wallet already created!\nWallets created are {wllt_names}")
                if input("Do you want to add a new sub-wallet(y/n): ") == 'y':
                    while True:
                        sub_wallet_name = input("Enter the name of the new sub-wallet(q to end): ").lower().replace(" ", "_")
                        if (sub_wallet_name == 'q'):
                            break
                        else:
                            if sub_wallet_name in wllt_names[wallet_name]:
                                print("Sub-wallet already exists!")
                            else:
                                wllt_names[wallet_name].append(sub_wallet_name)
                                while True:
                                    try:
                                        sub_wallet_amount = float(input("Enter the amount in the sub-wallet: "))
                                    except ValueError:
                                        print("Value entered is not a number.\n") 
                                    else:
                                        wallet_info[wallet_name].loc[sub_wallet_name] = sub_wallet_amount
                                        break
                    pass
            else:
                wallet_info[wallet_name] = pandas.DataFrame(columns=["sub_wallet", "amount"])
                wallet_info[wallet_name].set_index("sub_wallet", inplace=True)
                wllt_names[wallet_name] = []
                if input("Does the wallet have sub-wallets(y/n)? ") == 'y':
                    while True:
                        sub_wallet_name = input("Enter the name of the sub-wallet(q to end): ").lower().replace(" ", "_")
                        if (sub_wallet_name == 'q'):
                            break
                        wllt_names[wallet_name].append(sub_wallet_name)
                        while True:
                            try:
                                sub_wallet_amount = float(input("Enter the amount in the sub-wallet: "))
                            except ValueError:
                                print("Value entered is not a number.\n")
                            else:
                                wallet_info[wallet_name].loc[sub_wallet_name] = sub_wallet_amount
                                break
                else: 
                    while True:
                        try:
                            sub_wallet_amount = float(input("Enter the amount in the wallet: "))
                        except ValueError:
                            print("Value entered is not a number.\n") 
                        else:
                            wallet_info[wallet_name].loc[f"_{wallet_name}_"] = sub_wallet_amount
                            break
        
        wllt_info = [[], []]
        wllt_values = []
        pprint.pp(wallet_info)
        for key, value in wallet_info.items():
            wllt_info[0] += list(itertools.repeat(key, len(list(value.index.values))))
            wllt_info[1] += list(value.index.values)
            wllt_values += list(value["amount"])
        
        tupls = list(zip(*wllt_info))
        index = pandas.MultiIndex.from_tuples(tupls, names=['wallet', "sub_wallet"])
        self.data = pandas.DataFrame(wllt_values, index=index, columns=["amount"])
        self.data.to_csv(f"user_{self.username}_wallets.csv")

    def remove_wallet(self):
        wllt_names = {}
        for wllt, s_wllt in list(self.data.index.values):
            wllt_names.setdefault(wllt, []).append(s_wllt)
        wallet_info = {wllt_name: self.data.loc[wllt_name] for wllt_name in list(wllt_names.keys())}

        print()
        pprint.pp(wllt_names)
        print()
        print("Enter the name of the wallet and/or sub-wallet to be removed.")
        print("When entering wallet and sub-wallet put a colon between them.")
        removal = input("Enter here: ")
        if len(removal.split(":")) == 2:
            pass
        else:
            if removal in list(wllt_names.keys()):
                pass
            else:
                wllt_with_swllt = []
                for i, j in wllt_names.items():
                    if removal in j:
                        wllt_with_swllt.append(i)
                if len(wllt_with_swllt) == 1:
                    pass
                else:
                    pass
            

    def wallet_transfer(self, fro, to=None):
        pass


    def add_or_sub_formula(self) -> None:
        formula_name = input("Enter the name of your formula: ")
        try:
            formula = self.formulae[formula_name]         
        # formula creator
        except KeyError:
            print("Formula doesn't exist. Creating a new one.\n")
            # wallet names getter
            wllts = list(self.data.index.values)
            formula_variables = {}
            for wllt, s_wllt in wllts:
                formula_variables.setdefault(wllt, []).append(s_wllt)

            print("wallet: [sub_wallets]")
            pprint.pp(formula_variables)
            print("\n\n")

            print("Formula format instructions:")
            print("variable operation variable etc.")
            print("variable could be wallet(wallet:subwallet)")
            print("ensure a space is placed between any variables and operations")
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
            
            with open(f"user_{self.username}_formulae.json", "w") as file:
                self.formulae[formula_name] = formula
                json.dump(self.formulae, file)
        
        # formula evaluator - check the formula and print its value
        else:
            for i in range(0, len(formula), 2):
                var = formula[i].split(":")
                if len(var) == 2:
                    formula[i] = str(self.data.loc[var[0], var[1]]["amount"])

            formula_str = ""
            for i in formula:
                formula_str += i
            print(eval(formula_str))

checks = Account()
checks.remove_wallet()
