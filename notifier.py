import smtplib
from email.mime.text import MIMEText
from plyer import notification  # pip install plyer

def send_email(subject, body, sender_email, sender_pass, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_pass)
    server.send_message(msg)
    server.quit()

def send_popup(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )


