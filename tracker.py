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

def get_amazon_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find(id='productTitle')
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        price_tag = (
            soup.find('span', {'class': 'a-price-whole'}) or 
            soup.find('span', {'id': 'priceblock_ourprice'}) or
            soup.find('span', {'id': 'priceblock_dealprice'})
        )
        if price_tag:
            price_str = price_tag.get_text(strip=True).replace(',', '').replace('$', '')
            price = float(price_str.split('.')[0])
            return title, price
        else:
            return title, None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None, None
