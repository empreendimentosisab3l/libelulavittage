import requests
import json

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
    'acao': 'sugestao_produto',
    'busca': 'sutiã'
}

try:
    print(f"Sending POST to {url} with search 'sutiã'...")
    response = requests.post(url, headers=headers, data=data) 
    response.raise_for_status()
    
    try:
        json_data = response.json()
        print("\n--- JSON RESPONSE ---")
        print(json.dumps(json_data, indent=2, ensure_ascii=False)[:2000]) # First 2000 chars
        print(f"\nTotal items: {len(json_data) if isinstance(json_data, list) else 'Not a list'}")
    except json.JSONDecodeError:
        print("\n--- RESPONSE TEXT (Not JSON) ---")
        print(response.text[:1000])

except Exception as e:
    print(f"Error: {e}")
