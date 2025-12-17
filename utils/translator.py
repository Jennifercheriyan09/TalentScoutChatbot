from groq import Groq

client = Groq()

def translate(text, target_lang):
    """
    STRICT Translation using Llama 3.
    """
    if not text or target_lang == "en":
        return text 

    # ISO Code to Language Name Mapping
    lang_map = {
        "hi": "Hindi", "ml": "Malayalam", "ta": "Tamil", 
        "te": "Telugu", "kn": "Kannada"
    }
    target_name = lang_map.get(target_lang, "English")

    # The System Prompt is key here to stop hallucinations
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": f"You are a translator. Translate the text to {target_name}. "
                           f"Rules: 1. Return ONLY the translated text. "
                           f"2. Do NOT add explanations (e.g., 'This is already in Hindi'). "
                           f"3. Do NOT answer the question. "
                           f"4. If the text is already in {target_name}, return it exactly as is."
            },
            {"role": "user", "content": text}
        ],
        temperature=0.0 # Low temperature ensures consistency and speed
    )

    return response.choices[0].message.content.strip()