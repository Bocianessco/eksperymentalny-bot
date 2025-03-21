import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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

def fetch_product_links(driver):
    """Pobiera linki do t-shirtów w aktualnej kolekcji."""
    product_links = []
    try:
        # Czekaj na załadowanie linków do produktów
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/i/')]")))
        
        # Zbieramy wszystkie linki do produktów
        product_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/i/')]")
        
        for link in product_elements:
            href = link.get_attribute('href')
            if href and ('t-shirt' in href or 'classic-tee' in href or 'shirt' in href):  # Sprawdzamy obecność t-shirtu w linku
                print(f"Znaleziono link do t-shirtu: {href}")  # Debugowanie
                product_links.append(href)
    except Exception as e:
        print(f"Błąd podczas pobierania linków do t-shirtów: {e}")
    return product_links

def visit_collection(driver, collection_url):
    """Odwiedza konkretną kolekcję i losowo wybiera produkty do przetworzenia."""
    print(f"Otwieram kolekcję: {collection_url}")
    try:
        driver.get(collection_url)
        time.sleep(random.randint(3, 6))  # Dajemy czas na załadowanie strony

        # Pobierz produkty w tej kolekcji
        product_links = fetch_product_links(driver)
        if not product_links:
            print(f"Nie znaleziono t-shirtów w kolekcji: {collection_url}")
            return
        
        print(f"Znaleziono {len(product_links)} t-shirtów w kolekcji.")
        
        # Odwiedź losowo wybrane produkty
        random.shuffle(product_links)
        for product_url in product_links[:3]:  # Ograniczamy do 3 losowych t-shirtów
            print(f"Przechodzę do t-shirtu: {product_url}")
            driver.get(product_url)
            time.sleep(random.randint(5, 10))  # Dajemy czas na załadowanie strony produktu
                
    except Exception as e:
        print(f"Błąd podczas przetwarzania kolekcji {collection_url}: {e}")

# Zaktualizowana funkcja główna
def run_bot():
    """Główna funkcja sterująca botem."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
    try:
        while True:  # Nieskończona pętla
            random.shuffle(collection_links)  # Losowa kolejność odwiedzania kolekcji
            for collection_url in collection_links:
                visit_collection(driver, collection_url)
                time.sleep(random.randint(10, 20))  # Przerwa między kolekcjami
            print("Zakończono cykl odwiedzania kolekcji. Rozpoczynam nowy cykl...")
            time.sleep(random.randint(30, 60))  # Dłuższa przerwa między cyklami
            
    except KeyboardInterrupt:
        print("Bot został ręcznie zatrzymany.")
        
    finally:
        driver.quit()

# Uruchomienie bota
if __name__ == "__main__":
    run_bot()
