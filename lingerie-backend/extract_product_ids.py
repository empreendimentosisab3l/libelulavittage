"""
EXTRAIR IDS UNICOS DE PRODUTOS DO SITEMAP
Descobrimos que o sitemap tem URLs de produtos individuais!
Vamos extrair os IDs unicos e verificar quantos produtos existem
"""
import re
from collections import Counter

print("="*80)
print("EXTRAINDO IDS UNICOS DE PRODUTOS DO SITEMAP")
print("="*80)

# Ler arquivo com todas as URLs
with open('produto_urls.txt', 'r', encoding='utf-8') as f:
    urls = f.read().splitlines()

print(f"\nTotal de URLs no arquivo: {len(urls)}")

# Extrair IDs de produtos
# Padrão: /produto/186114 ou /produto/186114/17996842783
produto_ids = set()

for url in urls:
    # Procurar por /produto/NUMERO
    match = re.search(r'/produto/(\d+)', url)
    if match:
        produto_id = match.group(1)
        produto_ids.add(produto_id)

print(f"IDs unicos de produtos encontrados: {len(produto_ids)}")

# Salvar IDs em arquivo
with open('produto_ids.txt', 'w', encoding='utf-8') as f:
    for prod_id in sorted(produto_ids):
        f.write(f"{prod_id}\n")

print(f"Arquivo salvo: produto_ids.txt")

# Mostrar exemplos
print(f"\nExemplos de IDs (primeiros 20):")
for prod_id in sorted(produto_ids)[:20]:
    print(f"  - {prod_id}")

print("\n" + "="*80)
print("DESCOBERTA IMPORTANTE!")
print("="*80)
print(f"""
Encontramos {len(produto_ids)} IDs UNICOS de produtos no sitemap!

Isso significa que:
1. Sabemos EXATAMENTE quantos produtos existem na loja
2. Temos o ID de CADA produto
3. Podemos usar esses IDs para buscar na API!

PROXIMA ESTRATEGIA:
- Testar se a API aceita busca por ID de produto
- Ou acessar cada pagina de produto diretamente para scraper os dados
- Com isso conseguiremos 100% de cobertura!

URLs de produto seguem o padrao:
  https://calientelingerie.com.br/produto/[ID]
  ou
  https://calientelingerie.com.br/produto/[ID]/17996842783
""")
print("="*80)
