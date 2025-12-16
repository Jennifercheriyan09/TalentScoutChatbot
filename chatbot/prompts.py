# chatbot/prompts.py

# ---------------------------------------------------
# BASIC PROMPTS (ENGLISH ONLY)
# ---------------------------------------------------

def greeting_prompt():
    return """
Hello! 
I’m TalentScout, your AI Hiring Assistant.

I’ll be guiding you through a short screening interview to understand your
background and technical skills.

Before we begin, please note:
By continuing, you consent to the use of the information you provide
solely for this interview screening process. Your data will not be shared
or used for any other purpose.

Let’s get started.   
May I know your full name?
"""


def end_prompt():
    return """
Thank you for your time! Your responses have been recorded.
Our team will reach out with next steps.
"""


def fallback_prompt():
    return """
I didn't quite understand that. Could you please rephrase?
"""


# ---------------------------------------------------
# FIELD QUESTIONS (ENGLISH ONLY)
# ---------------------------------------------------

FIELD_QUESTIONS = {
    "name": "May I know your full name?",
    "email": "Please share your email address:",
    "phone": "Could you provide your phone number?",
    "experience": "How many years of total work experience do you have?",
    "position": "What position(s) are you applying for?",
    "location": "Where are you currently located?",
    "tech_stack": "Please list the technologies you are proficient in (languages, frameworks, databases, tools):"
}

def field_question(field):
    return FIELD_QUESTIONS[field]


# ---------------------------------------------------
# TECHNICAL QUESTION PROMPTS (ENGLISH ONLY)
# ---------------------------------------------------

INITIAL_QUESTION_PROMPT = """
You are TalentScout, an adaptive technical interviewer.

The candidate has this tech stack:
\"\"\"{tech_stack}\"\"\" 

Generate the FIRST technical interview question.

Rules:
- Ask a foundational question
- Keep it concise
- Do NOT provide an answer
"""

ADAPTIVE_QUESTION_PROMPT = """
You are TalentScout, an adaptive technical interviewer.

Candidate role:
{role}

Candidate tech stack:
{tech_stack}

Previous questions:
{previous_questions}

Candidate's last answer:
{last_answer}

Difficulty adjustment:
{difficulty}

Communication style:
{communication_style}

Generate the NEXT interview question.

Rules:
- Do NOT repeat previous questions
- Adjust difficulty based on the recommendation
- Adapt question style based on communication style
- Focus on relevance to the candidate's role
- Return ONLY the question text
"""

# ---------------------------------------------------
# BACKWARD COMPATIBILITY
# ---------------------------------------------------

GREETING_PROMPT = greeting_prompt()
END_PROMPT = end_prompt()
FALLBACK_PROMPT = fallback_prompt()
