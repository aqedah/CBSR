/* 오프라인 지원: 앱 화면은 인터넷이 되면 늘 새로 받고(network first),
   성경 본문·지형도·아이콘·글꼴·라이브러리는 처음 받은 뒤 보관해 둡니다(cache first). 기록은 Firestore가 따로 보관합니다. */
const V="cbsr-9576856a", D="cbsr-data-1", KEEP=["bible.js?v=87606874","bible_snb.js?v=da6552bc","bible_shg.js?v=da6552bc"];
/* 11-20 GPT 2차: 새 판마다 본문·지형도·그림까지 모두 지우던 것을 고침 — 앱 화면(V)만 판마다 바꾸고, 한 번 받은 자료(D)는 남김. 본문 파일은 지금 판이 아닌 것만 정리 */
const SHELL=["./","index.html","config.js","sync.js","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>/^cbsr-/.test(k)&&k!==V&&k!==D).map(k=>caches.delete(k))))
  .then(()=>caches.open(D)).then(c=>c.keys().then(rs=>Promise.all(rs.filter(q=>{const u=new URL(q.url);return /\/bible(_[a-z]+)?\.js$/.test(u.pathname)&&!KEEP.includes(u.pathname.split("/").pop()+u.search);}).map(q=>c.delete(q))))).then(()=>caches.open(D)).then(c=>c.keys().then(rs=>Promise.all(rs.filter(q=>/ibasemaps-api|maps\.eox\.at|gibs\.earthdata|elevation-tiles-prod/.test(q.url)).map(q=>c.delete(q))))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);
  if(/firestore\.googleapis\.com|identitytoolkit|securetoken|firebaseinstallations/.test(u.hostname))return;
  /* 11-21 목사님(데이터·저장 공간): 성경 지구의 위성사진·높이 조각은 보관함에 넣지 않음(브라우저가 알아서 잠깐 보관). 넣으면 돌려 볼 때마다 휴대폰 저장 공간이 끝없이 참 */
  if(/ibasemaps-api\.arcgis\.com|maps\.eox\.at|gibs\.earthdata\.nasa\.gov/.test(u.hostname)||/elevation-tiles-prod/.test(u.pathname))return;
  const shell=u.origin===location.origin&&!/bible\.js|\/terrain\/|\/terr[hwm]i?\/|\/icons\/|\/img\//.test(u.pathname);
  /* 11-13: 앱 화면을 다시 열 때(탭이 지워졌다 돌아올 때 등) 망이 1.5초 안에 안 오면 보관본을 먼저 보여 주고, 새 판은 뒤에서 받아 둠(다음에 열 때 반영) */
  if(shell&&r.mode==="navigate"){const net=fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res;});
    const appPage=/(^|\/)(index\.html|v2\.html)?$/.test(u.pathname);
    e.respondWith(caches.match(r,{ignoreSearch:true}).then(m=>m||(appPage?caches.match("index.html"):null)).then(m=>{ if(!m) return net; let done=false; return Promise.race([net.then(x=>{done=true;return x;}).catch(()=>m),new Promise(ok=>setTimeout(()=>ok(m),1500))]); }));return;}
  /* 11-20 GPT 감사 P1-7: 망이 끊겼을 때 앱 화면 대신 index.html을 돌려주는 것은 앱 화면을 열 때만. 자료(json 등)·다른 쪽은 보관본이 없으면 분명한 오류로 */
  if(shell){e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));}return res;}).catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||new Response("오프라인: 아직 받아 두지 않은 자료입니다.",{status:503,headers:{"Content-Type":"text/plain; charset=utf-8"}}))));return;}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==="opaque"){const cp=res.clone();caches.open(D).then(c=>c.put(r,cp));}return res;})));});
