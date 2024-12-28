import os
import requests
from bs4 import BeautifulSoup
import smtplib
import random
from playwright.sync_api import sync_playwright

# 1. Scrape Jobs from Indeed
# Rotating User-Agent headers to bypass blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
]

def scrape_indeed_jobs():
    url = "https://www.indeed.com/jobs?q=Cisco+Collaboration+Engineer&l=Brno"
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print("Access denied by Indeed, check headers or IP blocking.")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job in soup.find_all('div', class_='job_seen_beacon'):
        title = job.find('h2').text
        link = job.find('a')['href']
        jobs.append({'title': title, 'link': link})
    return jobs

# 2. Scrape Jobs from LinkedIn using Playwright
def scrape_linkedin_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.linkedin.com/jobs/search?keywords=Cisco%20Collaboration%20Engineer&location=Brno")
        
        # Wait for the job elements to be visible
        page.wait_for_selector('.job-card-container')
        
        jobs = []
        job_elements = page.query_selector_all('.job-card-container')
        
        for job in job_elements:
            title = job.query_selector('.job-card-list__title').text_content()
            link = job.query_selector('a').get_attribute('href')
            jobs.append({'title': title, 'link': link})
        
        browser.close()
        return jobs

# 3. Filter Relevant Jobs
def filter_jobs(jobs):
    relevant_jobs = []
    keywords = ['CUCM', 'Webex', 'VoIP']

    for job in jobs:
        if any(keyword.lower() in job['title'].lower() for keyword in keywords):
            relevant_jobs.append(job)

    return relevant_jobs

# 4. Send Email Notification
def send_email(job_list):
    if not job_list:
        print("No relevant jobs found.")
        return
    
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    recipient = os.getenv('RECIPIENT_EMAIL')

    if not email_user or not email_pass or not recipient:
        print("Email credentials not set.")
        return

    message = "Subject: New Job Listings\n\n"
    message += "\n".join([f"{job['title']} - {job['link']}" for job in job_list])

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, recipient, message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 5. Run the Bot
if __name__ == "__main__":
    indeed_jobs = scrape_indeed_jobs()
    linkedin_jobs = scrape_linkedin_jobs()

    all_jobs = indeed_jobs + linkedin_jobs
    filtered_jobs = filter_jobs(all_jobs)
    send_email(filtered_jobs)
