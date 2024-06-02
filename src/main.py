import logging
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import praw

def setup_logger():
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all types of log messages

    # Create handlers
    console_handler = logging.StreamHandler()
    log_filename = datetime.now().strftime("%Y%m%d_log.txt")
    file_handler = logging.FileHandler(f"log/{log_filename}")

    # Set the logging level for handlers
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to the handlers
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

DESIRED_PRICE = 800.00

with open("secrets/reddit_app_id.txt") as app:
    APP_ID = app.read()

with open("secrets/reddit_app_token.txt") as token:
    APP_TOKEN = token.read()

with open("secrets/to_email.txt") as to_email:
    TO_EMAIL = to_email.read()

with open("secrets/from_email.txt") as from_email:
    FROM_EMAIL = from_email.read()

with open("secrets/app_password.txt") as py_sec:
    APP_PWD = py_sec.read()

CURRENCY_REGEX = r"(\$[0-9]+(.[0-9]+)?)"

def send_alert(subject, body, to_email, from_email, app_password):
    # Create the email header
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))
    
    # Set up the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        text = msg.as_string()
        logger.debug(f"Sending {text}")
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    reddit = praw.Reddit(
        client_id=APP_ID,
        client_secret=APP_TOKEN,
        user_agent="linux:4060Scraper:v0",
    )
    laptop_deals = reddit.subreddit("LaptopDeals")
    for submission in laptop_deals.stream.submissions():
        if "4060" in submission.title:
            currency_found = re.findall(CURRENCY_REGEX, submission.title)
            if currency_found:
                usable_vals = []
                for currency in currency_found:
                    usable_vals.append(float(currency[0][1:].replace(",","")))
                price_val = max(usable_vals)
                if price_val < DESIRED_PRICE:
                    message = submission.title + "\n\n" + submission.url
                    logger.debug(f"\nPost ID:{submission.id}\n\n Post Title: {submission.title}\n\n")
                    logger.info(f"Sending alert for {submission.id}")
                    send_alert(None, message, TO_EMAIL, FROM_EMAIL, APP_PWD)


if __name__ == "__main__":
    main()