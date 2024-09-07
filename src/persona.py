from information_retrieval import InformationRetrieval
from prompts import persona_creation_from_wiki
from gemini_api import GeminiAPI
from utils import parse_model_output


class Persona:
    def __init__(self):
        self.gemini_api = GeminiAPI()
        self.information_retrieval = InformationRetrieval()
    
    def create_persona(self, persona_name):
        persona_information =  self.information_retrieval.retrieve_information(persona_name)
        wiki_info = persona_information['wikipedia_information']
        wiki_persona = persona_creation_from_wiki.format(person_name=persona_name, wikipedia_information=wiki_info)
        model_output = self.gemini_api.generate(wiki_persona)
        print(model_output)
        persona = parse_model_output(model_output)
        return persona



persona_creator = Persona()

persona_ = persona_creator.create_persona("Elon Musk")
print(persona_)