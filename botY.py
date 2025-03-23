import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
    """Pobiera linki do wszystkich produktów na stronie."""
    product_links = []
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/i/')]")))
        product_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/i/')]")

        for link in product_elements:
            href = link.get_attribute('href')
            if href and 'Bocianessco' in href:
                product_links.append(href)
    except Exception as e:
        print(f"Błąd podczas pobierania linków do produktów: {e}")
    return product_links

def visit_collection(driver, collection_url):
    """Odwiedza kolekcję i losowo wybiera produkty."""
    print(f"Otwieram kolekcję: {collection_url}")
    try:
        driver.get(collection_url)
        time.sleep(random.randint(3, 6))

        # Pobierz linki do produktów
        product_links = fetch_product_links(driver)
        if not product_links:
            print(f"Nie znaleziono produktów w kolekcji: {collection_url}")
            return
        
        print(f"Znaleziono {len(product_links)} produktów w kolekcji.")
        
        # Odwiedź losowe produkty
        random.shuffle(product_links)
        for product_url in product_links[:3]:
            print(f"Przechodzę do produktu: {product_url}")
            driver.get(product_url)
            time.sleep(random.randint(5, 10))
                
    except Exception as e:
        print(f"Błąd podczas przetwarzania kolekcji {collection_url}: {e}")

def run_bot():
    """Uruchamia bota w trybie headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tryb bez okna
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--remote-debugging-port=9222")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        while True:
            random.shuffle(collection_links)
            for collection_url in collection_links:
                visit_collection(driver, collection_url)
                time.sleep(random.randint(10, 20))
            print("Zakończono cykl odwiedzania kolekcji. Rozpoczynam nowy cykl...")
            time.sleep(random.randint(30, 60))  
            
    except KeyboardInterrupt:
        print("Bot został ręcznie zatrzymany.")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
