from src.main import app
from src.models.produto import db, Produto

def fix_images():
    print("Iniciando correção direta de imagens no banco de dados...")
    
    with app.app_context():
        produtos = Produto.query.all()
        count_fixed = 0
        
        for p in produtos:
            if not p.imagens:
                continue
                
            imgs = p.imagens.split(',')
            new_imgs = []
            changed = False
            
            for img in imgs:
                img = img.strip()
                if img and not img.startswith('http'):
                    # Fix relative path
                    # Check if it starts with slash or not
                    if img.startswith('/'):
                        fixed_img = f"https://calientelingerie.com.br{img}"
                    else:
                        fixed_img = f"https://calientelingerie.com.br/{img}"
                    
                    new_imgs.append(fixed_img)
                    changed = True
                else:
                    new_imgs.append(img)
            
            if changed:
                p.imagens = ','.join(new_imgs)
                count_fixed += 1
        
        if count_fixed > 0:
            db.session.commit()
            print(f"Sucesso! {count_fixed} produtos tiveram suas imagens corrigidas instantaneamente.")
        else:
            print("Nenhum produto precisou de correção.")

if __name__ == "__main__":
    fix_images()
