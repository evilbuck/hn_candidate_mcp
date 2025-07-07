import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class HackerNewsScraper:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self.base_url = "https://news.ycombinator.com"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def scrape_job_postings(self, hn_thread_id: str = "44434574") -> List[Dict[str, Any]]:
        """
        Scrape job postings from HackerNews 'Who's Hiring' thread
        """
        cache_file = os.path.join(self.cache_dir, f"hn_jobs_{hn_thread_id}.json")
        
        # Check if cached data exists and is recent (less than 1 hour old)
        if os.path.exists(cache_file):
            file_age = datetime.now().timestamp() - os.path.getmtime(cache_file)
            if file_age < 3600:  # 1 hour in seconds
                print(f"Loading from cache: {cache_file}")
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        print(f"Scraping HackerNews thread: {hn_thread_id}")
        url = f"{self.base_url}/item?id={hn_thread_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            comments = soup.find_all('tr', class_='athing comtr')
            
            job_postings = []
            
            for comment in comments:
                try:
                    # Extract comment text
                    comment_text_elem = comment.find('div', class_='comment')
                    if not comment_text_elem:
                        continue
                    
                    comment_text = comment_text_elem.get_text(strip=True)
                    
                    # Skip if comment is too short (likely not a job posting)
                    if len(comment_text) < 100:
                        continue
                    
                    # Extract comment metadata
                    comment_id = comment.get('id', '')
                    
                    # Extract author
                    author_elem = comment.find('a', class_='hnuser')
                    author = author_elem.get_text(strip=True) if author_elem else "Unknown"
                    
                    # Extract timestamp
                    time_elem = comment.find('span', class_='age')
                    timestamp = time_elem.get('title', '') if time_elem else ""
                    
                    job_posting = {
                        'id': comment_id,
                        'author': author,
                        'timestamp': timestamp,
                        'text': comment_text,
                        'scraped_at': datetime.now().isoformat(),
                        'thread_id': hn_thread_id
                    }
                    
                    job_postings.append(job_posting)
                    
                except Exception as e:
                    print(f"Error parsing comment: {e}")
                    continue
            
            # Cache the results
            with open(cache_file, 'w') as f:
                json.dump(job_postings, f, indent=2)
            
            print(f"Scraped {len(job_postings)} job postings")
            return job_postings
            
        except requests.RequestException as e:
            print(f"Error fetching HackerNews thread: {e}")
            return []
    
    def search_jobs(self, query: str, job_postings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Simple text search through job postings
        """
        query_lower = query.lower()
        matching_jobs = []
        
        for job in job_postings:
            if query_lower in job['text'].lower():
                matching_jobs.append(job)
        
        return matching_jobs

if __name__ == "__main__":
    scraper = HackerNewsScraper()
    jobs = scraper.scrape_job_postings()
    print(f"Found {len(jobs)} job postings")
    
    # Example search
    if jobs:
        python_jobs = scraper.search_jobs("python", jobs)
        print(f"Found {len(python_jobs)} Python jobs")