
import time
import random
import requests
from bs4 import BeautifulSoup

# Lista linków do kolekcji
collection_links = [
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141513&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141530&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141531&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141533&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141534&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141535&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141536&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141538&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141539&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141540&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4141541&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4146936&iaCode=all-departments&sortOrder=relevant",
    "https://www.redbubble.com/people/bocianessco/shop?artistUserName=Bocianessco&collections=4160094&iaCode=all-departments&sortOrder=relevant"
]

def fetch_product_links(collection_url):
    """Pobiera linki do produktów w aktualnej kolekcji i filtruje tylko t-shirty."""
    product_links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Wysyłanie zapytania HTTP do strony
        response = requests.get(collection_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Znajdujemy wszystkie linki, które zawierają "/i/" (linki do produktów)
            product_elements = soup.find_all('a', href=True)
            
            for link in product_elements:
                href = link['href']
                if 't-shirt' in href.lower():  # Filtrowanie tylko t-shirtów
                    product_links.append(f"https://www.redbubble.com{href}")
        else:
            print(f"Nie udało się pobrać strony: {collection_url}")
 
