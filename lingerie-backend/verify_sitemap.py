import requests
import time
import sys
import threading
from flask import Flask

# Need to mock the app structure or run this within the app context if accessing DB directly
# Easier to test via API if the server is running, but let's assume server is running
BASE_URL = 'http://localhost:5001/api'

def test_sitemap_scraper():
    print(f"Testing Sitemap Scraper via API at {BASE_URL}")
    
    # 1. Start Scraper with Sitemap Strategy
    print("1. Starting scraper (strategy='sitemap')...")
    try:
        resp = requests.post(f"{BASE_URL}/scraper/executar", json={'strategy': 'sitemap'})
        if resp.status_code == 200:
            print("Scraper started successfully.")
        elif resp.status_code == 400:
            print("Scraper already running, continuing to monitor...")
        else:
            print(f"Status Request: {resp.status_code}")
            print(f"Error Body: {resp.text}")
            return
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return

    # 2. Poll Progress
    print("2. Polling progress...")
    max_duration = 120 # Monitor for 2 minutes
    start_time = time.time()
    
    while (time.time() - start_time) < max_duration:
        try:
            resp = requests.get(f"{BASE_URL}/scraper/progress")
            data = resp.json()
            
            print(f"Status: {data.get('status')} | Progress: {data.get('percentage')}% | Message: {data.get('message')}")
            
            if data.get('status') in ['completed', 'error']:
                print(f"Final Status: {data.get('status')}")
                break
                
            time.sleep(2)
        except Exception as e:
             print(f"Polling error: {e}")
             break

if __name__ == "__main__":
    test_sitemap_scraper()
