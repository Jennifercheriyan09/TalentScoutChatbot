# chatbot/controller.py
import json
# ADD THESE IMPORTS AT TOP
from chatbot.answer_evaluator import evaluate_answer
from chatbot.state_manager import ConversationState
from chatbot.prompts import (
    greeting_prompt,
    end_prompt,
    fallback_prompt,
    field_question
)
from chatbot.validators import validate_email, validate_phone, validate_experience
from chatbot.question_generator import (
    generate_first_question,
    generate_adaptive_question
)
from chatbot.fallback import is_fallback_trigger
from utils.helpers import contains_exit_keyword
from utils.translator import translate


def handle_user_input(message: str, state: ConversationState):

    lang = state.language  # selected language (ISO code)

    # -------------------------------------------------
    # EXIT CHECK
    # -------------------------------------------------
    if contains_exit_keyword(message):
        state.stage = "done"
        return translate(end_prompt(), lang)

    # -------------------------------------------------
    # GREETING
    # -------------------------------------------------
    if state.stage == "greeting":
        state.stage = "info_collection"
        reply_en = greeting_prompt()
        return translate(reply_en, lang)

    # -------------------------------------------------
    # FALLBACK TRIGGER (nonsense / unclear input)
    # -------------------------------------------------
    if is_fallback_trigger(message):
        return translate(fallback_prompt(), lang)

    # -------------------------------------------------
    # INFO COLLECTION STAGE
    # -------------------------------------------------
    if state.stage == "info_collection":

        current_field = state.get_next_missing_field()

        # -------- Validation --------
        if current_field == "email" and not validate_email(message):
            return translate("Invalid email format. Please try again.", lang)

        if current_field == "phone" and not validate_phone(message):
            return translate("Invalid phone number. Please try again.", lang)

        if current_field == "experience" and not validate_experience(message):
            return translate("Experience must be a number. Please enter again.", lang)

        # -------- Save field --------
        state.update_field(current_field, message)

        next_field = state.get_next_missing_field()
        if next_field:
            question_en = field_question(next_field)
            return translate(question_en, lang)

        # -------------------------------------------------
        # ALL INFO COLLECTED → START INTERVIEW
        # -------------------------------------------------
        state.stage = "interview"

        first_q = generate_first_question(
            tech_stack=state.data["tech_stack"],
            lang=lang
        )

        state.current_question = first_q
        state.questions_asked.append(first_q)
        state.question_index = 1

        intro_en = f"Great! Let's begin the interview.\n\nQuestion 1:\n{first_q}"
        return translate(intro_en, lang)

    # -------------------------------------------------
    # INTERVIEW STAGE
    # -------------------------------------------------
    if state.stage == "interview":

        # Store answer
        state.answers.append(message)

        # 🔥 NEW: evaluate answer
        evaluation = evaluate_answer(
            question=state.current_question,
            answer=message,
            role=state.data["position"]
        )

        evaluation = json.loads(evaluation)

        state.evaluations.append(evaluation)

        # Ask next question if available
        if state.question_index < state.total_questions:

            next_q = generate_adaptive_question(
                tech_stack=state.data["tech_stack"],
                previous_questions=state.questions_asked,
                last_answer=message,
                role=state.data["position"],
                difficulty=evaluation["difficulty_recommendation"],
                communication_style=evaluation["communication_style"],
                lang=state.language
            )

            state.current_question = next_q
            state.questions_asked.append(next_q)
            state.question_index += 1

            return translate(
                f"Question {state.question_index}:\n{next_q}",
                state.language
            )

        # Interview complete
        from utils.storage import save_candidate
        save_candidate(
            candidate_data=state.data,
            questions=state.questions_asked,
            answers=state.answers,
            evaluations=state.evaluations
        )

        state.stage = "done"
        return translate(end_prompt(), state.language)

    # -------------------------------------------------
    # DONE STAGE
    # -------------------------------------------------
    if state.stage == "done":
        return translate("The interview has already been completed.", lang)

    # -------------------------------------------------
    # DEFAULT FALLBACK
    # -------------------------------------------------
    return translate(fallback_prompt(), lang)
