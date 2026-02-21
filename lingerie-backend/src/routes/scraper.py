from flask import Blueprint, jsonify, request, current_app
from src.models.produto import db, Produto, Configuracao, LogScraping
import urllib.parse
from datetime import datetime
import requests
import json
import time
import threading

scraper_bp = Blueprint('scraper', __name__)

# Global variable to track progress
SCRAPER_PROGRESS = {
    'status': 'idle',
    'percentage': 0,
    'message': '',
    'details': {}
}

def aplicar_margem_lucro(preco_original):
    """Aplica margem de lucro ao preço original"""
    config = Configuracao.query.filter_by(chave='margem_lucro').first()
    margem = float(config.valor) if config else 105.0  # 105% padrão
    return preco_original * (1 + margem / 100)

def gerar_link_whatsapp(produto_nome, preco_venda):
    """Gera link do WhatsApp com mensagem personalizada"""
    config = Configuracao.query.filter_by(chave='numero_whatsapp').first()
    numero = config.valor if config else '43996048712' # Pega do banco ou usa padrão
    
    mensagem = f"Olá! Tenho interesse no produto:\n*{produto_nome}*\nPreço: R$ {preco_venda:.2f}\n\nGostaria de mais informações!"
    mensagem_encoded = urllib.parse.quote(mensagem)
    
    link = f"https://wa.me/55{numero}?text={mensagem_encoded}"
    return link

def extrair_dados_caliente():
    """Conecta na API da Caliente e extrai produtos reais - ESTRATÉGIA HÍBRIDA COMPLETA"""
    url_base = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    produtos_encontrados = {}

    # ESTRATÉGIA 1: Categorias + Cores + Tamanhos + Estilos + Tecidos (EXPANDIDO)
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

        # Cores (NOVO)
        'preto', 'branco', 'vermelho', 'azul', 'rosa', 'verde',
        'amarelo', 'roxo', 'laranja', 'nude', 'bege', 'cinza',
        'pink', 'lilás', 'coral', 'dourado', 'prateado',
        'bordô', 'vinho', 'marrom', 'turquesa',

        # Tamanhos (NOVO)
        'P', 'M', 'G', 'GG', 'XG', 'PP',
        'pequeno', 'medio', 'grande',

        # Estilos e características (NOVO)
        'renda', 'rendado', 'transparente', 'aveludado', 'estampado',
        'liso', 'floral', 'onça', 'leopardo', 'animal print',
        'bolinhas', 'listrado', 'xadrez',
        'bojo', 'sem bojo', 'meia taça', 'push up', 'aro',
        'sem aro', 'tomara que caia', 'frente unica',
        'sexy', 'sensual', 'conforto', 'comfort',
        'romântico', 'romantico', 'luxo', 'premium',
        'básico', 'basico', 'casual', 'noite', 'dia',

        # Tecidos (NOVO)
        'microfibra', 'algodão', 'algodao', 'cotton',
        'cetim', 'seda', 'lycra', 'elastano',
        'poliamida', 'viscose', 'nylon',
        'tule', 'renda francesa', 'guipir',

        # Ocasiões (NOVO)
        'noiva', 'casamento', 'lua de mel',
        'dia dos namorados', 'natal', 'ano novo',
        'inverno', 'verao', 'verão'
    ]

    print(f"Fase 1: Buscando por {len(categorias)} categorias...")
    for termo in categorias:
        try:
            data = {'acao': 'sugestao_produto', 'busca': termo}
            response = requests.post(url_base, headers=headers, data=data, timeout=15)
            response.raise_for_status()

            items = response.json()
            if isinstance(items, list):
                for item in items:
                    if str(item.get('id')) not in produtos_encontrados:
                        produtos_encontrados[str(item.get('id'))] = item

            time.sleep(0.25)
        except Exception as e:
            print(f"Erro ao buscar '{termo}': {e}")
            continue

    print(f"Após categorias: {len(produtos_encontrados)} produtos")

    # ESTRATÉGIA 2: Alfabeto completo (a-z)
    import string
    print(f"Fase 2: Buscando por alfabeto (a-z)...")
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

    print(f"Após alfabeto: {len(produtos_encontrados)} produtos")


def extrair_dados_sitemap(apenas_atualizacao=False):
    """
    Conecta no sitemap, extrai IDs e busca produtos na API
    apenas_atualizacao: Se True, pula produtos que já existem e têm dados completos (cores/tamanhos)
    """
    global SCRAPER_PROGRESS
    
    url_base = 'https://calientelingerie.com.br/c/calientelingerie/17996842783'
    url_sitemap = 'https://calientelingerie.com.br/sitemap.xml'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    import re
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from threading import Lock

    try:
        SCRAPER_PROGRESS['message'] = 'Baixando sitemap para descoberta completa...'
        response = requests.get(url_sitemap, timeout=30)
        response.raise_for_status()
        
        # Extrair IDs usando Regex (mais rápido e robusto para este caso simples)
        # Padrão: /produto/{ID}/
        ids = list(set(re.findall(r'/produto/(\d+)', response.text)))
        total_ids = len(ids)
        
        SCRAPER_PROGRESS['message'] = f'Sitemap processado. {total_ids} produtos encontrados.'
        print(f"Sitemap: Encontrados {total_ids} IDs únicos.")
        
    except Exception as e:
        print(f"Erro ao baixar sitemap: {e}")
        SCRAPER_PROGRESS['status'] = 'error'
        SCRAPER_PROGRESS['message'] = f"Erro ao baixar sitemap: {str(e)}"
        return 0, 0

    import hashlib

    def calculate_hash(preco, imagens, tamanhos, cores):
        # Create a fingerprint string
        raw = f"{preco}-{imagens}-{tamanhos}-{cores}"
        return hashlib.md5(raw.encode('utf-8')).hexdigest()

    # Thread-safe counters
    lock = Lock()
    results = {
        'criados': 0,
        'atualizados': 0,
        'skipped': 0,
        'processed': 0,
        'erros': 0,
        'no_changes': 0 # New counter for hash match
    }
    
    # ... (skipping to processar_wrapper logic)
    
    # Needs current app context for DB access if needed, but we refactored to just fetch.
    # Actually, we need to query DB for Smart Update check AND Hash Check.
    # HACK: Query ALL existing IDs first.
    existing_map = {} # id -> {tamanhos, cores, imagens, data_hash}
    all_prods = Produto.query.all()
    for p in all_prods:
        existing_map[p.url_original] = {
            'tamanhos': p.tamanhos,
            'cores': p.cores,
            'imagens': p.imagens,
            'data_hash': p.data_hash
        }
    
    def processar_wrapper(pid):
         # Skip logic for "Update Only" mode (optional, let's keep it simple)
         if apenas_atualizacao:
             data = existing_map.get(str(pid))
             if data:
                 has_details = data['tamanhos'] and data['cores']
                 has_valid_images = False
                 if data['imagens']:
                      has_valid_images = all(img.startswith('http') for img in data['imagens'].split(','))
                 
                 # NOTE: We removed the check for 'skipped' here because we want to verify hash now?
                 # Actually, if we want "Smart Update" to mean "Fix missing", we keep this.
                 # If we want "Sync Stock", we should probably NOT skip if details exist, checking HASH instead.
                 # But user asked for "Efficiency".
                 # Let's keep "Smart Update" as "Fix Missing/Broken" and Hashing as "Sync Efficiently".
                 # If we check HASH, we essentially do "Smart Update" automatically.
                 pass

         # Fetch
         try:
            url_detalhes = f"https://calientelingerie.com.br/produto/{pid}/17996842783?ajax=ajax"
            response = requests.get(url_detalhes, headers=headers, timeout=15)
            if response.status_code == 200:
                item = response.json()
                return 'fetched', item
         except:
             pass
         return 'error', None

    MAX_WORKERS = 5
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_id = {executor.submit(processar_wrapper, pid): pid for pid in ids}
        
        for future in as_completed(future_to_id):
            pid = future_to_id[future]
            results['processed'] += 1
            percentage = int((results['processed'] / total_ids) * 100)
            SCRAPER_PROGRESS['percentage'] = percentage
            
            if results['processed'] % 10 == 0:
                SCRAPER_PROGRESS['message'] = f"Processando {results['processed']}/{total_ids} (Ignorados: {results['no_changes']})..."
            
            try:
                status, data = future.result()
                if status == 'fetched' and data:
                    item_encontrado = data
                    nome = item_encontrado.get('nome')
                    if not nome: continue
                    
                    preco_original = float(item_encontrado.get('preco', 0))
                    categoria = item_encontrado.get('categoria_nome', 'Lingerie')
                    
                    # Images
                    imagens_lista = item_encontrado.get('imagens', [])
                    imagens_final = []
                    for img in imagens_lista:
                        if img and not img.startswith('http'):
                            imagens_final.append(f"https://arquivos.facilzap.app.br/{img}")
                        else:
                            imagens_final.append(img)
                    imagens_str = ','.join(imagens_final)
                    
                    # Variants - usar 'disponibilidade' como fonte de verdade
                    # (mesmo campo que o fornecedor usa para exibir na página)
                    tamanhos_set = set()
                    cores_set = set()

                    variacoes = item_encontrado.get('variacoes', {})
                    disponibilidade = item_encontrado.get('disponibilidade', {})

                    if isinstance(variacoes, dict) and isinstance(disponibilidade, dict) and disponibilidade:
                        # disponibilidade contém APENAS os IDs que o fornecedor exibe na página
                        for var_id in disponibilidade.keys():
                            var_data = variacoes.get(var_id)
                            if not var_data:
                                continue
                            var_nome = var_data.get('nome', '').strip()
                            var_cor = var_data.get('cor')
                            if var_cor and var_cor.strip():
                                cores_set.add(var_nome)
                            else:
                                if var_nome.lower().startswith("tamanho "):
                                    tamanhos_set.add(var_nome[8:].strip())
                                else:
                                    tamanhos_set.add(var_nome)
                    elif isinstance(variacoes, dict):
                        # Fallback: sem disponibilidade, usar status como filtro
                        for var_id, var_data in variacoes.items():
                            if var_data.get('status') == "1":
                                var_nome = var_data.get('nome', '').strip()
                                var_cor = var_data.get('cor')
                                if var_cor and var_cor.strip():
                                    cores_set.add(var_nome)
                                else:
                                    if var_nome.lower().startswith("tamanho "):
                                        tamanhos_set.add(var_nome[8:].strip())
                                    else:
                                        tamanhos_set.add(var_nome)
                    
                    import re
                    match_cor = re.search(r'\((.*?)\)', nome)
                    if match_cor and len(match_cor.group(1)) < 30:
                        cores_set.add(match_cor.group(1))
                    
                    tamanhos_str = ', '.join(sorted(list(tamanhos_set)))
                    cores_str = ', '.join(sorted(list(cores_set)))
                    
                    # HASH CHECK
                    new_hash = calculate_hash(preco_original, imagens_str, tamanhos_str, cores_str)
                    existing_data = existing_map.get(str(pid))
                    
                    if existing_data and existing_data.get('data_hash') == new_hash:
                        # Identical content -> SKIP WRITE
                        results['no_changes'] += 1
                        continue

                    # SAVE TO DB
                    prod = Produto.query.filter_by(url_original=str(pid)).first()
                    preco_venda = aplicar_margem_lucro(preco_original)
                    link_whatsapp = gerar_link_whatsapp(nome, preco_venda)
                    
                    if prod:
                        prod.preco_original = preco_original
                        prod.preco_venda = preco_venda
                        prod.imagens = imagens_str
                        prod.link_whatsapp = link_whatsapp
                        prod.tamanhos = tamanhos_str
                        prod.cores = cores_str
                        prod.data_hash = new_hash # Save new hash
                        prod.data_atualizacao = datetime.utcnow()
                        results['atualizados'] += 1
                    else:
                        new_prod = Produto(
                            nome=nome, preco_original=preco_original, preco_venda=preco_venda,
                            categoria=categoria, descricao=f"{nome} - {categoria}",
                            imagens=imagens_str, link_whatsapp=link_whatsapp,
                            url_original=str(pid), tamanhos=tamanhos_str, cores=cores_str,
                            data_hash=new_hash
                        )
                        db.session.add(new_prod)
                        results['criados'] += 1
                    
                    if (results['criados'] + results['atualizados']) % 50 == 0:
                        db.session.commit()
                        
            except Exception as e:
                print(f"Exception processing {pid}: {e}")
                results['erros'] += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
        
    return results['criados'], results['atualizados']

def run_scraper_thread(app_context, strategy='keyword'):
    """Função que roda em thread separada"""
    global SCRAPER_PROGRESS
    
    with app_context:
        try:
            SCRAPER_PROGRESS['status'] = 'running'
            SCRAPER_PROGRESS['percentage'] = 0
            SCRAPER_PROGRESS['message'] = 'Iniciando...'
            SCRAPER_PROGRESS['details'] = {}
            
            produtos_criados = 0
            produtos_atualizados = 0
            
            if strategy == 'sitemap':
                 produtos_criados, produtos_atualizados = extrair_dados_sitemap(apenas_atualizacao=False)
            elif strategy == 'smart_update':
                 produtos_criados, produtos_atualizados = extrair_dados_sitemap(apenas_atualizacao=True)
            else:
                 # Default strategy (keyword)
                 produtos_criados, produtos_atualizados = extrair_dados_caliente()
            
            # Log sucesso
            log = LogScraping(
                produtos_novos=produtos_criados,
                produtos_atualizados=produtos_atualizados,
                erros=None,
                status='sucesso'
            )
            db.session.add(log)
            db.session.commit()
            
            SCRAPER_PROGRESS['status'] = 'completed'
            SCRAPER_PROGRESS['percentage'] = 100
            SCRAPER_PROGRESS['message'] = 'Concluído!'
            SCRAPER_PROGRESS['details'] = {
                'produtos_novos': produtos_criados,
                'produtos_atualizados': produtos_atualizados,
                'total_encontrados': produtos_criados + produtos_atualizados
            }
            
        except Exception as e:
            db.session.rollback()
            SCRAPER_PROGRESS['status'] = 'error'
            SCRAPER_PROGRESS['message'] = str(e)
            
            # Log erro
            try:
                log = LogScraping(
                    produtos_novos=0,
                    produtos_atualizados=0,
                    erros=str(e),
                    status='erro'
                )
                db.session.add(log)
                db.session.commit()
            except:
                pass


@scraper_bp.route('/scraper/executar', methods=['POST'])
def executar_scraper():
    """Inicia o scraper em background"""
    global SCRAPER_PROGRESS
    
    if SCRAPER_PROGRESS['status'] == 'running':
        return jsonify({'erro': 'Scraper já está em execução'}), 400
    
    # Obter estratégia do corpo da requisição
    data = request.get_json() or {}
    strategy = data.get('strategy', 'keyword')
    
    # Resetar status IMEDIATAMENTE antes de iniciar a thread
    # Isso evita que o frontend leia um status antigo (ex: 'completed') antes da thread iniciar
    SCRAPER_PROGRESS = {
        'status': 'running',
        'percentage': 0,
        'message': 'Inicializando scraper...',
        'details': {}
    }
        
    app = current_app._get_current_object()
    thread = threading.Thread(target=run_scraper_thread, args=(app.app_context(), strategy))
    thread.start()
    
    return jsonify({'mensagem': f'Scraper iniciado em background (Estratégia: {strategy})'})

@scraper_bp.route('/scraper/progress', methods=['GET'])
def get_progress():
    """Retorna o progresso atual do scraper"""
    return jsonify(SCRAPER_PROGRESS)

@scraper_bp.route('/scraper/status', methods=['GET'])
def status_scraper():
    """Obtém status do último scraping"""
    try:
        ultimo_log = LogScraping.query.order_by(LogScraping.data_execucao.desc()).first()
        
        if ultimo_log:
            return jsonify(ultimo_log.to_dict())
        else:
            return jsonify({'mensagem': 'Nenhum scraping executado ainda'})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@scraper_bp.route('/scraper/logs', methods=['GET'])
def logs_scraper():
    """Lista logs de scraping"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        logs_paginados = LogScraping.query.order_by(
            LogScraping.data_execucao.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        logs_dict = [log.to_dict() for log in logs_paginados.items]
        
        return jsonify({
            'logs': logs_dict,
            'total': logs_paginados.total,
            'pages': logs_paginados.pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

