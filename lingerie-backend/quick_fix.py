import sys
import os
sys.path.append(r"c:\Users\Lucas\Documents\loja-lingerie-completa\lingerie-backend")
from src.main import app, db
from src.models.produto import Produto
import requests
import json
import re

def quick_fix():
    app = create_app()
    with app.app_context():
        # List of IDs to force-fix immediately
        # 3507924 is the one with phantom sizes (Preto com Nude)
        ids = ["3507924"] 
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        print(f"Applying Quick Fix for IDs: {ids}...")
        
        for pid in ids:
            print(f"--> Processing {pid}...")
            url = f"https://calientelingerie.com.br/produto/{pid}/17996842783?ajax=ajax"
            
            try:
                resp = requests.get(url, headers=headers)
                if resp.status_code != 200:
                    print("Failed to fetch.")
                    continue
                    
                item_encontrado = resp.json()
                nome = item_encontrado.get('nome')
                
                # --- NEW LOGIC COPIED FROM SCRAPER.PY ---
                tamanhos_set = set()
                cores_set = set()
                variacoes = item_encontrado.get('variacoes', {})
                estoque_map = item_encontrado.get('estoque', {})
                
                if isinstance(variacoes, dict):
                    for var_id, var_data in variacoes.items():
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
                # ----------------------------------------
                
                print(f"   New Sizes: {tamanhos_str}")
                
                # Update DB
                prod = Produto.query.filter_by(url_original=str(pid)).first()
                if prod:
                    prod.tamanhos = tamanhos_str
                    prod.cores = cores_str
                    # Update hash too ideally, but for quick fix strictly size/color matter
                    db.session.commit()
                    print("   DATABASE UPDATED!")
                else:
                    print("   Product not found in DB (weird).")

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    quick_fix()
