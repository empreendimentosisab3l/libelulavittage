import requests
from bs4 import BeautifulSoup
import re
import json

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scripts = soup.find_all('script')
    print(f"Found {len(scripts)} script tags.")
    
    for i, script in enumerate(scripts):
        if script.string:
            if 'preco' in script.string or 'nome' in script.string or 'products' in script.string:
                print(f"\n--- Script {i} content (first 500 chars) ---")
                print(script.string[:500])
                # Try to extract a JSON object
                # Look for something like: var products = [...] or window.products = [...]
                # or just a big list of objects
                
except Exception as e:
    print(f"Error: {e}")
