import requests
import json
import re

def probe_logic():
    pid = "3507924"
    url = f"https://calientelingerie.com.br/produto/{pid}/17996842783?ajax=ajax"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"Fetching {url}...")
    resp = requests.get(url, headers=headers)
    item_encontrado = resp.json()
    
    # --- LOGIC START ---
    nome = item_encontrado.get('nome')
    
    # Variants
    tamanhos_set = set()
    cores_set = set()
    
    variacoes = item_encontrado.get('variacoes', {})
    estoque_map = item_encontrado.get('estoque', {})
    
    print(f"Estoque Map Keys: {list(estoque_map.keys())}")
    
    if isinstance(variacoes, dict):
        for var_id, var_data in variacoes.items():
            # Check stock in the root 'estoque' map first
            stock_real = 0
            
            # DEBUG: Print logic for EG (125147)
            if var_id == "125147":
                print(f"--- DEBUG VAR {var_id} (EG) ---")
                print(f"In Estoque Map? {var_id in estoque_map}")
                if var_id in estoque_map:
                    print(f"Value in Estoque: {estoque_map[var_id]}")
            
            # Strict Logic
            stock_real = 0
            if estoque_map:
                 # Trust Estoque Map
                 stock_real = int(estoque_map.get(var_id, 0))
            else:
                 stock_real = int(var_data.get('total_produtos', '0'))

            if var_data.get('status') == "1" and stock_real > 0:
                var_nome = var_data.get('nome', '').strip()
                if var_data.get('cor'): cores_set.add(var_nome)
                elif var_nome.lower().startswith("tamanho "): tamanhos_set.add(var_nome[8:].strip())
                else: tamanhos_set.add(var_nome)
    
    match_cor = re.search(r'\((.*?)\)', nome)
    if match_cor and len(match_cor.group(1)) < 30:
        cores_set.add(match_cor.group(1))
    
    tamanhos_str = ', '.join(sorted(list(tamanhos_set)))
    cores_str = ', '.join(sorted(list(cores_set)))
    # --- LOGIC END ---
    
    print("-" * 20)
    print(f"RESULT TAMANHOS: {tamanhos_str}")
    print(f"RESULT CORES: {cores_str}")

if __name__ == "__main__":
    probe_logic()
