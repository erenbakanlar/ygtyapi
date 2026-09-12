import fs from 'node:fs';
const html=fs.readFileSync('dist/index.html','utf8');
const refs=[...html.matchAll(/(?:src|href)="([^"]+)"/g)].map(x=>x[1]);
const missing=refs.filter(x=>! /^(https?:|tel:|#|data:)/.test(x)&&!fs.existsSync('dist/'+x));
const ids=new Set([...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]));
const brokenAnchors=refs.filter(x=>x.startsWith('#')&&x.length>1&&!ids.has(x.slice(1)));
const schema=JSON.parse(html.match(/application\/ld\+json">(.*?)<\/script>/s)[1]);
console.log(JSON.stringify({missing,brokenAnchors,schema:schema['@type'],h1Count:[...html.matchAll(/<h1>/g)].length,images:fs.readdirSync('dist/assets').filter(x=>x.endsWith('.webp')).map(x=>({name:x,bytes:fs.statSync('dist/assets/'+x).size}))},null,2));
if(missing.length||brokenAnchors.length) process.exit(1);
