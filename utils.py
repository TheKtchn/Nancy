import re
from datetime import date, datetime, timedelta


def validate_name(name):
    return bool(re.match("^[a-zA-Z -]+$", name))


def validate_amount(amount):
    try:
        abs(float(amount))
    except ValueError:
        return False

    return True


def validate_date_not_less(date_string):
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
            f"Date must be between {lower_bound.strftime('%d-%m-%Y')} and today.",
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
            f"Date must be between today and {upper_bound.strftime('%d-%m-%Y')}.",
        )
