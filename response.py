class Response:
    def __init__(self):
        self.is_error = False
        self.message = ""

    def display(self):
        print(f"\n{self.message}\n\n")
