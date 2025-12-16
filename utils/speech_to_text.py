# utils/speech_to_text.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def speech_to_text(audio_path: str, lang="en"):
    """
    Transcribes audio using Groq Whisper in the user's preferred language.
    """
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            language=lang,               # 💥 Force transcription in selected language
            response_format="text"
        )
    return result
