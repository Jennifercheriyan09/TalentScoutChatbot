# chatbot/question_generator.py

import os
from dotenv import load_dotenv
from groq import Groq
from chatbot.prompts import INITIAL_QUESTION_PROMPT, ADAPTIVE_QUESTION_PROMPT
from utils.translator import translate

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content

def generate_first_question(tech_stack: str, lang="en"):
    prompt = INITIAL_QUESTION_PROMPT.format(tech_stack=tech_stack)
    question_en = _ask_groq(prompt)
    return translate(question_en, lang)

def generate_adaptive_question(
    tech_stack,
    previous_questions,
    last_answer,
    role,
    difficulty,
    communication_style,
    lang="en"
):
    prompt = ADAPTIVE_QUESTION_PROMPT.format(
        tech_stack=tech_stack,
        previous_questions="\n".join(previous_questions),
        last_answer=last_answer,
        role=role,
        difficulty=difficulty,
        communication_style=communication_style
    )

    question_en = _ask_groq(prompt)
    return translate(question_en, lang)
