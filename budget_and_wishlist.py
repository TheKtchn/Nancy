import pandas
class BudgetList:
    def __init__(self, username) -> None:
        self.username = username
        self.moneydata = self.user_budg_list_data()
        
    def user_budg_list_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_budg_list.csv")
        except FileNotFoundError:
            data = pandas.DataFrame([], columns=["item", "description", "cost", "is_repeated"])
            data.to_csv(f"user_{self.username}_budg_list.csv")
        else:
            print("Printing your budget items.\n\n")
            print(data)
        return data

    def add_budg_list_item(self):
        frames = {
            "item": [],
            "description": [],
            "tags": [],
            "cost": [],
            "is_repeated": []
        }

        while True:
            item = input("Enter the item( q to end): ")
            if item == 'q':
                print("Items added!")
                break
            tags = input("What categories do item(s) fall under? ").split(", ") 
            cost = float(input("Enter the cost of the items: "))
            description = input("Enter the description of the item: ")
            repeat = input("Is it recurring(True or False)? ")

            frames["item"].append(item)
            frames["tags"].append(tags)
            frames["description"].append(description)
            frames["cost"].append(cost)
            frames["is_repeated"].append(repeat)

        df = pandas.DataFrame(frames)
        self.moneydata = pandas.concat(
            [self.moneydata, df],
            axis=0,
            join="outer", 
            ignore_index=False, 
            keys=None, 
            levels=None, 
            names=None, 
            verify_integrity=False, 
            copy=True)
        
        self.moneydata.to_csv(f"user_{self.username}_budg_list.csv")


budg = BudgetList("victor17")
budg.add_budg_list_item()