import hashlib
import re


def validate_name(name):
    return bool(re.match("^[a-zA-Z -]+$", name))


def validate_email(email):
    # A simple email validation using regular expression
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))


def validate_password(password):
    # Password should contain at least one letter and one number, with a minimum length of 5 characters
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$", password))


def hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    hashed_password = sha256_hash.hexdigest()

    return hashed_password
