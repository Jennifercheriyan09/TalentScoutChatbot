# chatbot/controller.py
import json
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
    # FALLBACK TRIGGER 
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
    # -------------------------------------------------
    # INTERVIEW STAGE (REPLACED VERSION)
    # -------------------------------------------------
    if state.stage == "interview":
        # 1. Store original message (as typed by user) in history
        state.answers.append(message)

        # 2. INTERNAL TRANSLATION: Convert user response to English for processing
        # This ensures the LLM 'brain' always works with English data
        message_en = translate(message, "en") 

        # 3. QUICK CHECK: Did they say "I don't know"? 
        # (Checking the English version is much more reliable)
        idk_keywords = ["don't know", "no idea", "not sure", "skip"]
        is_idk = any(k in message_en.lower() for k in idk_keywords)

        if is_idk:
            # Force the evaluation to be neutral/easy to avoid AI "teaching" the candidate
            evaluation = {
                "difficulty_recommendation": "easier", 
                "communication_style": "brief"
            }
        else:
            # 4. EVALUATE: Send English text to your LLM evaluator
            eval_raw = evaluate_answer(
                question=state.current_question, # Current question is already in English
                answer=message_en,               # English translation of user answer
                role=state.data["position"]
            )
            try:
                evaluation = json.loads(eval_raw)
            except:
                # Fallback if LLM output isn't clean JSON
                evaluation = {"difficulty_recommendation": "neutral", "communication_style": "neutral"}

        if not is_idk:
            state.evaluations.append(evaluation)
        else:
            state.evaluations.append({"skipped": True})


        # 5. GENERATE NEXT QUESTION
        # 5. GENERATE NEXT QUESTION
        if state.question_index < state.total_questions:
            
            # --- FIX STARTS HERE ---
            # If the user didn't know, don't send the literal "I don't know" to the AI.
            # Send a instruction instead so the AI knows to move on without explaining.
            context_answer = (
                    "[SKIP_ANSWER]"
                    if is_idk
                    else message_en)

            # --- FIX ENDS HERE ---

            next_q_en = generate_adaptive_question(
                tech_stack=state.data["tech_stack"],
                previous_questions=state.questions_asked,
                last_answer=context_answer, # Pass the cleaned context here
                role=state.data["position"],
                difficulty=evaluation.get("difficulty_recommendation", "neutral"),
                communication_style=evaluation.get("communication_style", "neutral"),
                lang="en" 
            )

            state.current_question = next_q_en
            state.questions_asked.append(next_q_en)
            state.question_index += 1

            # 6. EXTERNAL TRANSLATION: Translate the English question to the user's language
            translated_prefix = translate(f"Question {state.question_index}:", state.language)
            translated_question = translate(next_q_en, state.language)
            
            return f"{translated_prefix}\n{translated_question}"

        # --- Save and Finish (same as your original) ---
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
