import requests
import os


def parse_brave_search_results(search_results):
    if search_results is None:
        return None
    results = search_results.get("web", {}).get("results", [])
    if len(results) == 0:
        return None
    return results

def brave_search(query, count=10):
    base_url = "https://api.search.brave.com/res/v1/web/search"
    
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": os.getenv('BRAVE_API_KEY')
    }
    
    params = {
        "q": query,
        "count": count,
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return parse_brave_search_results(response.json()) if response.status_code == 200 else response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None