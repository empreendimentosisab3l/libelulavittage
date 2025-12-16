from src.main import app
from src.models.produto import db, Produto

def reset_variants():
    print("Resetando variantes no banco de dados para forçar atualização inteligente...")
    
    with app.app_context():
        # Update all products: set tamanhos = NULL, cores = NULL
        # Or empty string? The scraper checks `if existing_prod.tamanhos and ...`
        # So None or empty string works.
        
        produtos = Produto.query.all()
        count = 0
        for p in produtos:
            p.tamanhos = None
            p.cores = None
            count += 1
        
        db.session.commit()
        print(f"Sucesso! {count} produtos tiveram os dados de variantes limpos.")

if __name__ == "__main__":
    reset_variants()
