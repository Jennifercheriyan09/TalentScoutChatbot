from gtts import gTTS
import os
import uuid

def text_to_speech(text: str, lang: str = "en"):
    """
    Converts text to speech and returns audio file path
    """
    filename = f"tts_{uuid.uuid4().hex}.mp3"

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    return filename
