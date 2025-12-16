from src.main import app
from src.models.produto import db, Produto

def fix_images_cdn():
    print("Corrigindo domínio das imagens para o CDN correto...")
    
    with app.app_context():
        produtos = Produto.query.all()
        count_fixed = 0
        
        WRONG_DOMAIN = "https://calientelingerie.com.br/produtos/"
        CORRECT_DOMAIN = "https://arquivos.facilzap.app.br/produtos/"
        
        for p in produtos:
            if not p.imagens:
                continue
                
            imgs = p.imagens.split(',')
            new_imgs = []
            changed = False
            
            for img in imgs:
                img = img.strip()
                if WRONG_DOMAIN in img:
                    # Replace wrong domain with correct CDN
                    fixed_img = img.replace(WRONG_DOMAIN, CORRECT_DOMAIN)
                    new_imgs.append(fixed_img)
                    changed = True
                elif img.startswith('produtos/'):
                     # Handle cases that might have been missed or re-scraped
                     fixed_img = f"https://arquivos.facilzap.app.br/{img}"
                     new_imgs.append(fixed_img)
                     changed = True
                else:
                    new_imgs.append(img)
            
            if changed:
                p.imagens = ','.join(new_imgs)
                count_fixed += 1
        
        if count_fixed > 0:
            db.session.commit()
            print(f"Sucesso! {count_fixed} produtos corrigidos para usar o CDN da FacilZap.")
        else:
            print("Nenhum produto precisou de correção.")

if __name__ == "__main__":
    fix_images_cdn()
