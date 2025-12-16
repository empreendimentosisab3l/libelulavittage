import requests
import time

url = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

print("=== ESTRATÉGIA BASEADA EM CATEGORIAS ===\n")

# TODAS as categorias encontradas no site + variações
categorias_completas = [
    # Categorias principais (do menu)
    'BABY DOLL',
    'Baby doll',
    'baby',
    'babydoll',

    'CONJUNTOS',
    'Conjuntos',
    'conjunto',

    'CALCINHAS',
    'Calcinhas',
    'calcinha',
    'fio dental',
    'tanga',

    'SUTIÃS',
    'Sutiãs',
    'sutia',
    'sutiã',
    'soutien',
    'top',

    'LINGERIE',
    'Lingerie',
    'lingerie',

    'Body',
    'body',

    'Plus Size',
    'plus size',
    'plus',
    'tamanho grande',

    'Pijama Longo',
    'Pijama de Inverno',
    'Pijama',
    'pijama',

    'Camisola + Robe',
    'Camisolas',
    'camisola',
    'robe',

    'Cropped',
    'Cropped Super LUXO',
    'cropped',

    'Cueca Boxer',
    'Cueca',
    'cueca',
    'boxer',

    # Materiais e estilos
    'renda',
    'rendado',
    'microfibra',
    'algodão',
    'algodao',
    'cetim',
    'seda',
    'lycra',

    # Estilos
    'sexy',
    'sensual',
    'conforto',
    'comfort',
    'básico',
    'basico',

    # Tipos específicos
    'espartilho',
    'corset',
    'cinta liga',
    'meia calça',
    'meia',

    # Ocasiões
    'noiva',
    'festa',
    'dia a dia',

    # KIT
    'kit',
    'conjunto promocional',
]

todos_produtos = {}
categorias_com_resultado = {}

print(f"Buscando em {len(categorias_completas)} termos de categoria...\n")

for i, categoria in enumerate(categorias_completas, 1):
    try:
        data = {'acao': 'sugestao_produto', 'busca': categoria}
        response = requests.post(url, headers=headers, data=data, timeout=15)
        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            novos_antes = len(todos_produtos)

            for produto in result:
                produto_id = produto.get('id')
                if produto_id and produto_id not in todos_produtos:
                    todos_produtos[produto_id] = produto

            novos_produtos = len(todos_produtos) - novos_antes
            categorias_com_resultado[categoria] = len(result)

            if novos_produtos > 0:
                print(f"{i:3d}. '{categoria}': {len(result)} produtos (+{novos_produtos} novos) | Total: {len(todos_produtos)}")
            else:
                print(f"{i:3d}. '{categoria}': {len(result)} produtos (duplicados)")

        time.sleep(0.25)  # Pausa para não sobrecarregar

    except Exception as e:
        print(f"{i:3d}. '{categoria}': ERRO - {str(e)[:50]}")

print(f"\n{'='*70}")
print(f"RESULTADO FINAL")
print(f"{'='*70}")
print(f"Total de termos buscados: {len(categorias_completas)}")
print(f"Termos com resultados: {len(categorias_com_resultado)}")
print(f"TOTAL DE PRODUTOS ÚNICOS: {len(todos_produtos)}")
print(f"{'='*70}\n")

# Análise por categoria real do produto
categorias_produtos = {}
for pid, prod in todos_produtos.items():
    cat = prod.get('categoria_nome', 'Sem categoria')
    categorias_produtos[cat] = categorias_produtos.get(cat, 0) + 1

print("Distribuição por Categoria Real:")
for cat, count in sorted(categorias_produtos.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat:.<40} {count:>3} produtos")

print(f"\nExemplos de produtos (primeiros 15):")
for i, (pid, prod) in enumerate(list(todos_produtos.items())[:15], 1):
    preco = prod.get('preco', 0)
    nome = prod.get('nome', 'N/A')[:50]
    cat = prod.get('categoria_nome', 'N/A')
    print(f"  {i:2d}. {nome:.<50} R$ {preco:>6.2f} ({cat})")

print(f"\n{'='*70}")
print(f"CONCLUSÃO:")
print(f"Com busca por categorias conseguimos {len(todos_produtos)} produtos únicos!")
print(f"{'='*70}")
