"""
TESTE COM IDS QUE SABEMOS QUE EXISTEM
Verificar que conseguimos scraper corretamente dados de produtos ativos
"""
import requests
from bs4 import BeautifulSoup
import re
import json

print("="*80)
print("TESTANDO SCRAPING COM IDS ATIVOS CONHECIDOS")
print("="*80)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# IDs que sabemos que existem (da nossa API)
ids_teste = ['3507924', '3507814', '3507684', '2414954', '2414718']

print(f"\nTestando {len(ids_teste)} produtos que sabemos que existem...\n")

produtos_extraidos = []

for i, produto_id in enumerate(ids_teste, 1):
    print(f"\n{' PRODUTO ' + str(i) + '/' + str(len(ids_teste)) + ' ':=^80}")
    print(f"ID: {produto_id}")

    url = f"https://calientelingerie.com.br/produto/{produto_id}/17996842783"
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            print(f"  Status {response.status_code} - Pulando...")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        produto_dados = {'id': produto_id, 'url': url}

        # NOME DO PRODUTO
        nome = None
        title_tag = soup.find('title')
        if title_tag:
            # Remove " - Caliente Lingerie" do final
            nome = title_tag.get_text(strip=True).replace(' - Caliente Lingerie', '').strip()

        produto_dados['nome'] = nome
        print(f"  Nome: {nome}")

        # PRECO - procurar em JSON-LD e no HTML
        preco = None

        # Procurar JSON-LD estruturado
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                if isinstance(data, dict) and data.get('@type') == 'Product':
                    if 'offers' in data:
                        offers = data['offers']
                        if isinstance(offers, dict) and 'price' in offers:
                            preco = float(offers['price'])
            except:
                pass

        # Se não encontrou no JSON-LD, procurar no HTML
        if not preco:
            # Procurar por elementos de preço comuns
            preco_elem = soup.find(class_=re.compile(r'(price|preco|valor)', re.I))
            if preco_elem:
                preco_text = preco_elem.get_text()
                match = re.search(r'R?\$?\s*(\d+[.,]\d{2})', preco_text)
                if match:
                    preco = float(match.group(1).replace(',', '.'))

        produto_dados['preco'] = preco
        print(f"  Preco: R$ {preco:.2f}" if preco else "  Preco: NAO ENCONTRADO")

        # CATEGORIA - procurar em breadcrumbs ou meta tags
        categoria = None

        # Tentar breadcrumbs
        breadcrumbs = soup.find_all('a', href=re.compile(r'/categoria/|/c/', re.I))
        if breadcrumbs:
            for bc in breadcrumbs:
                text = bc.get_text(strip=True)
                if text and text.lower() not in ['home', 'inicio', 'caliente', 'lingerie']:
                    categoria = text
                    break

        produto_dados['categoria'] = categoria
        print(f"  Categoria: {categoria}" if categoria else "  Categoria: NAO ENCONTRADA")

        # IMAGENS - procurar em og:image e galeria
        imagens = []

        # og:image
        og_imgs = soup.find_all('meta', property='og:image')
        for og in og_imgs:
            img_url = og.get('content')
            if img_url and 'logo' not in img_url.lower():
                if img_url not in imagens:
                    imagens.append(img_url)

        # Imagens da galeria de produtos
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            # Filtrar apenas imagens que parecem ser de produtos
            if any(x in src.lower() for x in ['produto', 'products', 'uploads']) and 'logo' not in src.lower():
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://calientelingerie.com.br' + src
                if src not in imagens:
                    imagens.append(src)

        produto_dados['imagens'] = imagens[:5]
        print(f"  Imagens: {len(imagens)} encontradas")
        if imagens:
            for idx, img in enumerate(imagens[:2], 1):
                print(f"    {idx}. {img[:70]}...")

        # DESCRICAO
        descricao = None
        desc_meta = soup.find('meta', attrs={'name': 'description'})
        if desc_meta:
            descricao = desc_meta.get('content', '').strip()

        if not descricao:
            desc_elem = soup.find(class_=re.compile(r'(description|descricao|detalhes)', re.I))
            if desc_elem:
                descricao = desc_elem.get_text(strip=True)[:500]

        produto_dados['descricao'] = descricao
        print(f"  Descricao: {descricao[:80]}..." if descricao else "  Descricao: NAO ENCONTRADA")

        produtos_extraidos.append(produto_dados)

    except Exception as e:
        print(f"  ERRO: {e}")

# RESUMO
print("\n" + "="*80)
print("RESUMO DOS TESTES")
print("="*80)

print(f"\nProdutos testados: {len(ids_teste)}")
print(f"Produtos extraidos com sucesso: {len(produtos_extraidos)}")

sucesso_campos = {
    'nome': sum(1 for p in produtos_extraidos if p.get('nome')),
    'preco': sum(1 for p in produtos_extraidos if p.get('preco')),
    'categoria': sum(1 for p in produtos_extraidos if p.get('categoria')),
    'imagens': sum(1 for p in produtos_extraidos if p.get('imagens')),
    'descricao': sum(1 for p in produtos_extraidos if p.get('descricao'))
}

print(f"\nTaxa de extracao por campo:")
for campo, count in sucesso_campos.items():
    taxa = (count / len(produtos_extraidos) * 100) if produtos_extraidos else 0
    print(f"  {campo:.<20} {count}/{len(produtos_extraidos)} ({taxa:.0f}%)")

print("\n" + "="*80)
print("CONCLUSAO E PROXIMOS PASSOS")
print("="*80)

if produtos_extraidos and sucesso_campos['nome'] > 0:
    print("""
RESULTADO: SUCESSO! Conseguimos scraper dados de produtos individuais!

ESTRATEGIA DEFINITIVA PARA 100% DE COBERTURA:
1. Usar os 3,748 IDs do sitemap
2. Para cada ID, acessar a pagina e extrair dados
3. Filtrar apenas produtos que tem nome (para evitar produtos inativos)
4. Salvar no banco de dados

ESTIMATIVA:
- Total de produtos: 3,748 IDs
- Produtos com dados válidos: ~600-800 (estimativa baseada na razão atual de 272/554)
- Tempo total: ~30-60 minutos (com delay de 0.5-1s por produto)
- Taxa de cobertura esperada: 100% dos produtos ativos

IMPLEMENTACAO:
- Adicionar ao scraper.py uma nova função que usa IDs do sitemap
- Incluir retry logic e tratamento de erros
- Salvar progresso periodicamente
- Mostrar barra de progresso
""")
else:
    print("""
RESULTADO: FALHA - Não conseguimos extrair dados suficientes

POSSÍVEIS PROBLEMAS:
- Estrutura HTML diferente do esperado
- Produtos inativos/removidos
- Necessário ajustar seletores CSS/parsing

RECOMENDACAO:
- Investigar manualmente a estrutura HTML de algumas paginas
- Ajustar o script de scraping
- Ou continuar usando a API com busca expandida por termos
""")

print("="*80)
