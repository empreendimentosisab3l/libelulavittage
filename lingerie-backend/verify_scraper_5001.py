import requests
import time
import json

BASE_URL = 'http://localhost:5001/api'

def verify_scraper():
    print(f"Connecting to {BASE_URL}...")
    
    # 1. Check Status
    try:
        resp = requests.get(f"{BASE_URL}/scraper/progress")
        print(f"Initial Progress Status: {resp.status_code}")
        print(resp.json())
        
        # If running, we can't start again, but that's a good sign it's working
        if resp.json().get('status') == 'running':
            print("Scraper is already running. Monitoring...")
        else:
            # 2. Start Scraper
            print("Starting Scraper (Strategy: Smart)...")
            resp = requests.post(f"{BASE_URL}/scraper/executar", json={'strategy': 'smart_update'})
            print(f"Start Response: {resp.status_code}")
            print(resp.text)
            
            if resp.status_code != 200:
                print("FAILED TO START")
                return

    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    # 3. Monitor
    print("Monitoring progress for 5 seconds...")
    for _ in range(5):
        try:
            resp = requests.get(f"{BASE_URL}/scraper/progress")
            print(resp.json())
            time.sleep(1)
        except:
            pass

if __name__ == "__main__":
    verify_scraper()
