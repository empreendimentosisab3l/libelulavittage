import requests
import time
import json

BASE_URL = 'http://localhost:5000'

def verify_smart_update():
    print("--- Verifying Smart Update Strategy ---")
    
    # 1. Trigger Scraper
    print("Triggering scraper with strategy='smart_update'...")
    try:
        resp = requests.post(f"{BASE_URL}/scraper/executar", json={'strategy': 'smart_update'})
        print(f"Start Response: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Failed to start: {e}")
        return

    # 2. Poll Progress
    print("\nPolling progress (watching for 'Smart' in message)...")
    for _ in range(20): # Poll for 20 seconds
        try:
            resp = requests.get(f"{BASE_URL}/scraper/progress")
            if resp.status_code == 200:
                data = resp.json()
                status = data.get('status')
                pct = data.get('percentage')
                msg = data.get('message')
                
                print(f"[{status}] {pct}% - {msg}")
                
                if "Smart" in msg:
                    print("\nSUCCESS: 'Smart' tag found in progress message!")
                    # Check if skipping is happening (might be 0 if DB is empty of details)
                    if "pulados" in msg:
                         print("Skipping logic is active.")
                    return
                
                if status == 'completed':
                    print("Completed before seeing Smart tag (fast run?)")
                    return
                
                if status == 'error':
                    print("Scraper reported error.")
                    return
            
            time.sleep(1)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(1)

    print("\nTimeout waiting for Smart tag.")

if __name__ == "__main__":
    verify_smart_update()
