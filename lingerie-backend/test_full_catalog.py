import requests
import json

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

print("=== TESTE 1: Busca vazia (pode retornar tudo) ===")
try:
    data = {'acao': 'sugestao_produto', 'busca': ''}
    response = requests.post(url, headers=headers, data=data, timeout=15)
    result = response.json()
    print(f"Total produtos com busca vazia: {len(result) if isinstance(result, list) else 'N/A'}")
    if isinstance(result, list) and len(result) > 0:
        print(f"Exemplo: {result[0].get('nome', 'N/A')}")
except Exception as e:
    print(f"Erro: {e}")

print("\n=== TESTE 2: Busca com '*' (wildcard) ===")
try:
    data = {'acao': 'sugestao_produto', 'busca': '*'}
    response = requests.post(url, headers=headers, data=data, timeout=15)
    result = response.json()
    print(f"Total produtos com '*': {len(result) if isinstance(result, list) else 'N/A'}")
except Exception as e:
    print(f"Erro: {e}")

print("\n=== TESTE 3: Busca com '%' (SQL wildcard) ===")
try:
    data = {'acao': 'sugestao_produto', 'busca': '%'}
    response = requests.post(url, headers=headers, data=data, timeout=15)
    result = response.json()
    print(f"Total produtos com '%': {len(result) if isinstance(result, list) else 'N/A'}")
except Exception as e:
    print(f"Erro: {e}")

print("\n=== TESTE 4: Busca por letras comuns ===")
letras = ['a', 'e', 'i', 'o', 'u']
produtos_por_letra = {}
for letra in letras:
    try:
        data = {'acao': 'sugestao_produto', 'busca': letra}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            produtos_por_letra[letra] = len(result)
            print(f"Letra '{letra}': {len(result)} produtos")
    except:
        pass

print("\n=== TESTE 5: Verificar se existe paginacao ou limit ===")
try:
    # Tentar passar parametros de paginacao
    data = {
        'acao': 'sugestao_produto',
        'busca': 'conjunto',
        'limit': 1000,
        'page': 1
    }
    response = requests.post(url, headers=headers, data=data, timeout=15)
    result = response.json()
    print(f"Com limit=1000: {len(result) if isinstance(result, list) else 'N/A'} produtos")
except Exception as e:
    print(f"Erro: {e}")

print("\n=== TESTE 6: Verificar outras acoes disponiveis ===")
acoes_teste = ['listar_produtos', 'todos_produtos', 'catalogo', 'produtos', 'all']
for acao in acoes_teste:
    try:
        data = {'acao': acao}
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"Acao '{acao}': {len(result) if isinstance(result, list) else type(result).__name__}")
    except:
        pass

print("\n=== TESTE 7: Listar categorias no HTML ===")
from bs4 import BeautifulSoup
try:
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por categorias ou menus
    links = soup.find_all('a', href=True)
    categorias = set()
    for link in links:
        texto = link.get_text(strip=True)
        if texto and len(texto) > 2 and len(texto) < 30:
            categorias.add(texto)

    print(f"Possiveis categorias encontradas: {len(categorias)}")
    for cat in list(categorias)[:10]:
        print(f"  - {cat}")
except Exception as e:
    print(f"Erro: {e}")
