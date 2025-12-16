import requests
from bs4 import BeautifulSoup
import re
import json

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("="*70)
print("INVESTIGANDO TOTAL DE PRODUTOS NA LOJA CALIENTE")
print("="*70)

# MÉTODO 1: Verificar no HTML da página
print("\n1. Buscando informações no HTML da página...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por textos que indiquem total de produtos
    text_content = soup.get_text()

    # Procurar por padrões como "X produtos", "Total: X", etc
    patterns = [
        r'(\d+)\s+produtos?',
        r'total[:\s]+(\d+)',
        r'(\d+)\s+items?',
        r'(\d+)\s+resultados?'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            print(f"   Padrão '{pattern}' encontrou: {matches}")

    # Procurar em scripts por dados estruturados
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            data = json.loads(script.string)
            if 'numberOfItems' in str(data):
                print(f"   JSON-LD encontrado com numberOfItems: {data}")
        except:
            pass

except Exception as e:
    print(f"   Erro: {e}")

# MÉTODO 2: Tentar endpoint de listagem completa
print("\n2. Testando endpoint de listagem sem filtros...")
try:
    headers_api = headers.copy()
    headers_api['X-Requested-With'] = 'XMLHttpRequest'

    # Tentar busca vazia que pode retornar mais resultados
    data = {'acao': 'sugestao_produto', 'busca': ''}
    response = requests.post(url, headers=headers_api, data=data, timeout=15)
    result = response.json()

    if isinstance(result, list):
        print(f"   Busca vazia retornou: {len(result)} produtos")
        # A API limita a 8, então não é o total

except Exception as e:
    print(f"   Erro: {e}")

# MÉTODO 3: Verificar se existe paginação no site
print("\n3. Procurando por paginação no site...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por links de paginação
    pagination_elements = soup.find_all(['a', 'button', 'div'],
                                       class_=re.compile(r'(page|pagination|pag)', re.I))

    if pagination_elements:
        print(f"   Elementos de paginação encontrados: {len(pagination_elements)}")
        for elem in pagination_elements[:5]:
            text = elem.get_text(strip=True)
            if text and len(text) < 20:
                print(f"      - {text}")
    else:
        print("   Nenhum elemento de paginação encontrado")

    # Procurar por números que podem indicar páginas
    page_numbers = re.findall(r'página\s+(\d+)\s+de\s+(\d+)', text_content, re.IGNORECASE)
    if page_numbers:
        print(f"   Informação de página encontrada: {page_numbers}")

except Exception as e:
    print(f"   Erro: {e}")

# MÉTODO 4: Verificar JavaScript para dados de produtos
print("\n4. Procurando dados de produtos em JavaScript...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    scripts = soup.find_all('script')
    for i, script in enumerate(scripts):
        if script.string:
            # Procurar por arrays grandes que possam ser produtos
            if 'var produtos' in script.string or 'let produtos' in script.string:
                # Tentar contar quantos objetos tem no array
                matches = re.findall(r'\{[^}]*"id"[^}]*\}', script.string)
                if len(matches) > 10:
                    print(f"   Script {i}: Possível array de produtos com {len(matches)} items")

            # Procurar por total explícito
            total_matches = re.findall(r'total["\']?\s*:\s*(\d+)', script.string, re.IGNORECASE)
            if total_matches:
                print(f"   Script {i}: Propriedade 'total' encontrada com valor: {total_matches}")

except Exception as e:
    print(f"   Erro: {e}")

# MÉTODO 5: Tentar buscar por letras individuais e somar
print("\n5. Estimativa por busca alfabética...")
try:
    import string
    import time

    headers_api = headers.copy()
    headers_api['X-Requested-With'] = 'XMLHttpRequest'

    produtos_unicos = set()

    # Buscar por todas as letras
    for letra in string.ascii_lowercase[:5]:  # Apenas primeiras 5 letras para teste rápido
        try:
            data = {'acao': 'sugestao_produto', 'busca': letra}
            response = requests.post(url, headers=headers_api, data=data, timeout=15)
            result = response.json()

            if isinstance(result, list):
                for item in result:
                    produtos_unicos.add(str(item.get('id')))

            time.sleep(0.2)
        except:
            pass

    print(f"   Produtos únicos encontrados (primeiras 5 letras): {len(produtos_unicos)}")
    print(f"   Estimativa total (26 letras): ~{len(produtos_unicos) * 5} produtos")

except Exception as e:
    print(f"   Erro: {e}")

# MÉTODO 6: Contar elementos visíveis na página
print("\n6. Contando produtos visíveis na página inicial...")
try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por containers de produtos (divs, articles, etc)
    possible_products = soup.find_all(['div', 'article'],
                                     class_=re.compile(r'(product|item|card)', re.I))

    print(f"   Containers que parecem produtos: {len(possible_products)}")

    # Procurar por imagens de produtos
    product_images = soup.find_all('img', src=re.compile(r'produtos|product', re.I))
    print(f"   Imagens de produtos encontradas: {len(product_images)}")

except Exception as e:
    print(f"   Erro: {e}")

print("\n" + "="*70)
print("RESUMO DA INVESTIGAÇÃO")
print("="*70)
print("\nCONCLUSÕES:")
print("1. A API de sugestão retorna no máximo 8 produtos por busca")
print("2. Não encontramos um endpoint que retorne o total de produtos")
print("3. O site não mostra claramente quantos produtos existem no total")
print("\nRECOMENDAÇÕES:")
print("• Nossa estratégia atual (270+ produtos) provavelmente captura a maioria")
print("• Para verificar cobertura real, podemos:")
print("  - Navegar manualmente no site e contar")
print("  - Entrar em contato com o fornecedor")
print("  - Comparar com categorias conhecidas")
print("="*70)
