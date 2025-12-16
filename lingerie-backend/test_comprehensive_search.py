import requests
import time
import string

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

todos_produtos = {}

print("=== ESTRATÉGIA COMPLETA: Alfabeto completo (a-z) + Números (0-9) ===\n")

# 1. Buscar por todas as letras do alfabeto
letras = string.ascii_lowercase
print("1. Buscando por letras individuais (a-z)...")
for letra in letras:
    try:
        data = {'acao': 'sugestao_produto', 'busca': letra}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto
            if len(result) > 0:
                print(f"  {letra}: {len(result)} produtos")
        time.sleep(0.3)  # Pausa para não sobrecarregar
    except Exception as e:
        print(f"  {letra}: Erro - {e}")

print(f"\nTotal após letras: {len(todos_produtos)} produtos únicos")

# 2. Buscar por números
print("\n2. Buscando por números (0-9)...")
for numero in range(10):
    try:
        data = {'acao': 'sugestao_produto', 'busca': str(numero)}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto
            if len(result) > 0:
                print(f"  {numero}: {len(result)} produtos")
        time.sleep(0.3)
    except Exception as e:
        print(f"  {numero}: Erro - {e}")

print(f"\nTotal após números: {len(todos_produtos)} produtos únicos")

# 3. Buscar por combinações de 2 letras (mais comuns)
print("\n3. Buscando combinações de 2 letras...")
combinacoes_comuns = [
    'ba', 'be', 'bi', 'bo', 'ca', 'ce', 'ci', 'co', 'da', 'de', 'di', 'do',
    'la', 'le', 'li', 'lo', 'ma', 'me', 'mi', 'mo', 'na', 'ne', 'ni', 'no',
    'pa', 'pe', 'pi', 'po', 'ra', 're', 'ri', 'ro', 'sa', 'se', 'si', 'so',
    'ta', 'te', 'ti', 'to', 'va', 've', 'vi', 'vo'
]

count_before = len(todos_produtos)
for combo in combinacoes_comuns:
    try:
        data = {'acao': 'sugestao_produto', 'busca': combo}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto
        time.sleep(0.2)
    except:
        pass

novos = len(todos_produtos) - count_before
print(f"  Novos produtos encontrados: {novos}")
print(f"\nTotal após combinações: {len(todos_produtos)} produtos únicos")

# 4. Categorias específicas conhecidas
print("\n4. Buscando por categorias conhecidas...")
categorias = [
    'conjunto', 'sutia', 'calcinha', 'lingerie', 'pijama', 'camisola',
    'body', 'baby doll', 'cueca', 'renda', 'cropped', 'microfibra',
    'rendado', 'sexy', 'conforto', 'cotton', 'plus size', 'soutien'
]

count_before = len(todos_produtos)
for categoria in categorias:
    try:
        data = {'acao': 'sugestao_produto', 'busca': categoria}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto
            if len(result) > 0:
                print(f"  {categoria}: {len(result)} produtos")
        time.sleep(0.3)
    except:
        pass

novos = len(todos_produtos) - count_before
print(f"  Novos produtos encontrados: {novos}")

print(f"\n{'='*60}")
print(f"TOTAL FINAL: {len(todos_produtos)} produtos únicos")
print(f"{'='*60}")

# Listar algumas categorias encontradas
categorias_produtos = {}
for pid, prod in todos_produtos.items():
    cat = prod.get('categoria_nome', 'Sem categoria')
    categorias_produtos[cat] = categorias_produtos.get(cat, 0) + 1

print("\nProdutos por categoria:")
for cat, count in sorted(categorias_produtos.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count} produtos")

print("\nExemplos de produtos (primeiros 10):")
for i, (pid, prod) in enumerate(list(todos_produtos.items())[:10]):
    print(f"  {i+1}. {prod.get('nome', 'N/A')} - R$ {prod.get('preco', 'N/A')} ({prod.get('categoria_nome', 'N/A')})")
