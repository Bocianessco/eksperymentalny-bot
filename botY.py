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
    "https://www.redbubble.com/i/sweatshirt/Storm-of-Power-Political-Satire-War-Cartoon-Art-v3-by-Bocianessco/178909341/cdux",
    "https://www.redbubble.com/i/hoodie/Storm-of-Power-Political-Satire-War-Cartoon-Art-v1-by-Bocianessco/178908431/ng59",
    "https://www.redbubble.com/i/t-shirt/The-Future-Is-Tired-Dark-Aesthetic-Streetwear-Graphic-by-Bocianessco/179504173/z4fd",
    "https://www.redbubble.com/i/t-shirt/ERROR-404-Human-Not-Found-Glitch-Streetwear-Design-by-Bocianessco/179504127/rfjh",
    "https://www.redbubble.com/i/t-shirt/Game-On-Always-by-Bocianessco/179323615/e22z",
    "https://www.redbubble.com/i/t-shirt/Brotherhood-on-Wheels-by-Bocianessco/179403212/rfjh",
    "https://www.redbubble.com/i/sweatshirt/The-Symbolism-Here-Is-Brutal-by-Bocianessco/179092731/cdux",
    "https://www.redbubble.com/i/sweatshirt/Storm-of-Power-Political-Satire-War-Cartoon-Art-v3-by-Bocianessco/178909341/cdux",
  
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



