import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URL Twojej strony
TARGET_URL = 'https://www.otodom.pl/pl/oferta/osiedle-zielona-dolina-cicha-okolica-ID4vyMw?utm_campaign=share_button_1748331048409'

# Liczba wizyt w ciągu godziny
NUM_VISITS = 15

# Czas trwania testu w sekundach (1 godzina)
TEST_DURATION = 60 * 60

# Oblicz średni interwał między wizytami
average_interval = TEST_DURATION / NUM_VISITS

# Funkcja do konfiguracji przeglądarki
def configure_browser():
    options = Options()
    options.add_argument("--headless")  # Tryb bez okna
    options.add_argument("--disable-gpu")  # Wyłączenie GPU
    options.add_argument("--disable-extensions")  # Wyłączenie rozszerzeń
    options.add_argument("--disable-dev-shm-usage")  # Zapobieganie problemom z pamięcią
    service = Service(ChromeDriverManager().install())  # Automatyczne zarządzanie ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Funkcja do odwiedzania strony
def visit_site(driver, url):
    driver.get(url)
    print(f"Odwiedzono: {url}")
    time.sleep(random.uniform(1, 3))  # Losowe opóźnienie między wizytami

# Główna funkcja uruchamiająca bota
def run_bot():
    driver = configure_browser()
    start_time = time.time()
    try:
        for _ in range(NUM_VISITS):
            visit_site(driver, TARGET_URL)
            # Oblicz pozostały czas i dostosuj interwał
            elapsed_time = time.time() - start_time
            remaining_time = TEST_DURATION - elapsed_time
            remaining_visits = NUM_VISITS - (_ + 1)
            if remaining_visits > 0:
                interval = remaining_time / remaining_visits
                time.sleep(random.uniform(interval * 0.8, interval * 1.2))
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
