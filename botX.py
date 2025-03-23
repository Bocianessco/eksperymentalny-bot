import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL Twojej kolekcji
BASE_URL = 'https://viralstyle.com/store/maciekilcewicz/bocianessco/'

# Lista User-Agentów
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

# Konfiguracja logowania
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message):
    """Funkcja do zapisywania logów."""
    logging.info(message)
    print(message)

def random_delay(min_seconds=2, max_seconds=10):
    """Funkcja do losowego opóźnienia."""
    time.sleep(random.randint(min_seconds, max_seconds))

def configure_browser():
    """Funkcja do konfiguracji przeglądarki."""
    options = Options()
    options.add_argument("--headless")  # Tryb bez okna
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")  # Losowy User-Agent
    options.add_argument("--disable-gpu")  # Wyłączenie GPU
    options.add_argument("--disable-extensions")  # Wyłączenie rozszerzeń
    options.add_argument("--disable-dev-shm-usage")  # Zapobieganie problemom z pamięcią
    service = Service(ChromeDriverManager().install())  # Automatyczne zarządzanie ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_product_links(driver, page_url):
    """Funkcja do zbierania linków do produktów."""
    product_links = set()  # Używamy zbioru, aby uniknąć duplikatów
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/maciekilcewicz/')]")))
    product_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/maciekilcewicz/')]")
    
    for product_element in product_elements:
        link = product_element.get_attribute('href')
        product_links.add(link)
    
    if product_links:
        log_message(f"Znaleziono {len(product_links)} produktów.")
    else:
        log_message("Nie znaleziono produktów na tej stronie.")
    
    return list(product_links)

def visit_product(driver, product_url):
    """Funkcja do odwiedzania pojedynczego produktu."""
    try:
        driver.get(product_url)
        log_message(f"Odwiedzono: {product_url}")
        random_delay(5, 15)  # Losowe opóźnienie
    except Exception as e:
        log_message(f"Błąd podczas odwiedzania {product_url}: {e}")

def visit_all_products(driver, base_url):
    """Funkcja do odwiedzania wszystkich produktów w kolekcji."""
    page_number = 1
    while page_number <= 17:  # Tylko strony 1-17
        page_url = f"{base_url}{page_number}"
        log_message(f"Przechodzę na stronę: {page_url}")
        
        product_links = fetch_product_links(driver, page_url)
        if not product_links:
            log_message("Brak produktów na tej stronie. Kończę przeszukiwanie.")
            break
        
        for product_link in product_links:
            visit_product(driver, product_link)
            random_delay(2, 5)  # Losowe opóźnienie między produktami
        
        page_number += 1
        random_delay(2, 5)  # Losowe opóźnienie między stronami

def run_bot():
    """Główna funkcja uruchamiająca bota."""
    driver = configure_browser()
    try:
        visit_all_products(driver, BASE_URL)
    except Exception as e:
        log_message(f"Wystąpił błąd: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
