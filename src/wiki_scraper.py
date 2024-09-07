import wikipediaapi


class WikiScraper:
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia("PersonaGPT", "en")

    def search_wiki(self, query):
        page = self.wiki_wiki.page(query)
        if not page.exists():
            return None
        return page

    def get_page_data(self, query):

        page_data = {}
        page = self.search_wiki(query)
        if page:
            page_data["title"] = page.title
            page_data["sections_text"] = "\n".join(
                [section.title + "\n" + section.text for section in page.sections]
            )
        return page_data

    def get_wiki_content(self, query):
        page_data = self.get_page_data(query)
        content = ""
        for key, value in page_data.items():
            content += f"{key}: {value}\n"
        return content
