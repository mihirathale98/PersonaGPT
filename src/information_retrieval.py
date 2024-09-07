from wiki_scraper import WikiScraper

class InformationRetrieval:

    def __init__(self):
        self.wikiscraper = WikiScraper()

    def retrieve_information(self, query):
        retrieved_information = {}
        page_data = self.wikiscraper.get_wiki_content(query)
        if page_data:
            retrieved_information['wikipedia_information'] = page_data
        return retrieved_information