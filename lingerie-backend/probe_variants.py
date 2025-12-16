import requests
import json
import re

url_base = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# Known ID from previous probe
product_id = '2823474' # Sutiã Amamentação

def probe_api_details():
    print("--- Probing API for Details ---")
    actions = ['produto', 'get_produto', 'detalhe_produto', 'carregar_produto', 'produto_detalhes']
    
    for action in actions:
        try:
            data = {
                'acao': action,
                'produto_id': product_id,
                'id': product_id
            }
            print(f"Testing action: {action}")
            response = requests.post(url_base, headers=headers, data=data) 
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    # Check if it looks like a product detail
                    if isinstance(json_data, dict) and ('cores' in json_data or 'tamanhos' in json_data or 'variantes' in json_data):
                        print(f"SUCCESS with action '{action}'!")
                        print(json.dumps(json_data, indent=2, ensure_ascii=False)[:1000])
                        return
                    else:
                        print(f"Action '{action}' returned JSON but no obvious variants.")
                        # print(str(json_data)[:200])
                except:
                    pass
        except Exception as e:
            print(f"Error {e}")

def probe_html_page():
    print("\n--- Probing HTML Page for Variants ---")
    url = f"https://calientelingerie.com.br/produto/{product_id}/17996842783"
    try:
        response = requests.get(url, headers={'User-Agent': headers['User-Agent']})
        html = response.text
        
        # Look for JSON embedded in script tags
        # Common in Vue/React apps: window.__INITIAL_STATE__ or similar, or just props inside the component
        
        # Look for "cores" or "tamanhos"
        if 'cores' in html or 'tamanhos' in html:
            print("Found keyword 'cores' or 'tamanhos' in HTML.")
            
            # Try to find JSON structures
            # Regex for JSON-like objects containing "cores"
            # This is rough, but looking for variable assignments
            
            # Look for FZComponents.ProdutoConteudo(...) props
            matches = re.findall(r'produtoInicial\s*:\s*({.*?})', html, re.DOTALL)
            if matches:
                 print("Found 'produtoInicial' object?")
                 # It's likely not simple JSON parsing due to JS syntax (keys without quotes)
                 print(matches[0][:500])
            
            # Try to match a larger block of JSON-like data
            json_matches = re.findall(r'JSON\.parse\(\'(.*?)\'\)', html)
            for jm in json_matches:
                if 'cores' in jm:
                    print("Found JSON.parse with variants!")
                    # It might be escaped
                    try:
                        decoded = json.loads(jm.encode('utf-8').decode('unicode_escape'))
                        print(json.dumps(decoded, indent=2)[:500])
                    except:
                        print("Could not decode JSON.")

    except Exception as e:
        print(f"Error scraping HTML: {e}")

if __name__ == "__main__":
    probe_api_details()
    probe_html_page()
