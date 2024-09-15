import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator=' ', strip=True)

    cleaned_text = clean_scrap_data(text)
    return {url: cleaned_text}

def clean_scrap_data(scrapped_data):
    scrapped_data = re.sub(r'\s+', ' ', scrapped_data).strip()
    
    scrapped_data = re.sub(r'<[^>]+>', '', scrapped_data)
    
    scrapped_data = re.sub(r'[^\w\s.,!?-]', '', scrapped_data)
    
    return scrapped_data