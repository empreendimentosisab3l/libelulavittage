import requests
import re
import json

def verify_extraction():
    produto_id = '2823474' # Sutiã Amamentação
    url_detalhes = f"https://calientelingerie.com.br/produto/{produto_id}/17996842783?ajax=ajax"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    print(f"Fetching {url_detalhes}...")
    try:
        response = requests.get(url_detalhes, headers=headers, timeout=15)
        item_encontrado = response.json()
        
        nome = item_encontrado.get('nome')
        print(f"Product: {nome}")
        
        # --- LOGIC FROM SCRAPER ---
        tamanhos_set = set()
        cores_set = set()
        
        variacoes = item_encontrado.get('variacoes', {})
        if isinstance(variacoes, dict):
            for var_id, var_data in variacoes.items():
                if var_data.get('status') == "1":
                    var_nome = var_data.get('nome', '').strip()
                    var_cor = var_data.get('cor')
                    
                    if var_cor:
                        cores_set.add(var_nome)
                    else:
                        if var_nome.startswith("Tamanho "):
                            tamanhos_set.add(var_nome.replace("Tamanho ", ""))
                        else:
                            tamanhos_set.add(var_nome)
        
        match_cor = re.search(r'\((.*?)\)', nome)
        if match_cor:
            provavel_cor = match_cor.group(1)
            if len(provavel_cor) < 20: 
                cores_set.add(provavel_cor)

        tamanhos_str = ', '.join(sorted(list(tamanhos_set)))
        cores_str = ', '.join(sorted(list(cores_set)))
        
        print(f"\nExtracted Sizes: {tamanhos_str}")
        print(f"Extracted Colors: {cores_str}")
        
        if tamanhos_str and cores_str:
            print("\nSUCCESS: Both sizes and colors extracted.")
        elif tamanhos_str:
             print("\nPARTIAL SUCCESS: Sizes extracted.")
        else:
             print("\nFAILURE: Nothing extracted.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_extraction()
