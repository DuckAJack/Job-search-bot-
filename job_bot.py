# jobsearchbot - Cisco Collaboration Engineer Job Scraper (LinkedIn + Indeed)

import os
import requests
from bs4 import BeautifulSoup
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# 1. Scrape Jobs from Indeed

def scrape_jobs():
    url = "https://www.indeed.com/jobs?q=Cisco+Collaboration+Engineer&l=Brno"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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


# 2. Scrape Jobs from LinkedIn
def scrape_linkedin_jobs():
    url = "https://www.linkedin.com/jobs/search/?keywords=Cisco%20Collaboration%20Engineer&location=Brno"
    jobs = []
    
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Let page load fully

        # Scroll to load jobs
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all('div', class_='base-card')
        
        for job in job_elements:
            title_element = job.find('h3')
            link_element = job.find('a', href=True)
            
            if title_element and link_element:
                title = title_element.text.strip()
                link = link_element['href']
                jobs.append({'title': title, 'link': link})

    except Exception as e:
        print(f"Error fetching LinkedIn jobs: {e}")
    
    finally:
        driver.quit()  # Close the browser
    
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
