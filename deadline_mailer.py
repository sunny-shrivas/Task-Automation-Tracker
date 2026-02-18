import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# ================= CONFIG =================

EXCEL_FILE = "tasks.xlsx"
REMINDER_DAYS = 2   # notify if deadline is within 2 days

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Gmail App Password

# ==========================================

def send_email(receiver_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

def main():
    df = pd.read_excel(EXCEL_FILE)

    today = datetime.today().date()
    reminder_limit = today + timedelta(days=REMINDER_DAYS)

    for _, row in df.iterrows():
        deadline = pd.to_datetime(row["Deadline"]).date()

        if today <= deadline <= reminder_limit:
            name = row["Name"]
            email = row["Email"]
            task = row["Task"]

            subject = f"⏰ Deadline Reminder: {task}"

            body = f"""
Hi {name},

This is a reminder that your task:

📌 Task: {task}
📅 Deadline: {deadline}

is approaching soon.

Please ensure it is completed on time.

Regards,
Automation Bot 🤖
"""

            send_email(email, subject, body)
            print(f"Reminder sent to {name} ({email})")

if __name__ == "__main__":
    main()
