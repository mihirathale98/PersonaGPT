from src.brave_search import brave_search
from src.scraper import scrape_data
from src.gemini_api import GeminiAPI

gemini_model = GeminiAPI('gemini-1.5-flash')


def create_query(persona, query):
    prompt = "Write a query to search for {query} based on {persona}. Output:"
    response = gemini_model.generate(prompt.format(query=query, persona=persona))
    query = response.strip().split('\n')
    return query

def search_for_query(persona, query):
    query = create_query(persona, query)
    response = brave_search(query, count=3)
    if response is None:
        return None
    urls = [article['url'] for article in response if 'url' in article]
    if len(urls) == 0:
        return None
    
    data = ''
    for url in urls:
        search_results = scrape_data(url)
        if search_results is not None:
            data += search_results[url]
    return data


def summarize_data(persona, query):
    data = search_for_query(persona, query)
    prompt = 'Extract all the key information from the following text based on the query {query} and summarize it in 1000 words:\n\n {data} \n\nOutput:'
    prompt = prompt.format(query=query, data=data)
    response = gemini_model.generate(prompt)
    return response
