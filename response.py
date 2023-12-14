class Response:
    def __init__(self):
        self.is_error = False
        self.message = ""
        self.data = None

    def display(self):
        print(f"{self.message}\n\n")
