from flask import Blueprint, jsonify, request
from src.models.produto import db, Produto, Configuracao
import urllib.parse

produtos_bp = Blueprint('produtos', __name__)

def get_configuracao(chave, valor_padrao):
    """Busca uma configuração no banco de dados"""
    config = Configuracao.query.filter_by(chave=chave).first()
    return config.valor if config else valor_padrao

def gerar_link_whatsapp(produto, numero_whatsapp=None):
    """Gera link do WhatsApp com mensagem personalizada"""
    if numero_whatsapp is None:
        numero_whatsapp = get_configuracao('numero_whatsapp', '5511999999999')

    mensagem = f"""Olá! Tenho interesse no produto:
*{produto.nome}*
Preço: R$ {produto.preco_venda:.2f}

Gostaria de mais informações!"""

    mensagem_encoded = urllib.parse.quote(mensagem)
    return f"https://wa.me/{numero_whatsapp}?text={mensagem_encoded}"

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Lista produtos com paginação e filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 24, type=int)
        categoria = request.args.get('categoria')
        busca = request.args.get('busca')

        query = Produto.query.filter_by(ativo=True)

        if categoria:
            query = query.filter(Produto.categoria.ilike(f'%{categoria}%'))

        if busca:
            query = query.filter(Produto.nome.ilike(f'%{busca}%'))

        # Ordenar: destaques primeiro, depois por ID decrescente (mais recentes)
        # Fallback seguro caso a coluna destaque ainda não exista no banco
        try:
            query_with_destaque = query.order_by(Produto.destaque.desc(), Produto.id.desc())
            produtos_paginados = query_with_destaque.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            # Força execução para verificar se coluna existe
            _ = produtos_paginados.items
        except Exception:
            db.session.rollback()
            query = Produto.query.filter_by(ativo=True)
            if categoria:
                query = query.filter(Produto.categoria.ilike(f'%{categoria}%'))
            if busca:
                query = query.filter(Produto.nome.ilike(f'%{busca}%'))
            query = query.order_by(Produto.id.desc())
            produtos_paginados = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

        # Buscar número do WhatsApp uma única vez (resolve N+1 query)
        numero_whatsapp = get_configuracao('numero_whatsapp', '5511999999999')

        produtos_dict = []
        for produto in produtos_paginados.items:
            produto_dict = produto.to_dict()
            produto_dict['link_whatsapp'] = gerar_link_whatsapp(produto, numero_whatsapp)
            produtos_dict.append(produto_dict)

        return jsonify({
            'produtos': produtos_dict,
            'total': produtos_paginados.total,
            'pages': produtos_paginados.pages,
            'current_page': page,
            'per_page': per_page
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produtos_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Obtém detalhes de um produto específico"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        produto_dict = produto.to_dict()
        produto_dict['link_whatsapp'] = gerar_link_whatsapp(produto)
        
        return jsonify(produto_dict)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produtos_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    """Lista todas as categorias disponíveis"""
    try:
        categorias = db.session.query(Produto.categoria).filter_by(ativo=True).distinct().all()
        categorias_list = [categoria[0] for categoria in categorias]
        
        return jsonify({'categorias': categorias_list})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produtos_bp.route('/configuracoes', methods=['GET'])
def obter_configuracoes():
    """Obtém todas as configurações"""
    try:
        configuracoes = Configuracao.query.all()
        config_dict = {config.chave: config.valor for config in configuracoes}
        
        # Configurações padrão
        defaults = {
            'margem_lucro': '100',  # 100% de margem
            'numero_whatsapp': '5511999999999',
            'mensagem_padrao': 'Olá! Tenho interesse neste produto.'
        }
        
        for chave, valor in defaults.items():
            if chave not in config_dict:
                config_dict[chave] = valor
        
        return jsonify(config_dict)
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produtos_bp.route('/configuracoes', methods=['POST'])
def atualizar_configuracoes():
    """Atualiza configurações"""
    try:
        dados = request.get_json()
        
        for chave, valor in dados.items():
            config = Configuracao.query.filter_by(chave=chave).first()
            if config:
                config.valor = str(valor)
            else:
                config = Configuracao(chave=chave, valor=str(valor))
                db.session.add(config)
        
        db.session.commit()
        return jsonify({'mensagem': 'Configurações atualizadas com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

