import datetime
import pandas
class BudgetList:

    def __init__(self, username) -> None:
        self.username = username
        self.moneydata = self.user_list_data()
        
    def user_list_data(self) -> pandas.DataFrame:
        try:
            data = pandas.DataFrame(pandas.read_csv(f"user_{self.username}_budg_list.csv", index_col=[0]))
        except FileNotFoundError:
            data = pandas.DataFrame([], columns=["item", "tags", "description", "cost", "reminder", "repeat_info", "skip"])
            data.to_csv(f"user_{self.username}_budg_list.csv")
            print(f"Created a budg file for user {self.username}!")
        else:
            data["reminder"] = pandas.to_datetime(data["reminder"])
            data["skip"] = pandas.to_datetime(data["skip"])
        return data

    def add_list_item(self):
        frames = {}
        print(list(self.moneydata.columns))
        for i in list(self.moneydata.columns):
            frames[i] = []

        while True:
            item = input("Enter the item(q to end): ")
            if item == 'q':
                print("Items added!")
                break
            tags = input("What categories do item(s) fall under? ")
            description = input("Enter O for one time or P for piece of pie: ")

            while True:
                try: 
                    cost = float(input("Enter the cost of the item(s): "))
                except ValueError:
                    print("Value entered is invalid.\n")
                else:
                    break
            if description == 'P':
                description = f'{cost}P'    
            while True:
                try:
                    reminder = pandas.to_datetime(input("Enter date(YYYY-MM-DD): "))
                except ValueError:
                    print("Date entered can't be parsed.\nEnter date in YYYY-MM-DD format.")
                else:
                    break
            repeat_info = input("How often? ")
            # once
            # 2 D
            # 2 W
            # Mo:Tu of 2 W
            # Mo-Fr of 2 W
            # 2 M
            # 1:2 of 2 M
            # 1-3 of 2 M
            # 1Sat:1Sun of 2 M
            # 1Sat-1Mon of 2 M
            # 1 Y        

            frames["item"].append(item)
            frames["tags"].append(tags)
            frames["description"].append(description)
            frames["cost"].append(cost)
            frames["reminder"].append(reminder)
            frames["repeat_info"].append(repeat_info)
            frames["skip"].append(reminder)
            # skip involves moving or extending the date already specified

        df = pandas.DataFrame(frames)
        self.moneydata = pandas.concat([self.moneydata, df])
        self.moneydata.sort_values(by=["reminder"], inplace=True)
        self.moneydata.to_csv(f"user_{self.username}_budg_list.csv")
        
    def remind_manager(self):
        fltr = (self.moneydata["reminder"] <= datetime.datetime(2021, 12, 12))
        fltr = self.moneydata[fltr]
        fltr.set_index("item", inplace=True)
        items = list(fltr.index)
        outstanding = {}
        remainder = {}
        for i in items:
            if fltr.loc[i, 'description'] == 'O':
                outstanding[i] = fltr.loc[i, "cost"]
            else:
                remainder[i] = float(fltr.loc[i, "description"][:-1])

    def skip(self):
        pass
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
budgeter = BudgetList(username)
# budgeter.add_list_item()
budgeter.remind_manager()

