import re

def validate_email(email: str) -> bool:
    """
    Validates an email address using regex.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validates a phone number (basic check: only digits + 10–15 length).
    """
    phone = phone.replace(" ", "")
    return phone.isdigit() and 10 <= len(phone) <= 15

def validate_experience(experience: str) -> bool:
    """
    Validates that experience input is a number (integer or float).
    """
    try:
        float(experience)
        return True
    except ValueError:
        return False
