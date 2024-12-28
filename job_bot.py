#jobsearchbot

import requests
from bs4 import BeautifulSoup

def scrape_jobs():
    url = "https://www.indeed.com/jobs?q=Cisco+Collaboration+Engineer&l=Brno"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job in soup.find_all('div', class_='job_seen_beacon'):
        title = job.find('h2').text
        link = job.find('a')['href']
        jobs.append({'title': title, 'link': link})
    return jobs

#Filter jobs

def filter_jobs(jobs):
    relevant_jobs = []
    keywords = ['CUCM', 'Webex', 'VoIP']
    for job in jobs:
        if any(keyword in job['title'] for keyword in keywords):
            relevant_jobs.append(job)
    return relevant_jobs

#TelegramNotifications

import smtplib

def send_email(job_list):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your_email", "password")
        message = "Subject: New Job Listings\n\n"
        message += "\n".join([f"{job['title']} - {job['link']}" for job in job_list])
        server.sendmail("your_email", "recipient_email", message)
