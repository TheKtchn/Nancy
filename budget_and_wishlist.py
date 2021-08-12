import pandas


class List:
    def __init__(self, username, listtype) -> None:
        self.username = username
        self.listtype = listtype
        self.moneydata = self.user_list_data()
        
    def user_list_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_{self.listtype}_list.csv")
        except FileNotFoundError:
            data = pandas.DataFrame([], columns=["item", "tags", "description", "cost", "is_repeated", "repeat_info"])
            data.to_csv(f"user_{self.username}_{self.listtype}_list.csv")
        else:
            print(data)
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
            cost = float(input("Enter the cost of the items: "))
            repeat = input("Is it recurring(True or False)? ")
            repeat_information = []
            if repeat == "True":
                repeat_information.append(input("How often? "))
                repeat_information.append(input("Start date: "))
                repeat_information.append(input("When do you wanna be reminded? "))

            frames["item"].append(item)
            frames["tags"].append(tags)
            frames["description"].append(description)
            frames["cost"].append(cost)
            frames["is_repeated"].append(repeat)
            frames["repeat_info"].append(repeat_information)

        df = pandas.DataFrame(frames)
        self.moneydata = pandas.concat([self.moneydata, df])
        self.moneydata.to_csv(f"user_{self.username}_{self.listtype}_list.csv")

class BudgetList(List):
    def __init__(self, username) -> None:
        LISTTYPE = "budg" 
        super().__init__(username, LISTTYPE)
        
    
class WishList(List):
    def __init__(self, username) -> None:
        LISTTYPE = "wish" 
        super().__init__(username, LISTTYPE)

username = "victor17"
wisher = WishList(username)
budgeter = BudgetList(username)

    