# chatbot/state_manager.py

class ConversationState:
    def __init__(self):
        self.stage = "language_select"
        self.data = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": None,
        }
        self.language = "en"  

        self.current_question = None
        self.questions_asked = []
        self.answers = []
        self.evaluations = []  
        
        self.question_index = 0
        self.total_questions = 4  

    def get_next_missing_field(self):
        for key, value in self.data.items():
            if value is None:
                return key
        return None

    def update_field(self, field, value):
        self.data[field] = value
