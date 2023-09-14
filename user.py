from database import Database


class User:
    TABLE_NAME = "users"
    TEMPLATE = ["username"]

    def __init__(self, db: Database) -> None:
        self.db = db
        self.data = None

    def create_user(self):
        result = None
        is_user = self.read_user()

        if not is_user:
            self.db.create(self.TABLE_NAME, self.data)
            result = f"User {self.user_data} has been created."
        else:
            result = f"User {self.user_data} already exists."

        return result

    def read_user(self):
        return self.db.read(self.TABLE_NAME, self.data)

    def update_user(self):
        ...

    def delete_user(self):
        ...

    def login(self):
        username = input("Enter username: ")
        if username[0].isalpha():
            ...
        else:
            ...

    def signup(self):
        ...

    def close(self):
        ...

    def modify(self):
        ...


if __name__ == "__main__":
    usr = User(username="victorian177")
    print("Result: ", usr.create_user())
