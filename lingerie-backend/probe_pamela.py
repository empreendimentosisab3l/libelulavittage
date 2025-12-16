import requests
import json

def probe_pamela_details():
    # ID from search: 3507924
    url = "https://calientelingerie.com.br/produto/3507924/17996842783?ajax=ajax"
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers)
    data = resp.json()
    
    print("\n--- VARIATIONS ---")
    variacoes = data.get('variacoes', {})
    print(json.dumps(variacoes, indent=2))
    
    print("\n--- NAME ---")
    print(data.get('nome'))

if __name__ == "__main__":
    probe_pamela_details()
