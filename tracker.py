
import requests
from bs4 import BeautifulSoup

#  Directly define the headers here
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

def get_amazon_price(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find(id='productTitle')
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = "No title found"

    price_tag = (
        soup.find('span', {'class': 'a-price-whole'}) or 
        soup.find('span', {'id': 'priceblock_ourprice'}) or
        soup.find('span', {'id': 'priceblock_dealprice'})  # covers more Amazon layouts
    )

    if price_tag:
        price_str = price_tag.get_text(strip=True).replace(',', '').replace('$', '')
        try:
            price = float(price_str.split('.')[0])
            return title, price
        except:
            return title, None
    else:
        return title, None

