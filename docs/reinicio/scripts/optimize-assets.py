from PIL import Image
from pathlib import Path
assets=Path('lingerie-frontend/public/conceitos/assets')
before=after=0
for p in assets.glob('*.webp'):
 before+=p.stat().st_size
 im=Image.open(p).convert('RGB');im.thumbnail((900,1200));im.save(p,'WEBP',quality=83,method=6)
 after+=p.stat().st_size
for p in assets.glob('*OFL.txt'):
 p.write_text('\n'.join(line.rstrip() for line in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
print(f'Fotos: {before/1024/1024:.1f} MB -> {after/1024/1024:.1f} MB')
