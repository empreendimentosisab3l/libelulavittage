"""
TESTE RÁPIDO DA ESTRATÉGIA EXPANDIDA
Versão reduzida para teste rápido - apenas amostra de cada categoria
"""
import requests
import time
import string

print("="*80)
print("TESTE RÁPIDO - ESTRATÉGIA EXPANDIDA (AMOSTRA)")
print("="*80)

url_base = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

produtos_encontrados = {}

# Amostra de cada tipo de termo
termos_amostra = [
    # Categorias (10 amostras)
    'conjunto', 'calcinha', 'sutia', 'baby doll', 'body',
    'cropped', 'pijama', 'camisola', 'cueca', 'lingerie',

    # Cores (10 amostras)
    'preto', 'branco', 'vermelho', 'azul', 'rosa',
    'nude', 'verde', 'roxo', 'pink', 'bege',

    # Estilos (10 amostras)
    'renda', 'sexy', 'sensual', 'transparente', 'bojo',
    'push up', 'luxo', 'floral', 'liso', 'estampado',

    # Tecidos (5 amostras)
    'microfibra', 'algodão', 'cetim', 'lycra', 'renda francesa',

    # Tamanhos (5 amostras)
    'P', 'M', 'G', 'GG', 'plus size'
]

print(f"\nTestando {len(termos_amostra)} termos de amostra...")
print("(Nota: O scraper completo usará ~120 termos + alfabeto + números + combos)")

for i, termo in enumerate(termos_amostra, 1):
    try:
        data = {'acao': 'sugestao_produto', 'busca': termo}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            novos = 0
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item
                    novos += 1

            if novos > 0:
                print(f"  [{i:2d}/{len(termos_amostra)}] '{termo}': +{novos} novos | Total: {len(produtos_encontrados)}")

        time.sleep(0.3)
    except Exception as e:
        print(f"  Erro ao buscar '{termo}': {e}")

# Adicionar alfabeto completo (rápido)
print(f"\n+ Alfabeto (a-z)...")
for letra in string.ascii_lowercase:
    try:
        data = {'acao': 'sugestao_produto', 'busca': letra}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        time.sleep(0.2)
    except:
        pass

print(f"  Após alfabeto: {len(produtos_encontrados)} produtos")

# Adicionar números (rápido)
print(f"\n+ Números (0-9)...")
for num in range(10):
    try:
        data = {'acao': 'sugestao_produto', 'busca': str(num)}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        time.sleep(0.2)
    except:
        pass

print(f"  Após números: {len(produtos_encontrados)} produtos")

# Amostra de combinações
print(f"\n+ Amostra de combinações (20 de 90)...")
combos_amostra = ['ba', 'be', 'ca', 'co', 'da', 'de', 'la', 'le', 'ma', 'me',
                  'na', 'ne', 'pa', 'pe', 'ra', 're', 'sa', 'se', 'ta', 'te']

for combo in combos_amostra:
    try:
        data = {'acao': 'sugestao_produto', 'busca': combo}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        time.sleep(0.2)
    except:
        pass

print(f"  Após combos: {len(produtos_encontrados)} produtos")

# RESUMO
total_produtos = len(produtos_encontrados)
total_na_loja = 554
cobertura = (total_produtos / total_na_loja) * 100

print("\n" + "="*80)
print("RESUMO DO TESTE")
print("="*80)
print(f"\nRESULTADOS COM AMOSTRA:")
print(f"  Termos testados: {len(termos_amostra)} + alfabeto + números + 20 combos")
print(f"  Produtos únicos: {total_produtos}")
print(f"  Cobertura: {cobertura:.1f}%")

print(f"\nCOMPARAÇÃO:")
print(f"  Método anterior (140 termos): 272 produtos (49.1%)")
print(f"  Teste com amostra: {total_produtos} produtos ({cobertura:.1f}%)")

# Estimar resultado com scraper completo
termos_teste = len(termos_amostra) + 26 + 10 + 20  # amostra + alfabeto + números + combos
termos_completo = 120 + 26 + 10 + 90  # todos os termos
fator_multiplicador = termos_completo / termos_teste

estimativa = min(554, int(total_produtos * 1.2))  # Estimar 20% a mais com termos completos

print(f"\nESTIMATIVA COM SCRAPER COMPLETO:")
print(f"  Produtos esperados: ~{estimativa}")
print(f"  Cobertura esperada: ~{(estimativa/total_na_loja)*100:.1f}%")

if estimativa >= 440:  # 80% de 554
    status = "✓ META DE 80% ALCANÇÁVEL!"
    recomendacao = "Executar scraper completo - cobertura boa"
else:
    status = "⚠ Abaixo da meta de 80%"
    recomendacao = "Considerar método do sitemap para 100%"

print(f"\nSTATUS: {status}")
print(f"RECOMENDAÇÃO: {recomendacao}")

print("\n" + "="*80)
