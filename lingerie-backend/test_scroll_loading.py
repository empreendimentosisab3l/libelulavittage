import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("=== INVESTIGANDO COMO O SITE CARREGA PRODUTOS ===\n")

print("1. Analisando HTML inicial...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por dados embutidos no HTML
    scripts = soup.find_all('script')

    for i, script in enumerate(scripts):
        if script.string:
            # Procurar por arrays de produtos JavaScript
            if 'produtos' in script.string.lower() or 'items' in script.string.lower():
                # Tentar extrair JSON de arrays
                content = script.string

                # Procurar por padrões como: var produtos = [...] ou produtos: [...]
                patterns = [
                    r'produtos\s*[=:]\s*(\[.*?\])',
                    r'items\s*[=:]\s*(\[.*?\])',
                    r'products\s*[=:]\s*(\[.*?\])',
                    r'data\s*[=:]\s*(\[.*?\])',
                ]

                for pattern in patterns:
                    matches = re.search(pattern, content, re.DOTALL)
                    if matches:
                        try:
                            json_str = matches.group(1)
                            # Limitar tamanho para análise
                            if len(json_str) > 1000:
                                print(f"\n✓ Script {i}: Encontrado array grande (possível lista de produtos)")
                                print(f"  Tamanho: {len(json_str)} caracteres")
                                print(f"  Padrão: {pattern}")
                                # Tentar parsear
                                try:
                                    data = json.loads(json_str)
                                    if isinstance(data, list):
                                        print(f"  ✓ Array JSON válido com {len(data)} items")
                                        if len(data) > 0 and isinstance(data[0], dict):
                                            print(f"  Exemplo de chaves: {list(data[0].keys())[:5]}")
                                except:
                                    print(f"  JSON inválido, pode precisar limpeza")
                        except:
                            pass

except Exception as e:
    print(f"Erro: {e}")

print("\n2. Procurando por endpoints de API no HTML...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')

    endpoints_encontrados = set()

    for script in scripts:
        if script.string:
            # Procurar por URLs de API
            urls = re.findall(r'["\']([^"\']*(?:api|produto|listar|catalogo)[^"\']*)["\']', script.string, re.I)
            for url_found in urls:
                if '/' in url_found and len(url_found) > 5:
                    endpoints_encontrados.add(url_found)

    if endpoints_encontrados:
        print("Possíveis endpoints encontrados:")
        for endpoint in list(endpoints_encontrados)[:10]:
            print(f"  - {endpoint}")
    else:
        print("Nenhum endpoint específico encontrado")

except Exception as e:
    print(f"Erro: {e}")

print("\n3. Testando endpoint com parâmetros de paginação...")
test_params = [
    {},
    {'page': '1'},
    {'pagina': '1'},
    {'offset': '0', 'limit': '100'},
    {'all': 'true'},
    {'listar': 'todos'},
]

for params in test_params:
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            # Contar quantos produtos aparecem no HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Procurar por elementos que parecem produtos
            # Comum: divs com classes como 'product', 'item', 'card'
            possible_products = soup.find_all(['div', 'article'], class_=re.compile(r'(product|item|card)', re.I))

            if possible_products:
                print(f"Parâmetros {params}: {len(possible_products)} possíveis containers de produtos")
    except:
        pass

print("\n4. Procurando TODAS as categorias no menu/HTML...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por menus, navegação, links de categoria
    categorias_encontradas = set()

    # Estratégia 1: Links no menu
    nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=re.compile(r'(menu|nav|categ)', re.I))
    for nav in nav_elements:
        links = nav.find_all('a')
        for link in links:
            texto = link.get_text(strip=True)
            if texto and 3 < len(texto) < 50:
                categorias_encontradas.add(texto)

    # Estratégia 2: Procurar em todo o HTML por termos comuns
    all_text = soup.get_text()
    palavras_chave = ['Lingerie', 'Conjunto', 'Baby', 'Sutiã', 'Calcinha', 'Pijama',
                      'Camisola', 'Body', 'Cropped', 'Plus Size', 'Cueca']

    print("Categorias encontradas no site:")
    categorias_unicas = []
    for cat in sorted(categorias_encontradas):
        # Filtrar apenas categorias relevantes
        if any(palavra.lower() in cat.lower() for palavra in palavras_chave):
            categorias_unicas.append(cat)
            print(f"  - {cat}")

    print(f"\nTotal de categorias identificadas: {len(categorias_unicas)}")

except Exception as e:
    print(f"Erro: {e}")

print("\n5. Testando busca por categorias identificadas...")
categorias_teste = [
    'Baby doll', 'Conjuntos', 'Lingerie', 'Plus Size', 'Calcinhas',
    'Sutiãs', 'Pijama', 'Camisolas', 'Cropped', 'Body', 'Cueca'
]

total_por_categoria = {}
headers_api = headers.copy()
headers_api['X-Requested-With'] = 'XMLHttpRequest'

for categoria in categorias_teste:
    try:
        data = {'acao': 'sugestao_produto', 'busca': categoria}
        response = requests.post(url, headers=headers_api, data=data, timeout=15)
        result = response.json()
        if isinstance(result, list):
            total_por_categoria[categoria] = len(result)
            print(f"  {categoria}: {len(result)} produtos")
    except:
        pass

print(f"\n{'='*60}")
print("RESUMO DA INVESTIGAÇÃO")
print(f"{'='*60}")
print(f"Total de categorias testadas: {len(categorias_teste)}")
print(f"Total de produtos por categoria (máx 8 cada): {sum(total_por_categoria.values())}")
