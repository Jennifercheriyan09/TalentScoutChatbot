from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from chatbot.state_manager import ConversationState
from chatbot.controller import handle_user_input
import os
from pydub import AudioSegment
from utils.speech_to_text import speech_to_text
from utils.text_to_speech import text_to_speech


st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
# This snippet forces the browser to scroll to the bottom of the page
st.markdown(
    """
    <script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = body.scrollHeight;
    </script>
    """,
    unsafe_allow_html=True
)
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

if "input_mode" not in st.session_state:
    st.session_state.input_mode = "text"

state = st.session_state.state

# ------------------------------------------
# STAGE 0 — LANGUAGE SELECTION SCREEN
# ------------------------------------------
if state.stage == "language_select":

    st.header("Choose your interview language")

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
# AUDIO & SUBMISSION LOGIC
# ------------------------------------------

# 1. Handle Auto-Greeting Speak (Fix for the missing greeting)
if st.session_state.tts_audio:
    st.audio(st.session_state.tts_audio, autoplay=True)
    # Clear it after rendering so it doesn't loop on every rerun
    st.session_state.tts_audio = None

# 2. Setup Input Interface
final_input = None

if stage == "interview":
    st.write("---")
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        # We use a unique key for the chat input to handle the text side
        user_text = st.chat_input("Type your answer here...", key="text_input_field")
        if user_text:
            final_input = user_text
            
    with col2:
        # The mic icon button to trigger the audio input widget
        if st.button("🎤" if st.session_state.input_mode == "text" else "⌨️"):
            st.session_state.input_mode = "voice" if st.session_state.input_mode == "text" else "text"
            st.rerun()

    # If user toggled to voice mode, show the recorder
    if st.session_state.input_mode == "voice":
        audio_data = st.audio_input("Recording...", label_visibility="collapsed", key=f"mic_{st.session_state.audio_key}")
        if audio_data:
            with st.spinner("Transcribing..."):
                # Save and transcribe
                temp_path = "temp_voice.wav"
                with open(temp_path, "wb") as f:
                    f.write(audio_data.getvalue())
                
                final_input = speech_to_text(temp_path, lang=state.language)
                os.remove(temp_path)
                
                # Switch back to text mode for the next turn automatically
                st.session_state.input_mode = "text"
else:
    # Non-interview stages (like greeting/setup)
    user_text = st.chat_input("Type here...")
    if user_text:
        final_input = user_text

# 3. Main Processing Logic
if final_input:
    # Adding user message to history
    st.session_state.chat_history.append(("user", final_input))
    
    # Get Bot Response
    bot_response = handle_user_input(final_input, state)
    st.session_state.chat_history.append(("assistant", bot_response))
    
    # Generate Audio for the NEW response
    # This automatically "replaces" any pending audio in the session state
    st.session_state.tts_audio = text_to_speech(bot_response, lang=state.language)
    
    # Prepare for next turn
    st.session_state.audio_key += 1
    st.rerun()