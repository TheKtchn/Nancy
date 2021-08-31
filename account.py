import itertools
import json
import pandas
import pprint
 
class Account:
    def __init__(self) -> None:
        """Initialises files relating to wallet information"""

        self.username = input('What is your username(unique ID)? ')
        self.name = None        
        self.id = self.user_id_data()
        self.data, self.formulae = self.user_account_data()

    def _wallet_manager(self):
        """Sorts out the wallet information into wallet information and wallet dataframes"""
        
        # retrieves wallet and sub-wallet names
        wallet_list = list(self.data.index.values)

        wllt_names = {}
        for wllt, s_wllt in wallet_list:
            wllt_names.setdefault(wllt, []).append(s_wllt)

        # stores each wallet with its sub-wallets as its own dataframe for easy access
        wallet_info = {wllt_name: self.data.loc[wllt_name] for wllt_name in list(wllt_names.keys())}


        return (wllt_names, wallet_info, wallet_list)

    def _wallet_parser(self, wallet_info):
        wllt_info = [[], []]
        wllt_values = []
        print()
        pprint.pp(wallet_info, indent=4)
        print()
        for key, value in wallet_info.items():
            wllt_info[0] += list(itertools.repeat(key, len(list(value.index.values))))
            wllt_info[1] += list(value.index.values)
            wllt_values += list(value["amount"])
        
        tupls = list(zip(*wllt_info))
        index = pandas.MultiIndex.from_tuples(tupls, names=['wallet', "sub_wallet"])
        self.data = pandas.DataFrame(wllt_values, index=index, columns=["amount"])
        self.data.to_csv(f"user_{self.username}_wallets.csv")

    @staticmethod
    def _float_input_validator(inpt_sttmnt):
        while True:
            try: 
                value = float(input(f"{inpt_sttmnt}"))
            except ValueError:
                print("Value entered is invalid.\n")
            else:
                break
                
        return value

    # User account ID creation and management
    def user_id_data(self) -> None:
        """Manages user ID information"""
        
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
            
    # User account data creation and management
    def user_account_data(self) -> pandas.DataFrame:
        """Checks for presence of wallets and formulae files, if not present creates the necessary files"""

        # wallet data file initialiser
        try:
            data = pandas.DataFrame(pandas.read_csv(f"user_{self.username}_wallets.csv", index_col=[0, 1]))
        except FileNotFoundError:
            data = pandas.DataFrame(columns=["wallet", "sub_wallet", "amount"])
            data.to_csv(f"user_{self.username}_wallets.csv")
        else:
            pass

        # formulae data file initialiser
        try:
            with open(f"user_{self.username}_formulae.json") as file:
                formulae = json.load(file)
        except FileNotFoundError:
            with open(f"user_{self.username}_formulae.json", "w") as file:
                formulae = {}
                json.dump(formulae, file)
        else:
            pass
            
        return (data, formulae)

    def add_wallet(self):
        """Manages the creation of wallet and sub-wallets and additions to existing wallets."""

        wllt_names, wallet_info, _ = self._wallet_manager()

        while True:
            wallet_name = input("Enter the name of the wallet(q to end): ").lower().replace(" ", "_")
            if wallet_name == "q":
                print("Wallet(s) successfully created!")
                break

            # if wallet is already created
            elif wallet_name in wllt_names:
                print(f"Wallet already created!\nWallets created are {wllt_names}")

                # manages and resolves wallet name conflicts
                if input("Do you want to add new sub-wallet(s)(y/n): ") == 'y':
                    while True:
                        sub_wallet_name = input("Enter the name of the new sub-wallet(q to end): ").lower().replace(" ", "_")
                        if (sub_wallet_name == 'q'):
                            break
                        else:
                            if sub_wallet_name in wllt_names[wallet_name]:
                                print("Sub-wallet already exists!")
                            else:
                                wllt_names[wallet_name].append(sub_wallet_name)
                                sub_wallet_amount = Account._float_input_validator("Enter the amount in the sub-wallet: ")
                                wallet_info[wallet_name].loc[sub_wallet_name] = sub_wallet_amount
                print()

            # creates a new wallet if no conflicts in wallet names are found
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
                        sub_wallet_amount = Account._float_input_validator("Enter the amount in the sub-wallet: ")
                        wallet_info[wallet_name].loc[sub_wallet_name] = sub_wallet_amount

                else: 
                    wllt_names[wallet_name].append(wallet_name)
                    sub_wallet_amount = Account._float_input_validator("Enter the amount in the wallet: ")
                    wallet_info[wallet_name].loc[wallet_name] = sub_wallet_amount
      
        self._wallet_parser(wallet_info)

    def remove_wallet(self):
        """Manages the deletion of wallets and/or sub-wallets"""

        wllt_names, wallet_info, _ = self._wallet_manager()

        print()
        pprint.pp(wllt_names)
        print()
        print("Enter the name of the wallet and/or sub-wallet to be removed.")
        print("When entering wallet and sub-wallet put a colon between them.")
        removal = input("Enter here: ")
        if len(removal.split(":")) == 2:
            wallet_info[removal.split(":")[0]].drop(removal.split(":")[1], inplace=True)
        else:
            if removal in list(wllt_names.keys()):
                # check if name entered is a wallet, remove all wallet info and perform necessary transfer
                print("Deleting entire wallet!")
                wallet_info.pop(removal)
            else:
                wllts_with_swllt = []
                for i, j in wllt_names.items():
                    if removal in j:
                        wllts_with_swllt.append(i)
                if len(wllts_with_swllt) == 1:
                    # check if sub-wallet entered has no conflicts, if so remove and perform necessary transfer
                    wallet_info[wllts_with_swllt[0]].drop(removal, inplace=True)
                    print("Sub-wallet successfully removed.\n")
                else:
                    # check if sub-wallet entered has conflicts, if so remove and perform necessary transfer
                    pprint.pp({wllts_with_swllt.index(value): value for value in wllts_with_swllt})
                    indx = int(self._float_input_validator(inpt_sttmnt="Enter the index of the wallet: "))
                    wallet_info[wllts_with_swllt[indx]].drop(removal, inplace=True)
                    print("Sub-wallet successfully removed.\n")

        self._wallet_parser(wallet_info)

    def wallet_transfer(self):
        """Ensure seamless transfer between wallets themselves and from other sources"""

        wllt_names, _, _ = self._wallet_manager()

        print()
        pprint.pp(wllt_names)
        print()

        print("Enter the name of wallet and sub-wallet seperated by a colon.")
        print("If transfer is to or from another entity, enter other and the entity's name seperated by a colon.")
        fro = input("from: ")
        to = input("to: ")

        amount = Account._float_input_validator("Enter the amount transferred: ")

        if fro[:5] != "other":
            while self.data.loc[fro.split(":")[0], fro.split(":")[1]] < amount:
                print("Amount to be transferred is greater than amount in wallet.")
                amount = Account._float_input_validator("Enter the amount transferred: ")
            self.data.loc[fro.split(":")[0], fro.split(":")[1]] = self.data.loc[fro.split(":")[0], fro.split(":")[1]] - amount
            if to[:5] != "other":
                self.data.loc[to.split(":")[0], to.split(":")[1]] = self.data.loc[to.split(":")[0], to.split(":")[1]] + amount

        self.data.to_csv(f"user_{self.username}_wallets.csv")
        print("Transfer complete!")

    def add_del_evl_formula(self) -> None:
        """Manages the creation, deletion, and evaluation of special wallets that calculates the value of the given formula"""

        # Make sure formula addition and deletion is properly implemented
        formula_name = input("Enter the name of your formula(to delete put d- before name): ")
        if formula_name[:2] == 'd-':
            try:
                self.formulae.pop(formula_name[2:])
                with open(f"user_{self.username}_formulae.json", "w") as file:
                    json.dump(self.formulae, file)
            except KeyError:
                print("Formula does not exist!")
        else:
            try:
                formula = self.formulae[formula_name]         
            # formula creator
            except KeyError:
                print("Formula doesn't exist. Creating a new one.\n")
                formula_variables, _, wllts  = self._wallet_manager()

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
                        print("Formula created")
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
checks.add_del_evl_formula()