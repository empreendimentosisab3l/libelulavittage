import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from sqlalchemy import event
from sqlalchemy.engine import Engine
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

# Pool settings for Render free tier (512MB RAM)
engine_options = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
    'pool_size': 2,
    'max_overflow': 3
}

# Fix: Render PostgreSQL has a very short statement_timeout that kills queries
# Disable it completely (0 = no limit); gunicorn --timeout 120 handles runaway queries
if database_url:
    engine_options['connect_args'] = {
        'connect_timeout': 10,
        'options': '-c statement_timeout=0'
    }

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options

db.init_app(app)

# Event listener: disable statement_timeout on every new connection (belt + suspenders)
# Uses Engine CLASS (not db.engine instance) to avoid "outside application context" error
@event.listens_for(Engine, 'connect')
def set_statement_timeout(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("SET statement_timeout = '0'")
    cursor.close()

with app.app_context():
    db.create_all()
    db.session.remove()
    db.engine.dispose()
    print("[STARTUP] Banco inicializado com sucesso.")

@app.route('/api/health')
def health():
    """Debug endpoint to test DB connection"""
    import traceback
    import time
    start = time.time()
    try:
        result = db.session.execute(db.text('SELECT 1'))
        row = result.fetchone()
        t1 = time.time() - start
        count = db.session.execute(db.text('SELECT COUNT(*) FROM produtos')).fetchone()
        t2 = time.time() - start
        destaque_count = db.session.execute(db.text('SELECT COUNT(*) FROM produtos WHERE destaque = true')).fetchone()
        t3 = time.time() - start
        return jsonify({
            'status': 'ok',
            'db_test': row[0] if row else None,
            'total_produtos': count[0] if count else 0,
            'destaque_count': destaque_count[0] if destaque_count else 0,
            'timings': {'select1': f'{t1:.2f}s', 'count': f'{t2:.2f}s', 'destaque': f'{t3:.2f}s'}
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'status': 'error', 'erro': str(e), 'elapsed': f'{time.time()-start:.2f}s'}), 500

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
