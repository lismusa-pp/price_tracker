
import requests
from bs4 import BeautifulSoup
import headers

def get_amazon_price(url):
    headers = {
        "User-Agent": headers.USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find(id='productTitle').get_text(strip=True)
    
    price_str = (
        soup.find('span', {'class': 'a-price-whole'}) or 
        soup.find('span', {'id': 'priceblock_ourprice'})
    )

    if price_str:
        price = float(price_str.get_text(strip=True).replace(',', '').replace('$', '').split('.')[0])
        return title, price
    else:
        return title, None
