import sys
import os
sys.path.insert(0, os.getcwd())

from src.main import app
from src.routes.scraper import extrair_dados_caliente
from src.models.produto import Produto, Configuracao, db

# Setup dummy config if needed
with app.app_context():
    # Ensure config exists for margin
    if not Configuracao.query.filter_by(chave='margem_lucro').first():
        db.session.add(Configuracao(chave='margem_lucro', valor='105.0'))
        db.session.commit()

    print("Iniciando scraper...")
    novos, atualizados = extrair_dados_caliente()
    print(f"Novos: {novos}, Atualizados: {atualizados}")
    
    total = Produto.query.count()
    print(f"Total produtos no banco: {total}")
    
    first = Produto.query.first()
    if first:
        print(f"Exemplo: {first.nome} - R$ {first.preco_venda:.2f} (Original: {first.preco_original:.2f}) - Imagem: {first.imagens[:50]}...")
