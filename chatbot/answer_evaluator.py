import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluate_answer(question, answer, role):
    """
    Evaluates candidate answer and returns structured signals.
    """

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Role: {role}

Question:
{question}

Answer:
{answer}

Return ONLY valid JSON with the following fields:
- answer_quality: integer from 1 to 5
- difficulty_recommendation: one of [increase, maintain, decrease]
- communication_style: one of [concise, verbose, unclear]
- brief_feedback: one short sentence
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You evaluate technical interview answers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
