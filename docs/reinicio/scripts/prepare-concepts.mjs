import fs from 'node:fs';
const products=JSON.parse(fs.readFileSync('public/conceitos/produtos.json','utf8'));
fs.mkdirSync('public/conceitos/assets',{recursive:true});
for(const p of products.slice(0,18)){
 const url=String(p.imagens).split(',')[0]; const r=await fetch(url); if(!r.ok) throw Error(r.status); fs.writeFileSync(`public/conceitos/assets/${p.id}.webp`,Buffer.from(await r.arrayBuffer()));
}
const r=await fetch('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap',{headers:{'User-Agent':'Mozilla/5.0'}}); let css=await r.text(); let i=0; for(const match of [...css.matchAll(/url\((https:[^)]+)\)/g)]){const file=`font-${i++}.woff2`;const response=await fetch(match[1]);fs.writeFileSync(`public/conceitos/assets/${file}`,Buffer.from(await response.arrayBuffer()));css=css.replace(match[1],`./${file}`);}fs.writeFileSync('public/conceitos/assets/fonts.css',css);console.log('18 fotos reais e fontes locais salvas');
