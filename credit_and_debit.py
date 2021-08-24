import pandas

class Cr_Dr:
    def __init__(self, username) -> None:
        self.username = username
        self.cr_dr = self.user_cr_dr_data()

    def user_cr_dr_data(self) -> pandas.DataFrame:
        try:
            data = pandas.read_csv(f"user_{self.username}_cr_dr.csv")
        except FileNotFoundError:
            data = pandas.DataFrame([], columns=["entity", "type", "amount", "expected_due_date", "reminder"])
            data.to_csv(f"user_{self.username}_cr_dr.csv")
            print(f"Created a credit, debit file for user {self.username}!")
        else:
            print(data)

        return data

    def add_cr_dr_item(self):
        frames = {}
        for i in list(self.cr_dr.columns)[1:]:
            frames[i] = []

        while True:
            entity = input("Enter entity: ")
            if entity == 'q':
                print("Items added!")
                break
            type_ = input("Is it cr or dr? ")
            amount = float(input("How much: "))
            expected_due_date = input("When is the money due? ")            
            reminder = input("When do you want to reminded? ")

            frames["entity"].append(entity)
            frames["type"].append(type_)
            frames["amount"].append(amount)
            frames["expected_due_date"].append(expected_due_date)
            frames["reminder"].append(reminder)

        df = pandas.DataFrame(frames)
        self.cr_dr = pandas.concat([self.cr_dr, df])
        self.cr_dr.to_csv(f"user_{self.username}_cr_dr.csv")

dat = Cr_Dr("victor17")
dat.add_cr_dr_item()
