from src.main import app
from src.models.produto import db, Produto
import json

def inspect_images():
    with app.app_context():
        # Get first 5 products
        produtos = Produto.query.limit(5).all()
        print(f"Inspecting {len(produtos)} products...")
        
        for p in produtos:
            print(f"\nID: {p.id} | Nome: {p.nome}")
            print(f"Imagens (Raw): {p.imagens}")
            
            # Check if they look correct
            imgs = p.imagens.split(',') if p.imagens else []
            for img in imgs:
                print(f" - {img}")
                if not img.startswith('http'):
                     print("   [WARNING] Relative path detected!")
                elif 'calientelingerie.com.br' not in img:
                     print("   [NOTE] External domain?")

if __name__ == "__main__":
    inspect_images()
