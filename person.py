import os


class Profile:
    def __init__(self, name) -> None:
        self.name = name
        self.database_directory = self.get_database_directory()

    def get_database_directory(self):
        database_directory = os.path.join(os.getcwd(), "Personal Finance", self.name)

        if not os.path.exists(database_directory):
            os.makedirs(database_directory)

        return database_directory
