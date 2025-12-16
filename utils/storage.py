# utils/storage.py

import json
import os
from utils.helpers import anonymize_value

DATA_PATH = "data/candidates.json"


def load_candidates():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_candidate(candidate_data: dict, questions: list, answers: list, evaluations: list = None):
    """
    Saves anonymized candidate info + technical Q&A into the JSON file.
    """
    if evaluations is None:
        evaluations = []

    anonymized = {
        "name_hash": anonymize_value(candidate_data.get("name", "")),
        "email_hash": anonymize_value(candidate_data.get("email", "")),
        "phone_hash": anonymize_value(candidate_data.get("phone", "")),
        "experience": candidate_data.get("experience"),
        "position": candidate_data.get("position"),
        "location": candidate_data.get("location"),
        "tech_stack": candidate_data.get("tech_stack"),
        "technical_questions": questions,
        "technical_answers": answers,
        "evaluations": evaluations
    }

    candidates = load_candidates()
    candidates.append(anonymized)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(candidates, f, indent=4)
