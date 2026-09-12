import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve('dist');
http.createServer((req,res)=>{let requested;try{requested=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400);return res.end()};const file=path.resolve(root,'.'+(requested==='/'?'/index.html':requested));if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end()};fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);return res.end('Not found')};res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.webp':'image/webp','.txt':'text/plain; charset=utf-8','.xml':'application/xml'})[path.extname(file)]||'application/octet-stream');res.end(data)})}).listen(5173,'127.0.0.1',()=>console.log('Local: http://127.0.0.1:5173'));
