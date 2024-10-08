#pip install requests beautifulsoup4 pandas


import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.indeed.com/jobs?q=software+developer&start="

def get_job_listings(page):
    url = BASE_URL + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard')
    jobs = []

    for job in job_cards:
        title = job.find('h2', class_='title').text.strip()
        company = job.find('span', class_='company').text.strip()
        location = job.find('div', class_='location').text.strip() if job.find('div', class_='location') else "Not specified"
        description = job.find('div', class_='summary').text.strip()

        jobs.append({
            'Job Title': title,
            'Company': company,
            'Location': location,
            'Description': description
        })
    
    return jobs

def scrape_jobs(pages):
    all_jobs = []
    for page in range(0, pages * 10, 10):
        all_jobs.extend(get_job_listings(page))
        print(f"Scraped page {page // 10 + 1}")
    
    return all_jobs

def save_to_csv(jobs, filename):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    num_pages = int(input("Enter the number of pages to scrape: "))
    job_data = scrape_jobs(num_pages)
    save_to_csv(job_data, 'job_listings.csv')
