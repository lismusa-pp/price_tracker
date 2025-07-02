import customtkinter as ctk
import threading
import schedule
import time
import json
from tracker import get_amazon_price, find_first_amazon_product_url
from notifier import send_email_alert

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PriceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛒 Product Price Tracker")
        self.geometry("600x700")

        # Keywords input
        self.keywords_entry = ctk.CTkEntry(self, placeholder_text="Enter product keywords (e.g. wireless earbuds)")
        self.keywords_entry.pack(pady=10, padx=10, fill='x')

        self.find_url_btn = ctk.CTkButton(self, text="Find Product URL", command=self.find_product_url)
        self.find_url_btn.pack(pady=5)

        self.found_url_label = ctk.CTkLabel(self, text="No URL found yet")
        self.found_url_label.pack(pady=5)

        # Target price input
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Target price (e.g. 50)")
        self.price_entry.pack(pady=10, padx=10, fill='x')

        # Email inputs
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Your Gmail")
        self.email_entry.pack(pady=10, padx=10, fill='x')

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Gmail App Password", show="*")
        self.pass_entry.pack(pady=10, padx=10, fill='x')

        self.receiver_entry = ctk.CTkEntry(self, placeholder_text="Receiver Email")
        self.receiver_entry.pack(pady=10, padx=10, fill='x')

        # Manual check button
        self.track_btn = ctk.CTkButton(self, text="Check Price Now", command=self.track_price)
        self.track_btn.pack(pady=10)

        # Scheduler control buttons
        self.start_btn = ctk.CTkButton(self, text="Start Auto Tracking", command=self.start_scheduler)
        self.start_btn.pack(pady=10)

        self.stop_btn = ctk.CTkButton(self, text="Stop Auto Tracking", command=self.stop_scheduler, state='disabled')
        self.stop_btn.pack(pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=20)

        self.found_url = None
        self.scheduler_thread = None
        self.scheduler_running = False

    def find_product_url(self):
        keywords = self.keywords_entry.get()
        if not keywords.strip():
            self.status_label.configure(text="❌ Please enter product keywords.")
            return

        self.status_label.configure(text="🔎 Searching Amazon...")
        self.update()  # Refresh GUI to show status immediately

        url = find_first_amazon_product_url(keywords)
        if url:
            self.found_url = url
            self.found_url_label.configure(text=f"URL found:\n{url}")
            self.status_label.configure(text="✅ Product URL found!")
        else:
            self.found_url = None
            self.found_url_label.configure(text="No URL found")
            self.status_label.configure(text="❌ Could not find product URL.")

    def track_price(self):
        url = self.found_url
        if not url:
            self.status_label.configure(text="❌ No product URL found. Search first.")
            return

        try:
            target_price = float(self.price_entry.get())
        except ValueError:
            self.status_label.configure(text="❌ Enter a valid target price.")
            return

        sender = self.email_entry.get()
        password = self.pass_entry.get()
        receiver = self.receiver_entry.get()

        title, current_price = get_amazon_price(url)

        if current_price is None:
            self.status_label.configure(text="❌ Couldn't fetch price.")
            return

        if current_price <= target_price:
            send_email_alert(title, current_price, url, sender, password, receiver)
            self.status_label.configure(text=f"✅ Alert Sent! {title} = ${current_price}")
        else:
            self.status_label.configure(text=f"ℹ️ Price still high: ${current_price}")

    def start_scheduler(self):
        if self.scheduler_running:
            self.status_label.configure(text="Scheduler already running.")
            return

        url = self.found_url
        if not url:
            self.status_label.configure(text="❌ No product URL found. Search first.")
            return

        try:
            target_price = float(self.price_entry.get())
        except ValueError:
            self.status_label.configure(text="❌ Enter a valid target price.")
            return

        config = {
            "products": [
                {
                    "url": url,
                    "target_price": target_price
                }
            ],
            "email": {
                "sender": self.email_entry.get(),
                "password": self.pass_entry.get(),
                "receiver": self.receiver_entry.get()
            }
        }

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        self.scheduler_running = True
        self.status_label.configure(text="✅ Auto tracking started. Checks every hour.")

        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()

        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')

    def stop_scheduler(self):
        if not self.scheduler_running:
            self.status_label.configure(text="Scheduler is not running.")
            return

        self.scheduler_running = False
        self.status_label.configure(text="⏸️ Auto tracking stopped.")

        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')

    def run_scheduler(self):
        def job():
            if not self.scheduler_running:
                return schedule.CancelJob

            config = self.load_config()

            email_conf = config.get('email', {})
            sender_email = email_conf.get('sender')
            sender_pass = email_conf.get('password')
            receiver_email = email_conf.get('receiver')

            for item in config['products']:
                url = item['url']
                target_price = item['target_price']

                title, price = get_amazon_price(url)
                if price is not None:
                    print(f"Checked {title} - Current price: ${price}")
                    if price <= target_price:
                        send_email_alert(title, price, url, sender_email, sender_pass, receiver_email)
                        print(f"Price dropped! Email sent for {title}")

        schedule.every(1).hours.do(job)

        while self.scheduler_running:
            schedule.run_pending()
            time.sleep(60)

    def load_config(self):
        try:
            with open('config.json', 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

if __name__ == "__main__":
    app = PriceTrackerApp()
    app.mainloop()
