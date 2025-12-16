import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

print("=== ESTRATEGIA 1: Buscar produtos diretamente no HTML ===")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar scripts que contenham dados de produtos
    scripts = soup.find_all('script')
    for i, script in enumerate(scripts):
        if script.string and 'produtos' in script.string.lower():
            print(f"\n--- Script {i} ---")
            # Tentar extrair JSON
            script_content = script.string
            # Procurar por arrays ou objetos JSON
            json_matches = re.findall(r'\{[^{}]*"id"[^{}]*\}', script_content)
            if json_matches:
                print(f"Encontrados {len(json_matches)} possíveis objetos JSON")

except Exception as e:
    print(f"Erro: {e}")

print("\n=== ESTRATEGIA 2: Tentar endpoint de listagem completa ===")
endpoints_teste = [
    '/api/produtos',
    '/produtos',
    '/catalogo',
    '/listar',
    '/all',
    '?all=true',
    '?listar=1'
]

base_url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
for endpoint in endpoints_teste:
    try:
        test_url = base_url + endpoint
        response = requests.get(test_url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✓ {endpoint}: {len(data) if isinstance(data, list) else 'JSON object'}")
            except:
                print(f"  {endpoint}: HTML response ({len(response.text)} bytes)")
    except:
        pass

print("\n=== ESTRATEGIA 3: Buscar com combinacoes de 2 letras ===")
# Gerar todas as combinações de 2 letras mais comuns
combinacoes = []
vogais = 'aeiou'
consoantes = 'bcdfglmnprst'

# Vogal + Consoante e Consoante + Vogal
for v in vogais:
    for c in consoantes[:5]:  # Primeiras 5 consoantes
        combinacoes.append(v + c)
        combinacoes.append(c + v)

print(f"Testando {len(combinacoes)} combinações de 2 letras...")
todos_produtos = {}

for combo in combinacoes[:10]:  # Testar apenas 10 para ver se funciona
    try:
        data = {'acao': 'sugestao_produto', 'busca': combo}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto
    except:
        pass

print(f"Total de produtos únicos encontrados com combinações: {len(todos_produtos)}")

print("\n=== ESTRATEGIA 4: Buscar por numeros (0-9) ===")
for numero in range(10):
    try:
        data = {'acao': 'sugestao_produto', 'busca': str(numero)}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            print(f"Número {numero}: {len(result)} produtos")
            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto
    except:
        pass

print(f"\nTotal acumulado com números: {len(todos_produtos)}")

print("\n=== ESTRATEGIA 5: Verificar se existe paginacao no site ===")
try:
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por elementos de paginação
    paginacao = soup.find_all(['a', 'button'], text=re.compile(r'(próxima|anterior|página|\d+)', re.I))
    if paginacao:
        print(f"Elementos de paginação encontrados: {len(paginacao)}")
        for elem in paginacao[:5]:
            print(f"  - {elem.get_text(strip=True)}: {elem.get('href', elem.get('onclick', 'N/A'))}")
    else:
        print("Nenhum elemento de paginação encontrado")

except Exception as e:
    print(f"Erro: {e}")

print(f"\n=== RESUMO ===")
print(f"Total de produtos únicos coletados: {len(todos_produtos)}")
if todos_produtos:
    print("Exemplo de produtos encontrados:")
    for i, (pid, prod) in enumerate(list(todos_produtos.items())[:5]):
        print(f"  {i+1}. {prod.get('nome', 'N/A')} (ID: {pid})")
