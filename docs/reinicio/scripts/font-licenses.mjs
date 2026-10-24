import fs from 'node:fs';
for (const [name,dir] of [['Bodoni-Moda','bodonimoda'],['Cormorant-Garamond','cormorantgaramond'],['DM-Sans','dmsans']]){const r=await fetch(`https://raw.githubusercontent.com/google/fonts/main/ofl/${dir}/OFL.txt`);if(!r.ok)throw Error(`${name}: ${r.status}`);fs.writeFileSync(`public/conceitos/assets/${name}-OFL.txt`,await r.text());}
console.log('Licenças das três famílias incluídas.');
