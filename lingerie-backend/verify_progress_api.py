import requests
import time
import sys

BASE_URL = 'http://localhost:5001/api'

def test_progress_api():
    print(f"Testing progress API at {BASE_URL}")
    
    # 1. Start Scraper
    print("1. Starting scraper...")
    try:
        resp = requests.post(f"{BASE_URL}/scraper/executar")
        if resp.status_code == 200:
            print("Scraper started successfully.")
        elif resp.status_code == 400:
            print("Scraper already running, continuing to monitor...")
        else:
            print(f"Failed to start scraper: {resp.status_code} - {resp.text}")
            return
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return

    # 2. Poll Progress
    print("2. Polling progress...")
    for i in range(30): # Monitor for up to 30 seconds
        try:
            resp = requests.get(f"{BASE_URL}/scraper/progress")
            data = resp.json()
            
            print(f"[{i}s] Status: {data.get('status')} | Progress: {data.get('percentage')}% | Message: {data.get('message')}")
            
            if data.get('status') in ['completed', 'error']:
                print(f"Final Status: {data.get('status')}")
                break
                
            time.sleep(1)
        except Exception as e:
            print(f"Polling error: {e}")
            break

if __name__ == "__main__":
    test_progress_api()
