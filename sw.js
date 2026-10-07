/* 오프라인 지원: 앱 화면은 인터넷이 되면 늘 새로 받고(network first),
   성경 본문·지형도·아이콘·글꼴·라이브러리는 처음 받은 뒤 보관해 둡니다(cache first). 기록은 Firestore가 따로 보관합니다. */
const V="cbsr-6e74bc67";
const SHELL=["./","index.html","config.js","sync.js","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);
  if(/firestore\.googleapis\.com|identitytoolkit|securetoken|firebaseinstallations/.test(u.hostname))return;
  const shell=u.origin===location.origin&&!/bible\.js|\/terrain\/|\/icons\//.test(u.pathname);
  if(shell){e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res;}).catch(()=>caches.match(r).then(m=>m||caches.match("index.html"))));return;}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==="opaque"){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));}return res;})));});
