from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
root=Path('docs/reinicio/prints')
for name in ['rubi','noite','jardim']:
 board=Image.new('RGB',(1420,850),'#eee8de'); draw=ImageDraw.Draw(board)
 draw.text((25,15),name.upper()+' | Desktop 1440 px / celular 375 px',fill='#302820')
 for file,x,w in [(f'{name}-desktop.png',20,1040),(f'{name}-375.png',1090,310)]:
  im=Image.open(root/file).convert('RGB');im.thumbnail((w,780));board.paste(im,(x,50))
 board.save(root/f'{name}-comparativo.jpg',quality=92)
 for mode in ['375','desktop']:
  board=Image.new('RGB',(1440,850),'#eee8de')
  for i,section in enumerate(['','colecao','editorial','ritual']):
   im=Image.open(root/f'{name}{"-"+section if section else ""}-{mode}.png').convert('RGB');im.thumbnail((350,780));board.paste(im,(i*360,40))
  board.save(root/f'{name}-secoes-{mode}.jpg',quality=90)
