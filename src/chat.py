from src.gemini_api import GeminiAPI
from src.prompts import chat_with_persona
from src.persona import Persona


class ChatSession:

    def __init__(self, persona_name):
        self.gemini_api = GeminiAPI()
        self.persona_creator = Persona()
        self.persona = self.persona_creator.create_persona(persona_name)
        self.history = {}

    def add_message(self, message):
        if "messages" not in self.history:
            self.history["messages"] = []
        self.history["messages"].append(message)

    def add_user_message(self, message):
        self.add_message({"role": "user", "content": message})

    def add_assistant_message(self, message, person_name):
        self.add_message({"role": person_name, "content": message})

    def converse(self, user_message):
        self.add_user_message(user_message)
        input_prompt = chat_with_persona.format(
            person_name=self.persona["name"],
            persona=self.persona["persona"],
            conversation=str(self.history),
        )
        response = self.gemini_api.generate(input_prompt)
        self.add_assistant_message(response, "assistant")
        return response
