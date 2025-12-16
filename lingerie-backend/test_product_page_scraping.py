"""
TESTAR SCRAPING DE PAGINA INDIVIDUAL DE PRODUTO
Vamos tentar extrair dados de uma pagina de produto para ver se funciona
"""
import requests
from bs4 import BeautifulSoup
import json
import re

print("="*80)
print("TESTANDO SCRAPING DE PAGINA INDIVIDUAL DE PRODUTO")
print("="*80)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

# Ler alguns IDs de produtos para testar
with open('produto_ids.txt', 'r') as f:
    produto_ids = f.read().splitlines()

print(f"\nTotal de IDs disponíveis: {len(produto_ids)}")
print(f"Vamos testar com os primeiros 3 produtos...\n")

produtos_extraidos = []

for i, produto_id in enumerate(produto_ids[:3], 1):
    print(f"\n{'='*80}")
    print(f"PRODUTO {i}/3 - ID: {produto_id}")
    print(f"{'='*80}")

    url = f"https://calientelingerie.com.br/produto/{produto_id}/17996842783"
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            produto_dados = {
                'id': produto_id,
                'url': url
            }

            # 1. EXTRAIR NOME DO PRODUTO
            # Procurar em diferentes lugares comuns
            nome = None

            # Tentar h1
            h1 = soup.find('h1')
            if h1:
                nome = h1.get_text(strip=True)

            # Tentar meta og:title
            if not nome:
                og_title = soup.find('meta', property='og:title')
                if og_title:
                    nome = og_title.get('content')

            # Tentar title
            if not nome:
                title = soup.find('title')
                if title:
                    nome = title.get_text(strip=True)

            produto_dados['nome'] = nome
            print(f"  Nome: {nome}")

            # 2. EXTRAIR PRECO
            preco = None

            # Procurar por padrões de preço
            preco_patterns = [
                r'R\$\s*(\d+[.,]\d{2})',
                r'preco["\']?\s*:\s*["\']?(\d+[.,]\d{2})',
                r'"price"\s*:\s*"?(\d+\.?\d*)"?',
            ]

            for pattern in preco_patterns:
                match = re.search(pattern, response.text)
                if match:
                    preco_str = match.group(1).replace(',', '.')
                    preco = float(preco_str)
                    break

            # Tentar meta og:price
            if not preco:
                og_price = soup.find('meta', property='og:price:amount')
                if og_price:
                    preco = float(og_price.get('content'))

            produto_dados['preco'] = preco
            print(f"  Preço: R$ {preco:.2f}" if preco else "  Preço: Não encontrado")

            # 3. EXTRAIR CATEGORIA
            categoria = None

            # Procurar breadcrumbs
            breadcrumb = soup.find('nav', class_=re.compile(r'breadcrumb', re.I))
            if breadcrumb:
                links = breadcrumb.find_all('a')
                if len(links) > 1:
                    categoria = links[-1].get_text(strip=True)

            produto_dados['categoria'] = categoria
            print(f"  Categoria: {categoria}" if categoria else "  Categoria: Não encontrada")

            # 4. EXTRAIR IMAGENS
            imagens = []

            # Procurar og:image
            og_images = soup.find_all('meta', property='og:image')
            for og_img in og_images:
                img_url = og_img.get('content')
                if img_url and img_url not in imagens:
                    imagens.append(img_url)

            # Procurar imagens em galeria/slider
            img_tags = soup.find_all('img', src=re.compile(r'produto|product', re.I))
            for img in img_tags:
                img_url = img.get('src')
                if img_url and img_url not in imagens:
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = 'https://calientelingerie.com.br' + img_url
                    imagens.append(img_url)

            produto_dados['imagens'] = imagens[:5]  # Limitar a 5 imagens
            print(f"  Imagens encontradas: {len(imagens)}")
            if imagens:
                for idx, img in enumerate(imagens[:3], 1):
                    print(f"    {idx}. {img[:80]}...")

            # 5. PROCURAR POR JSON-LD (dados estruturados)
            print("\n  Procurando por dados estruturados (JSON-LD)...")
            scripts_json = soup.find_all('script', type='application/ld+json')
            for script in scripts_json:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        # Verificar se é um Product
                        if data.get('@type') == 'Product':
                            print(f"    ** JSON-LD Product encontrado! **")
                            print(f"    Nome: {data.get('name')}")
                            print(f"    Descrição: {data.get('description', '')[:80]}...")
                            if 'offers' in data:
                                offers = data['offers']
                                if isinstance(offers, dict):
                                    print(f"    Preço: {offers.get('price')} {offers.get('priceCurrency')}")

                            # Usar dados do JSON-LD se disponíveis
                            if not nome and data.get('name'):
                                produto_dados['nome'] = data.get('name')
                            if not preco and 'offers' in data:
                                offers = data['offers']
                                if isinstance(offers, dict) and 'price' in offers:
                                    produto_dados['preco'] = float(offers['price'])
                            if 'image' in data:
                                imgs = data['image'] if isinstance(data['image'], list) else [data['image']]
                                for img in imgs:
                                    if img not in produto_dados['imagens']:
                                        produto_dados['imagens'].append(img)
                except:
                    pass

            produtos_extraidos.append(produto_dados)

    except Exception as e:
        print(f"  Erro: {e}")
        import traceback
        traceback.print_exc()

# RESUMO
print("\n" + "="*80)
print("RESUMO DO TESTE")
print("="*80)

print(f"\nProdutos testados: {len(produtos_extraidos)}")
print(f"\nDados extraídos:")
for i, prod in enumerate(produtos_extraidos, 1):
    print(f"\n  Produto {i}:")
    print(f"    ID: {prod.get('id')}")
    print(f"    Nome: {prod.get('nome')}")
    print(f"    Preço: R$ {prod.get('preco'):.2f}" if prod.get('preco') else "    Preço: N/A")
    print(f"    Categoria: {prod.get('categoria', 'N/A')}")
    print(f"    Imagens: {len(prod.get('imagens', []))}")

print("\n" + "="*80)
print("CONCLUSAO")
print("="*80)
print(f"""
RESULTADO: {"SUCESSO" if produtos_extraidos else "FALHA"}

Se conseguimos extrair dados das paginas de produtos:
- Podemos criar um scraper que percorre todos os {len(produto_ids)} IDs
- Isso garantiria 100% de cobertura da loja
- Precisaríamos adicionar delays entre requests (0.5-1s) para não sobrecarregar
- Estimativa de tempo: ~{len(produto_ids) * 0.5 / 60:.0f}-{len(produto_ids) * 1 / 60:.0f} minutos para scraper completo

PROXIMOS PASSOS:
1. Implementar scraper completo usando os IDs do sitemap
2. Adicionar sistema de retry para erros
3. Salvar progresso periodicamente
4. Usar multiprocessing/threading para acelerar (com cuidado)
""")
print("="*80)
