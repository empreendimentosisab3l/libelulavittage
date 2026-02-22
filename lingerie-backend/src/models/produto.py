from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    preco_original = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    imagens = db.Column(db.Text)  # JSON string with image URLs
    tamanhos = db.Column(db.Text) # Lista de tamanhos (P, M, G...)
    cores = db.Column(db.Text, nullable=True) # Cores disponíveis (ex: "Vermelho, Preto")
    data_hash = db.Column(db.String(32), nullable=True) # Hash MD5 para controle de alterações
    link_whatsapp = db.Column(db.String(1000))  # Link do WhatsApp
    url_original = db.Column(db.String(500))
    destaque = db.Column(db.Boolean, default=False) # Produto em destaque no fornecedor
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco_original': self.preco_original,
            'preco_venda': self.preco_venda,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'imagens': self.imagens.split(',') if self.imagens else [],
            'tamanhos': self.tamanhos.split(', ') if self.tamanhos else [],
            'cores': self.cores,
            'link_whatsapp': self.link_whatsapp,
            'url_original': self.url_original,
            'destaque': self.destaque or False,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

class Configuracao(db.Model):
    __tablename__ = 'configuracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'chave': self.chave,
            'valor': self.valor,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

class LogScraping(db.Model):
    __tablename__ = 'logs_scraping'
    
    id = db.Column(db.Integer, primary_key=True)
    data_execucao = db.Column(db.DateTime, default=datetime.utcnow)
    produtos_novos = db.Column(db.Integer, default=0)
    produtos_atualizados = db.Column(db.Integer, default=0)
    erros = db.Column(db.Text)
    status = db.Column(db.String(50), default='sucesso')
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_execucao': self.data_execucao.isoformat() if self.data_execucao else None,
            'produtos_novos': self.produtos_novos,
            'produtos_atualizados': self.produtos_atualizados,
            'erros': self.erros,
            'status': self.status
        }

