"""
INVESTIGACAO COMPLETA - BUSCAR TODOS OS 554 PRODUTOS
Testar todos os metodos possiveis para obter listagem completa
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://calientelingerie.com.br',
    'Referer': 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
}

print("="*80)
print("INVESTIGACAO COMPLETA - METODOS PARA OBTER TODOS OS 554 PRODUTOS")
print("="*80)

# ============================================================================
# METODO 1: TESTAR PARAMETROS DE PAGINACAO NA API
# ============================================================================
print("\n[METODO 1] Testando parametros de paginacao na API...")
print("-"*80)

parametros_teste = [
    # Testar limites maiores
    {'acao': 'sugestao_produto', 'busca': '', 'limit': 100},
    {'acao': 'sugestao_produto', 'busca': '', 'limit': 500},
    {'acao': 'sugestao_produto', 'busca': '', 'limit': 1000},
    {'acao': 'sugestao_produto', 'busca': '', 'per_page': 100},
    {'acao': 'sugestao_produto', 'busca': '', 'per_page': 500},

    # Testar offset/page
    {'acao': 'sugestao_produto', 'busca': '', 'offset': 0, 'limit': 100},
    {'acao': 'sugestao_produto', 'busca': '', 'page': 1, 'per_page': 100},
    {'acao': 'sugestao_produto', 'busca': '', 'start': 0, 'length': 100},

    # Testar todos os produtos
    {'acao': 'sugestao_produto', 'busca': '', 'all': 'true'},
    {'acao': 'sugestao_produto', 'busca': '', 'show_all': 'true'},
    {'acao': 'sugestao_produto', 'busca': '', 'mostrar_todos': 'true'},
]

for i, params in enumerate(parametros_teste, 1):
    try:
        response = requests.post(BASE_URL, headers=HEADERS, data=params, timeout=15)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"  Teste {i:2d}: {str(params):60s} -> {len(data)} produtos")
                    if len(data) > 8:
                        print(f"           ** SUCESSO! Retornou mais que 8 produtos! **")
                elif isinstance(data, dict):
                    print(f"  Teste {i:2d}: {str(params):60s} -> Dict com chaves: {list(data.keys())}")
            except:
                print(f"  Teste {i:2d}: {str(params):60s} -> Resposta nao-JSON")
        time.sleep(0.3)
    except Exception as e:
        print(f"  Teste {i:2d}: Erro - {str(e)[:50]}")

# ============================================================================
# METODO 2: TESTAR DIFERENTES ACOES NA API
# ============================================================================
print("\n[METODO 2] Testando diferentes acoes na API...")
print("-"*80)

acoes_teste = [
    'listar_produtos',
    'lista_produtos',
    'produtos',
    'get_produtos',
    'all_produtos',
    'buscar_produtos',
    'catalogo',
    'listagem',
    'produtos_todos',
    'produto_lista'
]

for acao in acoes_teste:
    try:
        params = {'acao': acao, 'busca': ''}
        response = requests.post(BASE_URL, headers=HEADERS, data=params, timeout=15)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print(f"  Acao '{acao}': {len(data)} produtos")
                    if len(data) > 8:
                        print(f"           ** SUCESSO! Retornou mais que 8 produtos! **")
                elif isinstance(data, dict):
                    print(f"  Acao '{acao}': Dict com chaves {list(data.keys())[:5]}")
            except:
                pass
        time.sleep(0.3)
    except:
        pass

# ============================================================================
# METODO 3: ANALISAR JAVASCRIPT E AJAX NO HTML
# ============================================================================
print("\n[METODO 3] Analisando JavaScript e chamadas AJAX no HTML...")
print("-"*80)

try:
    response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por scripts com URLs de API
    scripts = soup.find_all('script')
    print(f"  Total de scripts encontrados: {len(scripts)}")

    api_endpoints = set()
    ajax_patterns = [
        r'url:\s*["\']([^"\']*produto[^"\']*)["\']',
        r'ajax\(["\']([^"\']*)["\']',
        r'fetch\(["\']([^"\']*)["\']',
        r'\.post\(["\']([^"\']*)["\']',
        r'\.get\(["\']([^"\']*)["\']',
    ]

    for script in scripts:
        if script.string:
            for pattern in ajax_patterns:
                matches = re.findall(pattern, script.string, re.IGNORECASE)
                for match in matches:
                    if 'produto' in match.lower() or 'api' in match.lower():
                        api_endpoints.add(match)

    if api_endpoints:
        print(f"  Endpoints de API encontrados:")
        for endpoint in sorted(api_endpoints):
            print(f"    - {endpoint}")
    else:
        print("  Nenhum endpoint de API especifico encontrado nos scripts")

    # Procurar por arrays de produtos em JavaScript
    print("\n  Procurando arrays de produtos em JavaScript...")
    for i, script in enumerate(scripts):
        if script.string:
            # Procurar por grandes arrays JSON
            if 'var produtos' in script.string or 'let produtos' in script.string:
                produtos_match = re.search(r'(var|let|const)\s+produtos\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                if produtos_match:
                    try:
                        produtos_str = produtos_match.group(2)
                        # Tentar contar objetos
                        count = len(re.findall(r'\{[^}]*"id"[^}]*\}', produtos_str))
                        print(f"    Script {i}: Array 'produtos' com ~{count} items")
                        if count > 100:
                            print(f"    ** POSSIVEL LISTA COMPLETA ENCONTRADA! **")
                    except:
                        pass

except Exception as e:
    print(f"  Erro: {e}")

# ============================================================================
# METODO 4: TESTAR BUSCA POR WILDCARD E CARACTERES ESPECIAIS
# ============================================================================
print("\n[METODO 4] Testando wildcards e caracteres especiais...")
print("-"*80)

wildcards_teste = [
    '%',      # SQL wildcard
    '*',      # Wildcard comum
    '.*',     # Regex wildcard
    '%%',     # Double wildcard
    '**',
    '_',      # SQL single char
    ' ',      # Espaco vazio
    '  ',     # Multiplos espacos
]

for wildcard in wildcards_teste:
    try:
        params = {'acao': 'sugestao_produto', 'busca': wildcard}
        response = requests.post(BASE_URL, headers=HEADERS, data=params, timeout=15)
        data = response.json()
        if isinstance(data, list):
            print(f"  Busca '{wildcard}': {len(data)} produtos")
            if len(data) > 8:
                print(f"           ** SUCESSO! Retornou mais que 8 produtos! **")
        time.sleep(0.2)
    except:
        pass

# ============================================================================
# METODO 5: ANALISAR ESTRUTURA HTML PARA PAGINACAO
# ============================================================================
print("\n[METODO 5] Analisando estrutura HTML para sistema de paginacao...")
print("-"*80)

try:
    response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar por elementos de paginacao
    paginacao_classes = ['pagination', 'pager', 'page-numbers', 'page-link', 'paginate']
    encontrados = []

    for classe in paginacao_classes:
        elementos = soup.find_all(class_=re.compile(classe, re.I))
        if elementos:
            encontrados.extend(elementos)

    if encontrados:
        print(f"  Elementos de paginacao encontrados: {len(encontrados)}")
        for elem in encontrados[:10]:
            print(f"    - {elem.name}: {elem.get('class')} - Texto: {elem.get_text(strip=True)[:50]}")
    else:
        print("  Nenhum elemento de paginacao encontrado")

    # Procurar por data attributes que podem ter info de paginacao
    print("\n  Procurando data-attributes relacionados a produtos...")
    data_attrs = []
    for elem in soup.find_all(attrs={'data-total': True}):
        data_attrs.append(('data-total', elem.get('data-total')))
    for elem in soup.find_all(attrs={'data-count': True}):
        data_attrs.append(('data-count', elem.get('data-count')))
    for elem in soup.find_all(attrs={'data-produtos': True}):
        data_attrs.append(('data-produtos', elem.get('data-produtos')))

    if data_attrs:
        print(f"  Data attributes encontrados:")
        for attr, valor in data_attrs:
            print(f"    - {attr}: {valor}")
    else:
        print("  Nenhum data-attribute relevante encontrado")

except Exception as e:
    print(f"  Erro: {e}")

# ============================================================================
# METODO 6: TESTAR DIFERENTES HEADERS E USER AGENTS
# ============================================================================
print("\n[METODO 6] Testando se diferentes headers retornam mais dados...")
print("-"*80)

headers_variados = [
    # Mobile user agent
    {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'X-Requested-With': 'XMLHttpRequest'
    },
    # Bot/crawler user agent
    {
        'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
        'X-Requested-With': 'XMLHttpRequest'
    },
    # Sem User-Agent
    {
        'X-Requested-With': 'XMLHttpRequest'
    },
    # Com Accept especifico
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest'
    }
]

for i, headers_custom in enumerate(headers_variados, 1):
    try:
        params = {'acao': 'sugestao_produto', 'busca': ''}
        response = requests.post(BASE_URL, headers=headers_custom, data=params, timeout=15)
        data = response.json()
        if isinstance(data, list):
            user_agent = headers_custom.get('User-Agent', 'Sem UA')[:40]
            print(f"  Teste {i}: {user_agent}... -> {len(data)} produtos")
            if len(data) > 8:
                print(f"           ** SUCESSO! Retornou mais que 8 produtos! **")
        time.sleep(0.3)
    except:
        pass

# ============================================================================
# METODO 7: VERIFICAR SE EXISTE SITEMAP OU FEED DE PRODUTOS
# ============================================================================
print("\n[METODO 7] Verificando sitemap.xml e feeds de produtos...")
print("-"*80)

urls_teste = [
    'https://calientelingerie.com.br/sitemap.xml',
    'https://calientelingerie.com.br/sitemap_produtos.xml',
    'https://calientelingerie.com.br/produtos.xml',
    'https://calientelingerie.com.br/feed',
    'https://calientelingerie.com.br/produtos/feed',
    'https://calientelingerie.com.br/api/produtos',
    'https://calientelingerie.com.br/api/products',
    'https://calientelingerie.com.br/produtos.json',
]

for url in urls_teste:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print(f"  {url}")
            print(f"    -> Status: {response.status_code}, Tamanho: {len(response.content)} bytes")
            if 'xml' in url:
                # Contar URLs de produtos
                count = response.text.count('<loc>')
                print(f"    -> URLs encontradas: {count}")
        time.sleep(0.3)
    except:
        pass

# ============================================================================
# RESUMO E RECOMENDACOES
# ============================================================================
print("\n" + "="*80)
print("RESUMO DA INVESTIGACAO")
print("="*80)
print("""
OBJETIVO: Encontrar metodo para obter todos os 554 produtos da loja

METODOS TESTADOS:
1. Parametros de paginacao (limit, offset, page, per_page, all)
2. Acoes alternativas na API (listar_produtos, catalogo, etc)
3. Analise de JavaScript para endpoints ocultos
4. Wildcards e caracteres especiais na busca
5. Estrutura HTML e sistema de paginacao
6. Diferentes headers e user agents
7. Sitemaps e feeds XML/JSON

PROXIMOS PASSOS RECOMENDADOS:
- Se algum metodo acima retornou >8 produtos, implementar esse metodo
- Se nenhum funcionou, considerar:
  a) Expandir termos de busca (cores, tamanhos, estilos) para 80-90% cobertura
  b) Usar web scraping completo (Selenium) para scroll infinito
  c) Contatar fornecedor para API completa
  d) Aceitar cobertura atual de 49% (272 produtos)
""")
print("="*80)
