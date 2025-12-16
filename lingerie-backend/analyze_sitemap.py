"""
ANALISE DO SITEMAP - EXTRAIR URLS DE PRODUTOS
Discovered: sitemap.xml has 22,620 URLs - let's extract product URLs
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

print("="*80)
print("ANALISANDO SITEMAP PARA ENCONTRAR URLS DE PRODUTOS")
print("="*80)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Baixar sitemap principal
print("\n[1] Baixando sitemap principal...")
sitemap_url = 'https://calientelingerie.com.br/sitemap.xml'

try:
    response = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    print(f"Status: {response.status_code}, Tamanho: {len(response.content):,} bytes")

    soup = BeautifulSoup(response.content, 'xml')

    # Procurar por sitemaps de produtos
    sitemap_indices = soup.find_all('sitemap')
    print(f"\n[2] Sitemaps encontrados no indice: {len(sitemap_indices)}")

    produtos_sitemap_url = None
    for sitemap in sitemap_indices:
        loc = sitemap.find('loc')
        if loc and 'produto' in loc.text.lower():
            print(f"  -> Sitemap de produtos: {loc.text}")
            produtos_sitemap_url = loc.text
            break

    # Se nao encontrou sitemap especifico, procurar URLs direto no sitemap principal
    if not produtos_sitemap_url:
        print("\n[3] Procurando URLs de produtos diretamente no sitemap principal...")
        urls = soup.find_all('loc')
        print(f"Total de URLs no sitemap: {len(urls)}")

        # Filtrar URLs que parecem ser de produtos
        produto_urls = []
        padroes_produto = [
            r'/produto/',
            r'/p/',
            r'/item/',
            r'-p-\d+',
            r'/\d+/',
        ]

        for url_tag in urls:
            url = url_tag.text
            # Verificar se URL parece ser de produto
            if any(re.search(padrao, url, re.I) for padrao in padroes_produto):
                produto_urls.append(url)

        print(f"\n[4] URLs de produtos encontradas: {len(produto_urls)}")

        if produto_urls:
            print("\nExemplos de URLs de produtos:")
            for url in produto_urls[:10]:
                print(f"  - {url}")

            print(f"\n[5] Analisando padroes das URLs...")
            # Analisar padroes
            padroes_contagem = {}
            for url in produto_urls:
                path = urlparse(url).path
                # Pegar primeira parte do path
                parts = [p for p in path.split('/') if p]
                if parts:
                    primeiro_segmento = parts[0]
                    padroes_contagem[primeiro_segmento] = padroes_contagem.get(primeiro_segmento, 0) + 1

            print("Padroes de URL encontrados:")
            for padrao, count in sorted(padroes_contagem.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  /{padrao}/... : {count} URLs")

            # Salvar todas as URLs de produtos em arquivo
            print(f"\n[6] Salvando URLs de produtos em arquivo...")
            with open('produto_urls.txt', 'w', encoding='utf-8') as f:
                for url in produto_urls:
                    f.write(f"{url}\n")
            print(f"Arquivo salvo: produto_urls.txt ({len(produto_urls)} URLs)")

    else:
        # Baixar sitemap especifico de produtos
        print(f"\n[3] Baixando sitemap especifico de produtos: {produtos_sitemap_url}")
        response = requests.get(produtos_sitemap_url, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.content, 'xml')

        urls = soup.find_all('loc')
        print(f"URLs de produtos encontradas: {len(urls)}")

        if urls:
            print("\nExemplos de URLs:")
            for url in urls[:10]:
                print(f"  - {url.text}")

            # Salvar todas as URLs
            print(f"\n[4] Salvando URLs de produtos em arquivo...")
            with open('produto_urls.txt', 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(f"{url.text}\n")
            print(f"Arquivo salvo: produto_urls.txt ({len(urls)} URLs)")

except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("PROXIMOS PASSOS")
print("="*80)
print("""
Se encontramos URLs de produtos no sitemap:
1. Podemos scraper cada URL individual para obter dados completos
2. Isso garantiria 100% de cobertura de todos os produtos da loja
3. Precisariamos extrair dados de cada pagina de produto (nome, preco, imagens, etc)

VANTAGENS:
+ Cobertura completa (100%)
+ Dados diretos da pagina do produto
+ Nao depende da API limitada

DESVANTAGENS:
- Mais lento (precisa acessar cada pagina)
- Mais requisicoes ao servidor
- Pode precisar de delays para nao sobrecarregar
""")
print("="*80)
