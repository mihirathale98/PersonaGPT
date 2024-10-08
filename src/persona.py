from src.information_retrieval import InformationRetrieval
from src.prompts import persona_creation_from_wiki
from src.gemini_api import GeminiAPI
from src.utils import parse_model_output


class Persona:
    def __init__(self):
        self.gemini_api = GeminiAPI()
        self.information_retrieval = InformationRetrieval()
    

    def create_persona_from_wiki(self, persona_name):
        ## with max retries 3
        persona = None
        persona_information =  self.information_retrieval.retrieve_information(persona_name)
        wiki_info = persona_information['relevant_information']
        wiki_persona = persona_creation_from_wiki.format(person_name=persona_name, relevant_information=wiki_info)
        for i in range(3):
            try:
                model_output = self.gemini_api.generate(wiki_persona)
                persona = parse_model_output(model_output)
            except:
                pass
            if persona:
                break
        return persona


    def create_persona(self, persona_name):
        persona = {'persona': self.create_persona_from_wiki(persona_name), 'name': persona_name}
        return persona