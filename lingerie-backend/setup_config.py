import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.produto import db, Configuracao
from src.main import app

with app.app_context():
    # Criar tabelas
    db.create_all()
    
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
    
    print('Configuracoes aplicadas com sucesso!')
    print(f'   WhatsApp: 43996048712')
    print(f'   Margem de lucro: 105%')

