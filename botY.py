import time
import random
import requests

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

def fetch_product_links():
    """Pobiera linki do produktów w aktualnej kolekcji i filtruje tylko t-shirty."""
    product_links = []
    for collection_url in collection_links:
        try:
            # Wysyłanie zapytania HTTP do strony
            response = requests.get(collection_url)
            if response.status_code == 200:
                # Sprawdź, czy zawiera t-shirty, przykładowo przez analizowanie treści HTML (później możesz dodać bardziej zaawansowane filtrowanie)
                if 't-shirt' in response.text.lower():
                    product_links.append(collection_url)
            else:
                print(f"Nie udało się pobrać strony: {collection_url}")
        except Exception as e:
            print(f"Błąd podczas pobierania linków: {e}")
    return product_links

def visit_collection():
    """Odwiedza kolekcje i wybiera t-shirty."""
    print("Zbieram linki do t-shirtów...")
    try:
        # Pobierz linki do t-shirtów
        product_links = fetch_product_links()
        if not product_links:
            print("Nie znaleziono t-shirtów.")
            return

        print(f"Znaleziono {len(product_links)} t-shirtów.")
        
        # Losowo odwiedzamy 3 t-shirty
        random.shuffle(product_links)
        for product_url in product_links[:3]:  # Ograniczamy do 3 linków
            print(f"Odwiedzam t-shirt: {product_url}")
            # Możesz dodać logikę np. zapisywania odwiedzin lub interakcji z linkiem
            
    except Exception as e:
        print(f"Błąd podczas przetwarzania kolekcji: {e}")

def run_bot():
    """Główna funkcja sterująca botem."""
    try:
        while True:  # Pętla nieskończona
            visit_collection()
            time.sleep(random.randint(30, 60))  # Przerwa między cyklami
            
    except KeyboardInterrupt:
        print("Bot został ręcznie zatrzymany.")

if __name__ == "__main__":
    run_bot()
