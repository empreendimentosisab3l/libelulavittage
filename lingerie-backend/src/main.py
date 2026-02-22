import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.produto import db
from src.routes.produtos import produtos_bp
from src.routes.scraper import scraper_bp
from src.routes.config import config_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes - Allow requests from Vercel
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(produtos_bp, url_prefix='/api')
app.register_blueprint(scraper_bp, url_prefix='/api')
app.register_blueprint(config_bp, url_prefix='/api')

# Enable database
# Use PostgreSQL in production (Render), SQLite locally
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render provides DATABASE_URL, use PostgreSQL
    # Fix for SQLAlchemy 1.4+ which uses postgresql:// instead of postgres://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development, use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lingerie_store.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pool recycling para evitar conexões mortas com PostgreSQL (psycopg2 OperationalError)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,      # Reciclar conexões a cada ~5 min (antes do timeout do Render)
    'pool_pre_ping': True,    # Verificar se a conexão está viva antes de usar
    'pool_size': 5,           # Tamanho do pool de conexões
    'max_overflow': 10        # Conexões extras permitidas
}

db.init_app(app)
with app.app_context():
    db.create_all()
    # Verificar se coluna destaque existe (sem tentar criá-la — isso é feito via /api/config/run-migrations)
    from src.models import produto as produto_module
    try:
        db.session.execute(db.text("SELECT destaque FROM produtos LIMIT 0"))
        produto_module.DESTAQUE_COLUMN_EXISTS = True
        print("[STARTUP] Coluna destaque existe. Ordenação por destaque ATIVADA.")
    except Exception:
        db.session.rollback()
        produto_module.DESTAQUE_COLUMN_EXISTS = False
        print("[STARTUP] Coluna destaque NÃO existe. Use POST /api/config/run-migrations para criá-la.")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

