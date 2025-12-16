# utils/helpers.py

import hashlib

EXIT_KEYWORDS = ["exit", "bye", "quit", "stop", "thank you", "bye bye"]

def contains_exit_keyword(message: str) -> bool:
    message = message.lower()
    return any(keyword in message for keyword in EXIT_KEYWORDS)

def clean_text(text: str) -> str:
    return text.strip()

def anonymize_value(value: str) -> str:
    """
    Hashes any sensitive value using SHA256 for anonymization.
    """
    return hashlib.sha256(value.strip().encode()).hexdigest()
