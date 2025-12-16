# chatbot/fallback.py

import re
from chatbot.prompts import FALLBACK_PROMPT
from chatbot.llm_client import ask_llm

UNEXPECTED_PATTERNS = [
    r"^(hi|hello|hey)$",           # casual greetings after start
    r"^[\W_]+$",                   # only symbols or emojis
    r"^\s*$",                      # empty input
]

def is_fallback_trigger(user_input: str) -> bool:
    """
    Detects inputs that the bot should NOT attempt to interpret as field values.
    """
    cleaned = user_input.strip().lower()

    # If it's empty → fallback
    if cleaned == "":
        return True

    # Emoji/symbol/meaningless patterns
    for pattern in UNEXPECTED_PATTERNS:
        if re.match(pattern, cleaned):
            return True

    return False


def get_fallback_response():
    """
    Returns a polite clarifying response from the LLM.
    """
    return ask_llm(FALLBACK_PROMPT)
