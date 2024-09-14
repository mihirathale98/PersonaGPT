import requests
from src.gemini_api import GeminiAPI
import os
from src.brave_search import brave_search
from src.scraper import scrape_data
import time
from src.prompts import statement_extractor, statement_extractor_summ


class PersonalityStatementFinder:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = GeminiAPI(model_name)
    
    def generate_search_queries(self, personality):
        # Modify the prompt to generate search queries specifically for press or news statements
        prompt = f"Generate 3 search queries to find press statements or interviews given by {personality}. Each query should focus on statements made in news articles or public press releases."
        response = self.model.generate(prompt)
        queries = response.strip().split('\n')
        return queries
    
    def web_search(self, query):
        response = brave_search(query)
        if response is None:
            return None
        urls = [article['url'] for article in response if 'url' in article]
        return urls[0]
    
    def extract_statements(self,personality, search_results):
        # Modify the prompt to extract press statements or news-related content
        prompt = statement_extractor.format(
            personality=personality,
            news_articles=search_results
        )
        
        response = self.model.generate(prompt)
        return response.strip()
    
    def get_personality_statements(self, personality):
        queries = self.generate_search_queries(personality)
        all_statements = []

        for query in queries:
            url = self.web_search(query)
            time.sleep(1)
            if url is not None:          
                search_results = scrape_data(url)
                if search_results is None:
                    continue
                search_results = search_results[url]
                statements = self.extract_statements(personality, search_results)
                all_statements.append(statements)

        summary = self.summarize_info(all_statements)
        return summary
    
    def summarize_info(self, all_statements):
        all_statements = '\n'.join(all_statements)
        prompt = statement_extractor_summ.format(
            information=all_statements
        )
        response = self.model.generate(prompt)
        return response
