import schedule
import time
import json
from tracker import get_amazon_price
from notifier import send_email_alert

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def job():
    config = load_config()

    for item in config['products']:
        url = item['url']
        target_price = item['target_price']
        sender_email = config['email']['sender']
        sender_pass = config['email']['password']
        receiver_email = config['email']['receiver']

        title, price = get_amazon_price(url)
        if price is not None:
            print(f"Checked {title} - Current price: ${price}")
            if price <= target_price:
                send_email_alert(title, price, url, sender_email, sender_pass, receiver_email)
                print(f"Price dropped! Email sent for {title}")

# Schedule the job every hour
schedule.every(1).hours.do(job)

print("Scheduler started. Checking prices every hour...")

while True:
    schedule.run_pending()
    time.sleep(60)


