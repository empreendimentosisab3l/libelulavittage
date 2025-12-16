import requests

def probe():
    url = "http://localhost:5001/api/scraper/progress"
    print(f"Probing {url}...")
    try:
        resp = requests.get(url, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    probe()
