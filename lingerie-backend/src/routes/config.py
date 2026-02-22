from flask import Blueprint, jsonify
from src.models.produto import db, Configuracao, Produto
import urllib.parse

config_bp = Blueprint('config', __name__)

@config_bp.route('/config/run-migrations', methods=['POST'])
def run_migrations():
    """Executa migrações de banco de dados manualmente"""
    results = []
    migrations = [
        'ALTER TABLE produtos ALTER COLUMN tamanhos TYPE TEXT',
        'ALTER TABLE produtos ADD COLUMN destaque BOOLEAN DEFAULT FALSE',
    ]
    for sql in migrations:
        try:
            db.session.execute(db.text(sql))
            db.session.commit()
            results.append({'sql': sql, 'status': 'ok'})
        except Exception as e:
            db.session.rollback()
            results.append({'sql': sql, 'status': 'skipped', 'reason': str(e)})

    # Verificar se coluna destaque existe agora
    try:
        db.session.execute(db.text("SELECT destaque FROM produtos LIMIT 1"))
        destaque_exists = True
    except Exception:
        db.session.rollback()
        destaque_exists = False

    return jsonify({
        'mensagem': 'Migrações executadas',
        'results': results,
        'destaque_column_exists': destaque_exists
    })

@config_bp.route('/config/setup', methods=['POST'])
def setup_config():
    """Configura o banco de dados com WhatsApp e margem de lucro"""
    try:
        # Configurar WhatsApp
        whatsapp_config = Configuracao.query.filter_by(chave='numero_whatsapp').first()
        if whatsapp_config:
            whatsapp_config.valor = '43996048712'
        else:
            whatsapp_config = Configuracao(chave='numero_whatsapp', valor='43996048712')
            db.session.add(whatsapp_config)
        
        # Configurar margem de lucro
        margem_config = Configuracao.query.filter_by(chave='margem_lucro').first()
        if margem_config:
            margem_config.valor = '105'
        else:
            margem_config = Configuracao(chave='margem_lucro', valor='105')
            db.session.add(margem_config)
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Configurações aplicadas com sucesso',
            'whatsapp': '43996048712',
            'margem_lucro': '105%'
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@config_bp.route('/config/limpar-produtos', methods=['POST'])
def limpar_produtos():
    """Deleta todos os produtos do banco de dados"""
    try:
        produtos_deletados = Produto.query.delete()
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Produtos deletados com sucesso',
            'produtos_deletados': produtos_deletados
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@config_bp.route('/config/atualizar-produtos', methods=['POST'])
def atualizar_produtos():
    """Atualiza os links do WhatsApp de todos os produtos"""
    try:
        config = Configuracao.query.filter_by(chave='numero_whatsapp').first()
        numero = config.valor if config else '43996048712'
        
        produtos = Produto.query.all()
        produtos_atualizados = 0
        
        for produto in produtos:
            mensagem = f"Olá! Tenho interesse no produto:\n*{produto.nome}*\nPreço: R$ {produto.preco_venda:.2f}\n\nGostaria de mais informações!"
            mensagem_encoded = urllib.parse.quote(mensagem)
            # Adicionar código do país +55
            produto.link_whatsapp = f"https://wa.me/55{numero}?text={mensagem_encoded}"
            produtos_atualizados += 1
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Produtos atualizados com sucesso',
            'produtos_atualizados': produtos_atualizados,
            'numero_whatsapp': f"55{numero}"
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

