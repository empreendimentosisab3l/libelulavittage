import requests

url = "https://calientelingerie.com.br/produtos/69010c56f3b89_jgN57DYL.webp"

print(f"Testing access to: {url}")

# 1. Test standard request (like a browser)
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    print(f"Status Code: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type')}")
    print(f"Content-Length: {resp.headers.get('Content-Length')}")
    
    if resp.status_code == 403:
        print("[!] 403 Forbidden - Likely Hotlinking Protection")
    elif resp.status_code == 404:
        print("[!] 404 Not Found - URL is wrong")
    elif resp.status_code == 200:
        print("[ok] Image is accessible directly.")
        
except Exception as e:
    print(f"Error: {e}")
