from gtts import gTTS
import os
import uuid

def text_to_speech(text: str, lang: str = "en"):
    """
    Converts text to speech and returns audio file path
    """
    os.makedirs("audio", exist_ok=True)
    filename = f"audio/tts_{uuid.uuid4().hex}.mp3"

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    return filename
