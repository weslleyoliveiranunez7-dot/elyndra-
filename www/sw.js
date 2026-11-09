const V='elyndra-v2';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(['./','./index.html','./manifest.webmanifest','./img/icon-192.png'])).catch(()=>{}))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
e.respondWith(caches.open(V).then(c=>c.match(r,{ignoreSearch:true}).then(m=>{const n=fetch(r).then(x=>{if(x&&x.ok&&x.status===200)c.put(r,x.clone());return x}).catch(()=>m);return m||n})))});
