import smtplib
from email.mime.text import MIMEText

def send_email_alert(product_title, current_price, url, sender_email, sender_pass, receiver_email):
    subject = f"Price Drop Alert: {product_title}"
    body = f"The price for '{product_title}' has dropped to ${current_price}!\n\nCheck it here: {url}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_pass)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
