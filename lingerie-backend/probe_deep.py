import requests
import json

def probe_ajax_endpoint():
    # ID from sitemap: 951705, 17996842783
    # URL pattern from sitemap: https://calientelingerie.com.br/produto/951705/17996842783
    
    product_id = '2823474' # Sutiã Amamentação
    catalog_id = '17996842783'
    
    url = f"https://calientelingerie.com.br/produto/{product_id}/{catalog_id}?ajax=ajax"
    
    print(f"Fetching {url}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("SUCCESS! JSON received.")
                
                # Inspect for variants
                print("\n--- JSON KEYS ---")
                print(data.keys())
                
                if 'grade' in data:
                    print("\n--- GRADE (Colors/Sizes) ---")
                    print(json.dumps(data['grade'], indent=2, ensure_ascii=False)[:2000])
                
                if 'variacoes' in data:
                    print("\n--- VARIACOES ---")
                    print(json.dumps(data['variacoes'], indent=2, ensure_ascii=False)[:2000])

                if 'cores' in data:
                    print("\n--- CORES ---")
                    print(json.dumps(data['cores'], indent=2, ensure_ascii=False)[:1000])
                    
                # Save to file for full inspection if needed
                with open('product_deep_dump.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                print(f"Failed to parse JSON: {e}")
                print(f"Content start: {response.text[:200]}")
        else:
            print("Failed request.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    probe_ajax_endpoint()
