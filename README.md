# Project Overview
TalentScout is an AI-powered Hiring Assistant chatbot designed to automate the initial candidate screening process.
It simulates a real technical interview by collecting candidate details, generating personalized technical questions, and adapting the interview flow dynamically based on candidate responses.

The chatbot supports multilingual interaction, voice-based responses, and adaptive personalization, making the interview experience natural, inclusive, and efficient for both candidates and recruiters.

# Key Capabilities

1. Multilingual interview flow (Text + Voice)
2. Dynamic information gathering
3. Tech-stack–based technical question generation
4. Adaptive difficulty based on answer quality
5. Role-based and communication-style personalization
6. Voice input (Speech-to-Text) and Voice output (Text-to-Speech)
7. Full interview completion summary (backend)

# Installation Instructions

1. Prerequisites
Ensure the following are installed:
Python 3.9+
pip
A valid GROQ API key

2. Clone the Repository
git clone <your-repo-url>
cd TalentScoutChatbot

3. Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

4. Install Dependencies
pip install -r requirements.txt

5. Environment Variables
Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here

6. Run the Application
streamlit run app.py

The application will open automatically in your browser.

# Usage Guide
Step-by-Step Flow:

1. Language Selection
Candidate selects their preferred interview language.

2. Consent & Greeting
The chatbot greets the candidate and clearly explains data usage and consent.

3. Information Collection
The chatbot collects:
Full Name
Email
Phone Number
Years of Experience
Desired Position
Current Location
Tech Stack

4. Technical Interview
The chatbot generates 4 personalized technical questions.
Candidates can respond using voice input.
The chatbot adapts:
Question difficulty
Question focus
Follow-up depth

5. Interview Completion
A full-screen confirmation message is shown.
Candidate inputs are disabled after completion.

# Technical Details
Frontend  -	Streamlit
LLM - LLaMA 3.3 (via Groq API)
Speech-to-Text	- Whisper (via custom wrapper)
Text-to-Speech  -	Multilingual TTS utility
Environment	- Python, dotenv
State Management - Custom ConversationState

# Architectural Decisions

State-driven conversation flow to ensure context continuity.
LLM-based evaluation instead of rule-based scoring for realism.
Hidden internal evaluation to avoid biasing the candidate.
Modular design for easy extension (dashboard, analytics, ATS integration).

# Prompt Design

1. Information Gathering Prompts:
Structured and sequential prompts ensure clarity and validation.
Each question is asked only when the previous response is successfully captured.

2. Technical Question Generation
Prompts include:
Candidate tech stack
Previously asked questions
Candidate’s last response
Role applied for
Difficulty adjustment signal
Communication style signal

This ensures:
No repeated questions
Context-aware progression
Adaptive difficulty

3. Answer Evaluation Prompts

Each answer is evaluated internally for:
Technical correctness
Depth of understanding
Communication clarity

The output is structured JSON used only by the system.

# Challenges & Solutions
🔹 Challenge 1: Maintaining Context Across Reruns
Solution: Implemented a custom ConversationState stored in st.session_state.

🔹 Challenge 2: Avoiding Repeated Audio Inputs
Solution: Used dynamic keys (audio_key) for Streamlit audio widgets.

🔹 Challenge 3: Multilingual Support Without Hardcoding
Solution: Leveraged translation utilities and language-aware prompts instead of duplicating text.

🔹 Challenge 4: Adaptive Question Logic
Solution: Introduced an intermediate answer evaluation layer using LLMs to derive personalization signals.

# Conclusion

TalentScout demonstrates how modern LLMs, speech technologies, and thoughtful UX design can be combined to build a realistic, scalable AI hiring assistant.
The system goes beyond static Q&A by offering adaptive, personalized, and multilingual interviews, closely mimicking real-world recruiter behavior.