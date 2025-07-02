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

def clean_amazon_url(url):
    import re
    # Extract /dp/ASIN pattern and rebuild URL
    match = re.search(r"(https://www\.amazon\.com/dp/[A-Z0-9]{10})", url)
    if match:
        return match.group(1) + "/"
    else:
        return url  # fallback: use original URL if no match



def find_first_amazon_product_url(keywords):
    import requests
    from bs4 import BeautifulSoup

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    search_query = '+'.join(keywords.strip().split())
    search_url = f"https://www.amazon.com/s?k={search_query}"

    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    result = soup.find('a', {'class': 'a-link-normal s-no-outline'})
    if result and 'href' in result.attrs:
        product_url = "https://www.amazon.com" + result['href']
        return product_url
    else:
        return None

def get_amazon_price(url):
    url = clean_amazon_url(url)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find(id='productTitle')
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        price_tags = [
            soup.find(id='priceblock_ourprice'),
            soup.find(id='priceblock_dealprice'),
            soup.find('span', class_='a-price-whole'),
            soup.find('span', class_='a-offscreen')
        ]

        for tag in price_tags:
            if tag:
                print(f"DEBUG - Found price tag HTML: {tag}")
                price_text = tag.get_text(strip=True)
                print(f"DEBUG - Extracted price text: {price_text}")
                price_text = price_text.replace('$', '').replace(',', '').strip()
                try:
                    price = float(price_text.split()[0])
                    return title, price
                except Exception as e:
                    print(f"DEBUG - Price conversion error: {e}")
                    continue

        print("DEBUG - No price found in known tags.")
        return title, None

    except Exception as e:
        print(f"Error fetching price: {e}")
        return None, None
