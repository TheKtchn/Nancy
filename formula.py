import json
import pprint

class Formula:
    def __init__(self, username) -> None:
        self.username = username
        self.formulae = self.user_formula_data()

    @staticmethod
    def num_checker(num):
        try:
            float(num)
        except ValueError:
            return False
        else:
            return True

    def user_formula_data(self):
        # formulae data file initialiser
        try:
            with open(f"user_{self.username}_formulae.json") as file:
                formulae = json.load(file)
        except FileNotFoundError:
            with open(f"user_{self.username}_formulae.json", "w") as file:
                formulae = {}
                json.dump(formulae, file)
        else:
            print(formulae)

        return formulae

    def add_formula(self):
        formula_name = input("Enter the name of the formula: ")
        if formula_name in list(self.formulae.keys()):
            print("Formula name already exists.")
        else:
            print("Formula contains values or operations.")
            print("Values could be wallet, credit, debit, budget, and/or wishlist.")
            print("Operations are simple arithmetic.\n")

            formula = input("Enter formula: ").lower().split()
            correct = True
            if len(formula) / 2 != 0:
                # split into values and operations
                formula_vals = formula[::2] 
                formula_ops = formula[1::2]
                # variables contains list of possible filters for the named lists
                variables = None
                
                correct = True
                brckts = 0
                for i in formula_ops: # confirm if formula has valid operators
                    if i not in ['+', '-', '*', '/', '^', '%', '>', '<', '>=', '<=', '==', '!=', '&', '|', '~']:
                        correct = False
                        break

                if correct:
                    for i in formula_vals: # value validator
                        if ':' in i: # otherwise check if value is a wallet:subwallet or variable:filter
                            a, b = i.split(":")
                            a = a[1:] if a[0] == '(' else a
                            b = b[1:] if b[0] == ')' else b

                            if a in variables: # variable:filter
                                if a in ["budg", "cred", "debt", "wish"]:
                                    if a == "budg":
                                        correct = False
                                    elif a in ["cred", "debt"]:
                                        correct = False
                                    else:
                                        correct = False
                        elif not Formula.num_checker(i):
                            correct = False

                        if not correct:
                            break
                if not correct:
                    print("Formula has incorrect variable entries.")
            else:
                print("Formula likely can't be calculated because it contains unresolved operations.")

    def del_formula(self):
        pprint.pp(self.formulae)
        formula_name = input("Enter the name of the formula to be deleted: ")
        try:
            self.formulae.pop(formula_name)
        except KeyError:
            print("Formula does not exist!")
        else:
            pass

    def evl_formula(self):
        pprint.pp(self.formulae)
        formula_name = input("Enter the name of the formula to be evaluated: ")
        # evaluator is first to check for bracket groupings then obtain values for such expression working from outside in
        pass

form = Formula("victor17")
form.add_formula()