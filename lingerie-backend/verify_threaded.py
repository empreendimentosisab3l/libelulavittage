from verify_scraper import verify_scraper
from src.routes.scraper import SCRAPER_PROGRESS
import time
import threading

def monitor_progress():
    while True:
        print(f"PROGRESS: {SCRAPER_PROGRESS}")
        if SCRAPER_PROGRESS['status'] in ['success', 'error', 'stopped']:
            break
        time.sleep(2)

if __name__ == "__main__":
    # Start monitor in backgroud
    t = threading.Thread(target=monitor_progress)
    t.daemon = True
    t.start()
    
    print("Iniciando verificação do Scraper Multi-thread...")
    # This calls the route or function? calling function directly is hard because of app_context
    # Let's call via API or just reuse verify_sitemap.py?
    
    # Better to use verify_sitemap.py as it calls the API.
    print("Use verify_sitemap.py instead.")
