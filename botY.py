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
    "https://www.redbubble.com/people/Bocianessco/shop",
    "https://viralstyle.com/maciekilcewicz/mustardos-mc-hoodie-hot-heads-cold-bee",
    "https://viralstyle.com/maciekilcewicz/ketchupas-mc-hoodie-born-to-squeeze",
    "https://viralstyle.com/maciekilcewicz/mayonnaise-mc-hoodie-spread-the-chaos",
    "https://viralstyle.com/maciekilcewicz/sons-of-arthritis-ride-slow-or-dont",
    "https://viralstyle.com/maciekilcewicz/sons-of-autism-different-minds-same-ri",
    "https://viralstyle.com/maciekilcewicz/sons-of-altzhaimer-who-how-where",
    "https://www.redbubble.com/i/t-shirt/Forgot-Where-We-Parked-MC-Funny-Vintage-Skull-Biker-Club-by-Bocianessco/185846922/lrcw",
    "https://www.redbubble.com/i/t-shirt/Rusty-Joints-Riding-Club-Old-School-Biker-Still-Full-Throttle-by-Bocianessco/185846832/z5wf",
    "https://www.redbubble.com/i/t-shirt/Different-Minds-Riding-Club-Ride-Your-Own-Road-Skull-Biker-Art-by-Bocianessco/185846731/lrcw",
    "https://www.redbubble.com/i/t-shirt/Mustardos-MC-Hot-Heads-Cold-Beer-Vintage-Skull-Biker-Motorcycle-Art-by-Bocianessco/185846622/e22z",
    "https://www.redbubble.com/i/t-shirt/Mayonnaise-MC-Spread-the-Chaos-Funny-Biker-Skull-Motorcycle-Club-by-Bocianessco/185846046/2cn5",
    "https://www.redbubble.com/i/t-shirt/Ketchupas-MC-Born-to-Squeeze-Funny-Skull-Biker-Motorcycle-Club-by-Bocianessco/185845913/z5wf",
    "https://www.redbubble.com/i/apron/Christmas-Chaos-Funny-Christmas-Design-for-Holiday-Lovers-by-Bocianessco/185744596/2b5j",
    "https://www.redbubble.com/i/t-shirt/Santa-s-Favorite-Problem-Funny-Christmas-Holiday-Design-by-Bocianessco/185744492/rfjh",
    "https://www.redbubble.com/i/dress/Christmas-Calories-Don-t-Count-Funny-Holiday-Gift-by-Bocianessco/185743473/3yb7",
    "https://www.redbubble.com/i/dress/Funny-Christmas-Couple-Design-Santa-s-Favorite-Trouble-Makers-Humorous-Holiday-Art-Festive-Christmas-Gift-by-Bocianessco/185741987/3yb7",
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



