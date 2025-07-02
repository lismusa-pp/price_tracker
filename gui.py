import customtkinter as ctk
from tracker import get_amazon_price
from notifier import send_email_alert

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PriceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛒 Product Price Tracker")
        self.geometry("500x400")

        # URL input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Amazon product URL")
        self.url_entry.pack(pady=10)

        # Target price
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Target price (e.g. 50)")
        self.price_entry.pack(pady=10)

        # Email details
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Your Gmail")
        self.email_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="App Password", show="*")
        self.pass_entry.pack(pady=10)

        self.receiver_entry = ctk.CTkEntry(self, placeholder_text="Receiver Email")
        self.receiver_entry.pack(pady=10)

        # Button
        self.track_btn = ctk.CTkButton(self, text="Track Now", command=self.track_price)
        self.track_btn.pack(pady=20)

        # Status
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def track_price(self):
        url = self.url_entry.get()
        target_price = float(self.price_entry.get())
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

if __name__ == "__main__":
    app = PriceTrackerApp()
    app.mainloop()
