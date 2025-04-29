import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playwright.sync_api import sync_playwright
import logging

CACHE_FILE = 'job_list_cache/jobs.txt'
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def fetch_jobs():
    logging.info("Fetching job listings from the website...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://careers.cityfootballgroup.com/search')
        job_elements = page.query_selector_all('.job-row')
        jobs = [job.inner_text() for job in job_elements]
        browser.close()
    logging.info(f"Fetched {len(jobs)} job listings.")
    return jobs

def load_cached_jobs():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return f.read().splitlines()
    return []

def save_jobs_to_cache(jobs):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        f.write('\n'.join(jobs))

def send_email(jobs):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = 'New Job Listings'
    body = '\n'.join(jobs)
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

def main():
    latest_jobs = fetch_jobs()
    cached_jobs = load_cached_jobs()

    if latest_jobs != cached_jobs:
        logging.info("New job listings found.")
        if EMAIL_ADDRESS and EMAIL_USER and EMAIL_PASSWORD:
            logging.info("Sending email...")
            send_email(latest_jobs)
        else:
            logging.error("Cowardly refusing to send email because the necessary environment variables are not set")
        save_jobs_to_cache(latest_jobs)
    else:
        logging.info("No new job listings found.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
