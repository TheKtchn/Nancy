import pandas

class BudgetList:

    def __init__(self, username) -> None:
        self.username = username
        self.moneydata = self.user_list_data()
        
    def user_list_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_budg_list.csv")
        except FileNotFoundError:
            data = pandas.DataFrame([], columns=["item", "tags", "description", "cost", "reminder", "repeat_info"])
            data.to_csv(f"user_{self.username}_budg_list.csv")
            print(f"Created a budg file for user {self.username}!")
        else:
           pass
        return data

    def add_list_item(self):
        frames = {}
        for i in list(self.moneydata.columns)[1:]:
            frames[i] = []

        while True:
            item = input("Enter the item(q to end): ")
            if item == 'q':
                print("Items added!")
                break
            tags = input("What categories do item(s) fall under? ").split(", ") 
            description = input("Enter the description of the item: ")
            cost = float(input("Enter the cost of the item(s): "))
            while True:
                try:
                    reminder = pandas.Timestamp(input("Enter date: "))
                except ValueError:
                    print("Date entered can't be parsed.\nEnter date in YYYY-MM-DD format.")
                else:
                    break
            repeat_info = input("How often? ")                            

            frames["item"].append(item)
            frames["tags"].append(tags)
            frames["description"].append(description)
            frames["cost"].append(cost)
            frames["reminder"].append(reminder)
            frames["repeat_info"].append(repeat_info)

        df = pandas.DataFrame(frames)
        self.moneydata = pandas.concat([self.moneydata, df])
        self.moneydata.to_csv(f"user_{self.username}_budg_list.csv")
    
class WishList:
    def __init__(self, username) -> None:
        self.username = username
        self.moneydata = self.user_list_data()
        
    def user_list_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_wish_list.csv")
        except FileNotFoundError:
            data = pandas.DataFrame([], columns=["item", "tags", "description", "cost", "repeat_info"])
            data.to_csv(f"user_{self.username}_wish_list.csv")
            print(f"Created a wish file for user {self.username}!")
        else:
           pass
        return data

    def add_list_item(self):
        frames = {}
        for i in list(self.moneydata.columns)[1:]:
            frames[i] = []

        while True:
            item = input("Enter the item(q to end): ")
            if item == 'q':
                print("Items added!")
                break
            tags = input("What categories do item(s) fall under? ").split(", ") 
            description = input("Enter the description of the item: ")
            cost = float(input("Enter the cost of the item(s): "))
            repeat_info = input("How often? ")                            

            frames["item"].append(item)
            frames["tags"].append(tags)
            frames["description"].append(description)
            frames["cost"].append(cost)
            frames["repeat_info"].append(repeat_info)

        df = pandas.DataFrame(frames)
        self.moneydata = pandas.concat([self.moneydata, df])
        self.moneydata.to_csv(f"user_{self.username}_wish_list.csv")

username = "victor17"
wisher = WishList(username)
budgeter = BudgetList(username)

wisher.add_list_item()
budgeter.add_list_item()
