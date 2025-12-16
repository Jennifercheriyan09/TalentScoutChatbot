from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from chatbot.state_manager import ConversationState
from chatbot.controller import handle_user_input
import os

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

st.title("🤖 TalentScout – AI Hiring Assistant")
st.markdown(
    """
    <style>
    audio {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = None

# ------------------------------------------
# INITIAL SESSION STATE
# ------------------------------------------
if "state" not in st.session_state:
    st.session_state.state = ConversationState()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

state = st.session_state.state

# ------------------------------------------
# STAGE 0 — LANGUAGE SELECTION SCREEN
# ------------------------------------------
if state.stage == "language_select":

    st.header("🌍 Choose your interview language")

    LANGS = {
        "English": "en",
        "Hindi": "hi",
        "Malayalam": "ml",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn"
    }

    choice = st.selectbox("Select a language to begin:", list(LANGS.keys()))

    if st.button("Start Interview"):
        state.language = LANGS[choice]
        state.stage = "greeting"
        st.rerun()

    st.stop()   # 🚨 Do NOT render chat yet


# ------------------------------------------
# AUTO GREETING (ONLY AFTER LANGUAGE IS SET)
# ------------------------------------------
if len(st.session_state.chat_history) == 0:
    greeting_msg = handle_user_input("INIT", state)
    st.session_state.chat_history.append(("assistant", greeting_msg))

    # 🔊 Speak greeting
    from utils.text_to_speech import text_to_speech
    st.session_state.tts_audio = text_to_speech(greeting_msg, lang=state.language)



# ------------------------------------------
# DETECT STAGE
# ------------------------------------------
stage = state.stage
final_input = None


# ------------------------------------------
# FULL SCREEN "INTERVIEW COMPLETE"
# ------------------------------------------
if stage == "done":

    st.markdown(
        """
        <style>
        .full-screen-center {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 90vh;
            text-align: center;
        }
        .done-box {
            background-color: #0f5132;
            padding: 40px;
            border-radius: 12px;
            color: white;
            font-size: 22px;
            width: 80%;
            max-width: 600px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="full-screen-center">
            <div class="done-box">
                🎉 <b>Your interview is complete!</b><br><br>
                Thank you for your time.<br>
                Our team will review your responses and reach out with next steps.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ------------------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------------------
for sender, text in st.session_state.chat_history:
    st.chat_message(sender).write(text)

# ------------------------------------------
# PLAY BOT AUDIO RESPONSE (SAFE)
# ------------------------------------------
if st.session_state.tts_audio:
    st.audio(st.session_state.tts_audio, autoplay=True)
    st.session_state.tts_audio = None



# ------------------------------------------
# INPUT SECTION
# ------------------------------------------
if stage == "interview":

    st.markdown("### 🎤 Speak your answer:")

    audio_key = f"audio_{st.session_state.audio_key}"
    user_audio = st.audio_input("", key=audio_key, label_visibility="collapsed")

    if user_audio:
        os.makedirs("audio", exist_ok=True)
        audio_path = "audio/temp_answer.wav"
        with open(audio_path, "wb") as f:
            f.write(user_audio.getvalue())

        from utils.speech_to_text import speech_to_text
        final_input = speech_to_text(audio_path, lang=state.language)

        os.remove(audio_path)

else:
    # Greeting + Info collection → text only
    final_input = st.chat_input("Type your response...")


# ------------------------------------------
# PROCESS INPUT
# ------------------------------------------
if final_input:

    st.session_state.chat_history.append(("user", final_input))

    bot_response = handle_user_input(final_input, state)
    st.session_state.chat_history.append(("assistant", bot_response))
    from utils.text_to_speech import text_to_speech
    st.session_state.tts_audio = text_to_speech(bot_response, lang=state.language)

    if stage == "interview":
        st.session_state.audio_key += 1

    st.rerun()
