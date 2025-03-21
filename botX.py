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
from selenium.webdriver.common.action_chains import ActionChains

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

def simulate_user_interaction(driver):
    """Funkcja do symulowania interakcji użytkownika."""
    elements = driver.find_elements(By.XPATH, "//a | //button | //img")
    if elements:
        random_element = random.choice(elements)
        try:
            random_element.click()
            log_message(f"Kliknięto w element: {random_element.text if random_element.text else 'brak tekstu'}")
            random_delay(2, 5)
        except Exception as e:
            log_message(f"Nie udało się kliknąć w element: {e}")

def random_scroll(driver):
    """Funkcja do losowego przewijania strony."""
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_positions = [random.randint(0, scroll_height) for _ in range(3)]
    for pos in scroll_positions:
        driver.execute_script(f"window.scrollTo(0, {pos});")
        random_delay(1, 3)

def fetch_product_links(driver, page_url):
    """Funkcja do zbierania linków do produktów."""
    product_links = set()  # Używamy zbioru, aby uniknąć duplikatów
    driver.get(page_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/maciekilcewicz/')]")))
    product_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/maciekilcewicz/')]")
    
    for product_element in product_elements:
        link = product_element.get_attribute('href')
        product_links.add(link)
    
    if len(product_links) > 0:
        log_message(f"Znaleziono {len(product_links)} produktów.")
    else:
        log_message("Nie znaleziono produktów w danej stronie.")
    
    return list(product_links)

def visit_random_products(driver, product_links, num_visits=10):
    """Funkcja do odwiedzania losowych produktów."""
    visited = set()  # Zbiór odwiedzonych linków
    
    while len(visited) < num_visits and len(visited) < len(product_links):
        product_link = random.choice(product_links)  # Losujemy link
        if product_link not in visited:
            visited.add(product_link)  # Dodajemy do odwiedzonych
            driver.get(product_link)  # Odwiedzamy link
            log_message(f"Odwiedzono: {product_link}")
            
            # Symulowanie interakcji użytkownika
            simulate_user_interaction(driver)
            random_scroll(driver)
            
            random_delay(5, 15)  # Losowe opóźnienie przed kolejnym produktem

    log_message(f"Odwiedzono {len(visited)} produktów na tej stronie.")

def retry_on_failure(func, max_retries=3, delay=5):
    """Funkcja do ponawiania prób w przypadku błędów."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            log_message(f"Próba {attempt + 1} nie powiodła się: {e}")
            time.sleep(delay)
    raise Exception(f"Nie udało się wykonać funkcji po {max_retries} próbach")

def visit_all_pages(driver, base_url):
    """Funkcja do odwiedzania wszystkich stron."""
    page_number = 1
    while True:
        log_message(f"Przechodzimy na stronę {page_number}")
        page_url = f"{base_url}{page_number}"
        
        # Pobieramy linki do produktów z bieżącej strony
        product_links = retry_on_failure(lambda: fetch_product_links(driver, page_url))

        # Jeśli produkty zostały znalezione, odwiedzamy je losowo
        if len(product_links) > 0:
            visit_random_products(driver, product_links)
        else:
            log_message(f"Brak produktów na stronie {page_number}.")
            break  # Jeśli na bieżącej stronie nie ma produktów, kończymy

        # Przechodzimy na kolejną stronę
        page_number += 1
        random_delay(2, 5)  # Losowe opóźnienie przed przejściem na kolejną stronę

def run_bot():
    """Główna funkcja, która uruchamia bota."""
    driver = configure_browser()

    try:
        # Przechodzimy przez wszystkie strony i odwiedzamy produkty
        visit_all_pages(driver, BASE_URL)
    
    finally:
        driver.quit()  # Zamykamy przeglądarkę po zakończeniu

# Uruchomienie bota
if __name__ == "__main__":
    run_bot()
