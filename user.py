import bcrypt
import re

import response
from database import db, ping

class UserDatabaseManager:
    PRIMARY_KEY = "email"
    def __init__(self) -> None:
        self.users = db["users"]
    
    def create_user(self, user_data):
        result = self.users.insert_one(user_data)
        return result
        
    def retrieve_user(self, key):
        query = {self.PRIMARY_KEY: key}
        user = self.users.find_one(query)
        
        return user
    
    def update_user(self, key, data):
        query = {self.PRIMARY_KEY: key}
        result = self.users.update_one(query, {"$set": data})
        
        return result
    
    def delete_user(self, key):
        query = {self.PRIMARY_KEY: key}
        result = self.users.delete_one(query)
        
        return result        
    
class UserData:
    def __init__(self, id, name, email, password) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
class UserCreateForm:
    def __init__(self, user_create_form: dict) -> None:
        pass
    
    def validate_name(name):
        return bool(re.match("^[a-zA-Z]+$", name))

    def validate_email(email):
        # A simple email validation using regular expression
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.match(email_pattern, email))

    def validate_password(password):
        # Password should contain at least one letter and one number, with a minimum length of 5 characters
        return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$", password))

    def check_email_existence(email):
        # Check if the email already exists in the mock database
        existing_emails = [user["email"] for user in mock_database["users"]]
        return email in existing_emails

    def create_user():
        # Validate user input
        if not validate_name(name):
            return "Invalid name. Name should only contain alphabets."

        if not validate_email(email):
            return "Invalid email address."

        if not validate_password(password):
            return "Invalid password. Password should contain at least one letter and one number, with a minimum length of 5 characters."

        # Check if the email already exists
        if check_email_existence(email):
            return "Email already exists. Please choose a different email."

        # Hash the password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    


        
    
