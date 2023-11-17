from enum import Enum

class ResponseState(Enum):
    SUCCESS = "success"
    ERROR = "error"

class Response:
    def __init__(self, state, error_message=None, data=None):
        self.state = state
        self.error_message = error_message
        self.data = data

