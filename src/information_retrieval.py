from src.wiki_scraper import WikiScraper
from src.get_statements import PersonalityStatementFinder
from src.gemini_api import GeminiAPI
from src.prompts import info_merge_prompt

class InformationRetrieval:

    def __init__(self):
        self.wikiscraper = WikiScraper()
        self.statement_finder = PersonalityStatementFinder()
        self.gemini_api = GeminiAPI()

    
    def merge_information(self, wiki_data, statement_data):
        prompt = info_merge_prompt.format(
            wikipedia_information=wiki_data,
            other_information=statement_data
        )
        model_output = self.gemini_api.generate(prompt)
        return model_output.strip()


    def retrieve_information(self, query):
        page_data = self.wikiscraper.get_wiki_content(query)
        relevant_statements = self.statement_finder.get_personality_statements(query)
        relevant_information = self.merge_information(page_data, relevant_statements)
        return {"relevant_information": relevant_information}