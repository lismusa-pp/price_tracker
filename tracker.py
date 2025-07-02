from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

def find_first_amazon_product_url(keywords):
    search_query = '+'.join(keywords.strip().split())
    search_url = f"https://www.amazon.com/s?k={search_query}"

    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find('a', {'class': 'a-link-normal s-no-outline'})
        if result and 'href' in result.attrs:
            return "https://www.amazon.com" + result['href']
        return None
    except Exception as e:
        print(f"[Search Error] {e}")
        return None 
    

def clean_amazon_url(url):
    match = re.search(r"(https://www\.amazon\.com/dp/[A-Z0-9]{10})", url)
    if match:
        return match.group(1) + "/"
    return url

def get_amazon_price(url):
    url = clean_amazon_url(url)
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--lang=en-US")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        print("✅ Page loaded")
        
        with open("page_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            print("✅ HTML saved to page_debug.html")


        # Wait for product title to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )

        title = driver.find_element(By.ID, "productTitle").text.strip()

        try:
            price = driver.find_element(By.ID, "priceblock_ourprice").text
        except:
            try:
                price = driver.find_element(By.ID, "priceblock_dealprice").text
            except:
                try:
                    price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
                except:
                    price = None

        driver.quit()

        if price:
            price = price.replace('$', '').replace(',', '').strip()
            return title, float(price)
        else:
            return title, None

    except Exception as e:
        print(f"[Selenium Error] {e}")
        return None, None
