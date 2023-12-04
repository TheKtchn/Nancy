import hashlib
import re


def validate_name(name):
    """
    Validates a name using a regular expression.

    The name should only contain letters, spaces, and hyphens.

    Args:
        name (str): The name to be validated.

    Returns:
        bool: True if the name is valid, False otherwise.
    """
    return bool(re.match("^[a-zA-Z -]+$", name))


def validate_email(email):
    """
    Validates an email address using a simple regular expression.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # A simple email validation using regular expression
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))


def validate_password(password):
    """
    Validates a password according to certain criteria.

    The password should contain at least one letter and one number,
    with a minimum length of 5 characters.

    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    # Password should contain at least one letter and one number, with a minimum length of 5 characters
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$", password))


def hash_password(password):
    """
    Hashes a password using SHA-256.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    hashed_password = sha256_hash.hexdigest()

    return hashed_password
