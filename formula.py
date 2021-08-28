import json
import pprint

class Formula:
    def __init__(self) -> None:
        self.formulae = self.user_formula_data()

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
            pass

        return formulae

    def add_formula(self):
        formula = input("Enter the name of the formula: ")
        if formula in list(self.formulae.keys()):
            print("Formula name already exists.")
        else:
            print("Formula contains values or operations.")
            print("Values could be wallet, budget, or wishlist.")
            print("Operations are arithmetic.\n")     
        pass

    def del_formula(self):
        pprint.pp(self.formulae)
        formula = input("Enter the name of the formula to be deleted: ")
        try:
            self.formulae.pop(formula)
        except KeyError:
            print("Formula does not exist!")
        else:
            pass

    def evl_formula(self):
        pprint.pp(self.formulae)
        formula = input("Enter the name of the formula to be evaluated: ")
        pass