"""
TESTAR ESTRATÉGIA EXPANDIDA SEM SALVAR NO BANCO
Verificar quantos produtos conseguimos encontrar com os novos termos
"""
import requests
import time
import string

print("="*80)
print("TESTANDO ESTRATÉGIA EXPANDIDA - PREVIEW SEM SALVAR")
print("="*80)

url_base = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

produtos_encontrados = {}

# FASE 1: Categorias expandidas
categorias = [
    # Categorias principais
    'BABY DOLL', 'Baby doll', 'baby', 'babydoll',
    'CONJUNTOS', 'Conjuntos', 'conjunto',
    'CALCINHAS', 'Calcinhas', 'calcinha', 'fio dental', 'tanga',
    'SUTIÃS', 'Sutiãs', 'sutia', 'sutiã', 'soutien', 'top',
    'LINGERIE', 'Lingerie', 'lingerie',
    'Body', 'body',
    'Plus Size', 'plus size', 'plus', 'tamanho grande',
    'Pijama Longo', 'Pijama de Inverno', 'Pijama', 'pijama',
    'Camisola + Robe', 'Camisolas', 'camisola', 'robe',
    'Cropped', 'Cropped Super LUXO', 'cropped',
    'Cueca Boxer', 'Cueca', 'cueca', 'boxer',
    'espartilho', 'corset', 'cinta liga', 'meia calça', 'meia',
    'kit', 'conjunto promocional',

    # Cores
    'preto', 'branco', 'vermelho', 'azul', 'rosa', 'verde',
    'amarelo', 'roxo', 'laranja', 'nude', 'bege', 'cinza',
    'pink', 'lilás', 'coral', 'dourado', 'prateado',
    'bordô', 'vinho', 'marrom', 'turquesa',

    # Tamanhos
    'P', 'M', 'G', 'GG', 'XG', 'PP',
    'pequeno', 'medio', 'grande',

    # Estilos e características
    'renda', 'rendado', 'transparente', 'aveludado', 'estampado',
    'liso', 'floral', 'onça', 'leopardo', 'animal print',
    'bolinhas', 'listrado', 'xadrez',
    'bojo', 'sem bojo', 'meia taça', 'push up', 'aro',
    'sem aro', 'tomara que caia', 'frente unica',
    'sexy', 'sensual', 'conforto', 'comfort',
    'romântico', 'romantico', 'luxo', 'premium',
    'básico', 'basico', 'casual', 'noite', 'dia',

    # Tecidos
    'microfibra', 'algodão', 'algodao', 'cotton',
    'cetim', 'seda', 'lycra', 'elastano',
    'poliamida', 'viscose', 'nylon',
    'tule', 'renda francesa', 'guipir',

    # Ocasiões
    'noiva', 'casamento', 'lua de mel',
    'dia dos namorados', 'natal', 'ano novo',
    'inverno', 'verao', 'verão'
]

print(f"\nFase 1: Buscando por {len(categorias)} termos expandidos...")
termos_processados = 0
for termo in categorias:
    try:
        data = {'acao': 'sugestao_produto', 'busca': termo}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        termos_processados += 1
        if termos_processados % 20 == 0:
            print(f"  Processados {termos_processados}/{len(categorias)} termos - {len(produtos_encontrados)} produtos únicos até agora")

        time.sleep(0.25)
    except Exception as e:
        print(f"  Erro ao buscar '{termo}': {e}")
        continue

print(f"\nApós Fase 1 (termos expandidos): {len(produtos_encontrados)} produtos")

# FASE 2: Alfabeto
print(f"\nFase 2: Alfabeto (a-z)...")
for letra in string.ascii_lowercase:
    try:
        data = {'acao': 'sugestao_produto', 'busca': letra}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        time.sleep(0.2)
    except:
        continue

print(f"Após Fase 2 (alfabeto): {len(produtos_encontrados)} produtos")

# FASE 3: Números
print(f"\nFase 3: Números (0-9)...")
for numero in range(10):
    try:
        data = {'acao': 'sugestao_produto', 'busca': str(numero)}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        time.sleep(0.2)
    except:
        continue

print(f"Após Fase 3 (números): {len(produtos_encontrados)} produtos")

# FASE 4: Combinações de 2 letras
print(f"\nFase 4: Combinações de 2 letras expandidas...")
combinacoes = [
    'ba', 'be', 'bi', 'bo', 'bu', 'ca', 'ce', 'ci', 'co', 'cu',
    'da', 'de', 'di', 'do', 'du', 'fa', 'fe', 'fi', 'fo', 'fu',
    'ga', 'ge', 'gi', 'go', 'gu', 'ha', 'he', 'hi', 'ho', 'hu',
    'ja', 'je', 'ji', 'jo', 'ju', 'la', 'le', 'li', 'lo', 'lu',
    'ma', 'me', 'mi', 'mo', 'mu', 'na', 'ne', 'ni', 'no', 'nu',
    'pa', 'pe', 'pi', 'po', 'pu', 'ra', 're', 'ri', 'ro', 'ru',
    'sa', 'se', 'si', 'so', 'su', 'ta', 'te', 'ti', 'to', 'tu',
    'va', 've', 'vi', 'vo', 'vu', 'xa', 'xe', 'xi', 'xo', 'xu',
    'za', 'ze', 'zi', 'zo', 'zu'
]

combos_processados = 0
for combo in combinacoes:
    try:
        data = {'acao': 'sugestao_produto', 'busca': combo}
        response = requests.post(url_base, headers=headers, data=data, timeout=15)
        items = response.json()

        if isinstance(items, list):
            for item in items:
                if str(item.get('id')) not in produtos_encontrados:
                    produtos_encontrados[str(item.get('id'))] = item

        combos_processados += 1
        if combos_processados % 20 == 0:
            print(f"  Processados {combos_processados}/{len(combinacoes)} combos - {len(produtos_encontrados)} produtos únicos")

        time.sleep(0.2)
    except:
        continue

print(f"\nApós Fase 4 (combinações): {len(produtos_encontrados)} produtos")

# RESUMO FINAL
print("\n" + "="*80)
print("RESUMO DA ESTRATÉGIA EXPANDIDA")
print("="*80)

total_produtos = len(produtos_encontrados)
total_na_loja = 554  # Valor conhecido da investigação anterior

cobertura = (total_produtos / total_na_loja) * 100

print(f"\nRESULTADOS:")
print(f"  Total de termos de busca: {len(categorias) + 26 + 10 + len(combinacoes)}")
print(f"  Produtos únicos encontrados: {total_produtos}")
print(f"  Total na loja Caliente: {total_na_loja}")
print(f"  Cobertura alcançada: {cobertura:.1f}%")

print(f"\nCOMPARAÇÃO:")
print(f"  Método anterior: 272 produtos (49.1%)")
print(f"  Método expandido: {total_produtos} produtos ({cobertura:.1f}%)")
print(f"  Melhoria: +{total_produtos - 272} produtos (+{cobertura - 49.1:.1f}%)")

if cobertura >= 80:
    status = "EXCELENTE! Meta de 80-90% atingida!"
elif cobertura >= 70:
    status = "BOM! Próximo da meta"
elif cobertura >= 60:
    status = "RAZOÁVEL - Melhorou bastante"
else:
    status = "Precisa de mais termos"

print(f"\nSTATUS: {status}")

print("\n" + "="*80)
print("PRÓXIMOS PASSOS")
print("="*80)
print(f"""
1. Se a cobertura está boa (>80%), executar o scraper completo
2. Se ainda está baixa (<80%), considerar adicionar mais termos ou usar método do sitemap

Quer executar o scraper completo agora para salvar no banco de dados?
Acesse o painel admin: http://localhost:5000/admin
""")
print("="*80)
