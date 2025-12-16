from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate(text, target_lang):
    """
    Translates 'text' into target_lang using Llama 3.
    target_lang must be ISO code: en, hi, ml, ta, te, kn
    """
    if target_lang == "en":
        return text  # no need to translate

    prompt = f"""
Translate the following text into {target_lang}.
Preserve meaning, tone, and clarity.

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
