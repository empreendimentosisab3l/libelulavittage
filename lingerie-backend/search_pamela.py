import requests
import json

def search_pamela():
    url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {'acao': 'sugestao_produto', 'busca': 'Pamela'}
    
    resp = requests.post(url, headers=headers, data=data)
    try:
        items = resp.json()
        print(f"Items found: {len(items)}")
        for item in items:
            print(f"ID: {item.get('id')} - Nome: {item.get('nome')}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    search_pamela()
