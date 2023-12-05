import hashlib
import re
from datetime import date, datetime, timedelta


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


def validate_amount(amount):
    """
    Validates if the input is a valid numeric amount.

    Args:
        amount (str): The amount to be validated.

    Returns:
        bool: True if the amount is a valid numeric value, False otherwise.
    """
    try:
        abs(float(amount))
    except ValueError:
        return False

    return True


def validate_date_not_less(date_string):
    """
    Validates if the input is a valid date string in the format 'dd-mm-yyyy' within a specific range.

    Args:
        date_string (str): The date string to be validated.

    Returns:
        tuple: A tuple containing a boolean indicating whether the date is valid, and a message.
            - If the date is valid, the boolean is True, and the message is "Valid date."
            - If the date is invalid, the boolean is False, and the message contains details on the error.
    """
    pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    if not pattern.match(date_string):
        return False, "Invalid date format. Please use dd-mm-yyyy.\n"
    try:
        parsed_date = datetime.strptime(date_string, "%d-%m-%Y").date()
    except ValueError:
        return False, "Invalid date. Please enter a valid date.\n"

    today = date.today()
    lower_bound = today - timedelta(days=3 * 30)

    if lower_bound <= parsed_date <= today:
        return True, "Valid date."
    else:
        return (
            False,
            f"Date must be between {lower_bound.strftime('%d-%m-%Y')} and today.\n",
        )


def validate_date_not_greater(date_string):
    pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    if not pattern.match(date_string):
        return False, "Invalid date format. Please use dd-mm-yyyy.\n"
    try:
        parsed_date = datetime.strptime(date_string, "%d-%m-%Y").date()
    except ValueError:
        return False, "Invalid date. Please enter a valid date.\n"

    today = date.today()
    upper_bound = today + timedelta(days=3 * 30)

    if today <= parsed_date <= upper_bound:
        return True, "Valid date."
    else:
        return (
            False,
            f"Date must be between today and {upper_bound.strftime('%d-%m-%Y')}.\n",
        )


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
