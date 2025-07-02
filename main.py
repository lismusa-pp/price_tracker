
import json
from tracker import get_amazon_price
from notifier import send_popup  # or send_email

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

def main():
    config = load_config()

    for item in config['products']:
        url = item['url']
        target_price = item['target_price']

        title, current_price = get_amazon_price(url)

        if current_price is not None:
            print(f"[{title}] Current Price: ${current_price}")

            if current_price <= target_price:
                send_popup("Price Alert!", f"{title} is now ${current_price}!")
                # send_email(...) if preferred

if __name__ == "__main__":
    main()
