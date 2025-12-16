import requests
import json

def dump_full_json():
    # ID: 3507924 (Preto com Nude)
    url = "https://calientelingerie.com.br/produto/3507924/17996842783?ajax=ajax"
    headers = {'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest'}
    
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers)
    data = resp.json()
    
    # Save to file for reading
    with open('full_product_dump.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print("Dump saved to full_product_dump.json")
    
    # Also print keys to see structure
    print("Top level keys:", list(data.keys()))

if __name__ == "__main__":
    dump_full_json()
