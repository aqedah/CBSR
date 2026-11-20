/* 이야기통독 — 독립 웹앱용 기록 동기화 (Firebase + Firestore)
   2026-11-20 목사님: 기록은 구글 계정으로 잇습니다(users/{구글 uid}, 본인만 읽고 씀).
   예전의 이름 + 숫자 4자리 기록(readers/{열쇠})은 구글로 들어갈 때 한 번 옮겨 오고, 새로 쓰지 않습니다. */
(function(){
  "use strict";
  const cfg=window.CBSR_FIREBASE_CONFIG;
  const LOGIN="cbsr-login-v1", LEGACY="cbsr-login-legacy";
  const ls={get(k,d){try{const v=localStorage.getItem(k);return v==null?d:JSON.parse(v);}catch(e){return d;}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}},del(k){try{localStorage.removeItem(k);}catch(e){}}};
  const LOGIN_ON=window.CBSR_LOGIN!==false;
  let fs=null,ready=null,login=LOGIN_ON?ls.get(LOGIN,null):null,pushT=null,lastSaved=null,lastErr=null,listeners=[];
  const inc=n=>firebase.firestore.FieldValue.increment(n);
  function init(){ if(ready) return ready;
    ready=(async()=>{
      if(!cfg||!cfg.apiKey||!window.firebase) throw new Error("firebase-config");
      firebase.initializeApp(cfg); const auth=firebase.auth(); fs=firebase.firestore();
      if(cfg.emulator){ auth.useEmulator("http://127.0.0.1:9099"); fs.useEmulator("127.0.0.1",8080); }
      try{ await fs.enablePersistence({synchronizeTabs:true}); }catch(e){}
      try{ await auth.getRedirectResult(); }catch(e){ console.warn("redirect",e); }
      await new Promise((res,rej)=>{ let first=true; const off=auth.onAuthStateChanged(u=>{ if(u){off();res();} else if(first){ first=false; auth.signInAnonymously().catch(rej); } }); });
      await adopt();
      auth.onAuthStateChanged(()=>{ adopt().catch(()=>{}); });
    })(); return ready; }
  /* 구글로 들어와 있으면 그 계정을 기록 주인으로. 예전 이름·숫자 기록이 이 기기에 있었으면 옮길 것으로 남겨 둠 */
  const isG=u=>!!(u&&!u.isAnonymous&&(u.providerData||[]).some(p=>p&&p.providerId==="google.com"));
  async function adopt(){ const u=firebase.auth().currentUser;
    if(isG(u)){ if(!login||!login.g||login.uid!==u.uid){ if(login&&login.key&&!login.g) ls.set(LEGACY,{name:login.name,key:login.key});
        login={g:1,uid:u.uid,name:u.displayName||(u.email||"").split("@")[0]||"",email:u.email||""}; ls.set(LOGIN,login);
        try{ const ref=fs.doc(`users/${u.uid}`); const s=await ref.get(); if(!s.exists){ await ref.set({name:login.name.slice(0,40),data:"{}",createdAt:Date.now(),updatedAt:Date.now()}); fs.doc("stats/church").set({readers:inc(1)},{merge:true}).catch(()=>{}); } }catch(e){ lastErr={at:new Date(),code:e&&e.code||""}; console.warn("users",e); }
        notify(); } }
    else if(login&&login.g){ login=null; ls.del(LOGIN); notify(); } }
  const docOf=()=>login&&login.g?fs.doc(`users/${login.uid}`):login&&login.key?fs.doc(`readers/${login.key}`):null;
  async function keyOf(name,pin){
    const s=`cbsr|${name.replace(/\s+/g,"")}|${pin}`;
    const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(s));
    return [...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,"0")).join("");
  }
  const notify=()=>listeners.forEach(f=>{try{f();}catch(e){}});
  /* 저장(11-20 GPT 2차 검토): ① 바이트로 크기를 재고 ② 크면 조각으로 나눠 한 번에(batch) 쓰고 ③ 고쳐지지 않는 오류(권한·형식·너무 큼)는 되풀이하지 않음 */
  let pend=null, partsN=0; const INLINE_MAX=700000, PART=200000, LEGACY_MAX=850000;
  const bytes=s=>new TextEncoder().encode(s).length;
  async function write(mem){ await init(); const r=docOf(); if(!r) return; const s=JSON.stringify(mem), b=bytes(s), name=String(login.name||"").slice(0,40);
    if(!login.g){ if(b>LEGACY_MAX){ const e=new Error("too-big"); e.code="too-big"; throw e; } await r.set({name,data:s,updatedAt:Date.now()},{merge:true}); return; }
    const B=fs.batch();
    if(b<=INLINE_MAX){ const doc={name,data:s,updatedAt:Date.now()}; if(partsN>0) doc.n=0; /* 조각을 쓴 적 없으면 n 칸을 만들지 않음(예전 규칙에서도 저장되게) */ B.set(r,doc,{merge:true}); for(let i=0;i<partsN;i++) B.delete(r.collection("c").doc(String(i))); await B.commit(); partsN=0; return; }
    const P=[]; for(let i=0;i<s.length;){ let j=Math.min(s.length,i+PART); const c=s.charCodeAt(j-1); if(j<s.length&&c>=0xD800&&c<=0xDBFF) j--; /* 이모지 반쪽으로 자르지 않게 */ P.push(s.slice(i,j)); i=j; } if(P.length>60){ const e=new Error("too-big"); e.code="too-big"; throw e; }
    P.forEach((t,i)=>B.set(r.collection("c").doc(String(i)),{s:t})); for(let i=P.length;i<partsN;i++) B.delete(r.collection("c").doc(String(i)));
    B.set(r,{name,data:"",n:P.length,updatedAt:Date.now()},{merge:true}); await B.commit(); partsN=P.length; }
  const PERM=/permission-denied|invalid-argument|too-big|unauthenticated|failed-precondition|out-of-range/;
  async function run(now){ const m=pend; if(!m||!login) return; pend=null;
    try{ await Promise.race([write(m),new Promise((_,rej)=>setTimeout(()=>{ const e=new Error("timeout"); e.code="timeout"; rej(e); },20000))]); lastSaved=new Date(); lastErr=null; notify(); }
    catch(e){ console.warn("sync",e); const c=e&&e.code||""; lastErr={at:new Date(),code:c}; notify();
      if(!PERM.test(c)){ if(!pend) pend=m; clearTimeout(pushT); pushT=setTimeout(run,/resource-exhausted/.test(c)?300000:30000); }
      if(now) throw e; } }
  window.SYNC={
    available:!!(cfg&&cfg.apiKey),
    loginEnabled:LOGIN_ON,
    loggedIn:()=>!!login,
    google:()=>!!(login&&login.g), /* 구글 계정으로 잇는 중 */
    legacyOnly:()=>!!(login&&login.key&&!login.g), /* 예전 이름·숫자로만 잇는 중(구글로 옮겨야 함) */
    email:()=>login&&login.email||"",
    /* 이 기기 기록의 주인 표시(계정을 바꿀 때 앞사람 기록이 뒷사람 계정에 섞이지 않게) */
    uid:()=>login&&login.g?"g:"+login.uid:login&&login.key?"k:"+login.key:"",
    name:()=>login?login.name:"",
    lastSaved:()=>lastSaved,
    lastError:()=>lastErr, /* 11-20 GPT 감사: 저장 실패를 화면에 알리기 위해 */
    pending:()=>!!pend,
    onChange(f){listeners.push(f);},
    /* 구글 계정으로 들어가기(휴대폰에서 창이 막히면 페이지를 옮겨 다녀옴 — 돌아오면 init()이 마저 처리) */
    async loginGoogle(){ await init(); const pv=new firebase.auth.GoogleAuthProvider(); pv.setCustomParameters({prompt:"select_account"});
      /* 11-20 GPT 2차: 사용자가 창을 닫은 것(popup-closed-by-user·cancelled-popup-request)은 취소로 끝냄. 창이 막혔거나 지원하지 않을 때만 페이지를 다녀옴 */
      try{ await firebase.auth().signInWithPopup(pv); }
      catch(e){ const c=e&&e.code||""; if(/popup-closed-by-user|cancelled-popup-request|user-cancelled/.test(c)) return "cancel";
        if(/popup-blocked|operation-not-supported|web-storage-unsupported/.test(c)){ await firebase.auth().signInWithRedirect(pv); return "redirect"; } throw e; }
      await adopt(); return login&&login.g?"ok":"fail"; },
    /* 예전 이름·숫자 기록: 옮길 것이 있는지, 가져오기, 다 옮겼다고 표시 */
    legacyPending:()=>!!(login&&login.g&&ls.get(LEGACY,null)),
    async legacyPull(){ const L=ls.get(LEGACY,null); if(!L) return null; await init(); const s=await fs.doc(`readers/${L.key}`).get(); if(!s.exists) return {}; try{ return JSON.parse(s.data().data||"{}"); }catch(e){ return {}; } },
    legacyDone(){ ls.del(LEGACY); },
    async importOld(name,pin){ name=String(name||"").trim(); pin=String(pin||"").trim();
      if(!name) throw new Error("이름을 넣어 주세요."); if(!/^\d{4}$/.test(pin)) throw new Error("숫자 4자리를 넣어 주세요.");
      await init(); const s=await fs.doc(`readers/${await keyOf(name,pin)}`).get(); if(!s.exists) throw new Error("그 이름과 숫자로 남긴 기록을 찾지 못했습니다.");
      try{ return JSON.parse(s.data().data||"{}"); }catch(e){ return {}; } },
    /* 예전 방식 들어가기(이제 새로 쓰지 않음 — 옮겨 오기에만) */
    async login(name,pin){
      name=String(name||"").trim(); pin=String(pin||"").trim();
      if(!name) throw new Error("이름을 넣어 주세요.");
      if(!/^\d{4}$/.test(pin)) throw new Error("숫자 4자리를 넣어 주세요.");
      await init(); const key=await keyOf(name,pin);
      const ref=fs.doc(`readers/${key}`); const snap=await ref.get();
      let remote=null;
      if(snap.exists){ try{ remote=JSON.parse(snap.data().data||"{}"); }catch(e){ remote={}; } }
      else { await ref.set({name,data:"{}",createdAt:Date.now(),updatedAt:Date.now()});
        fs.doc("stats/church").set({readers:inc(1)},{merge:true}).catch(()=>{}); }
      login={name,key}; ls.set(LOGIN,login); notify();
      return remote;
    },
    /* 나가기 전에 아직 못 올린 기록을 먼저 올림. 못 올리면 false(앱이 알리고 나가지 않음) */
    async logout(force){ if(!force){ try{ await window.SYNC.flush(); }catch(e){ return false; } if(pend) return false; }
      const g=login&&login.g; login=null; ls.del(LOGIN); notify(); if(g){ try{ await init(); await firebase.auth().signOut(); await firebase.auth().signInAnonymously(); }catch(e){} } return true; },
    async pull(){ if(!login) return null; await init(); const r=docOf(); if(!r) return null; const s=await r.get(); if(!s.exists) return null; const x=s.data();
      /* 11-20 GPT 2차: 기록이 커지면(문서 한 개 1MiB 한도) users/{uid}/c/{0..n-1} 조각에 나눠 둠 */
      if(x.n>0){ const P=await Promise.all([...Array(x.n).keys()].map(i=>r.collection("c").doc(String(i)).get())); partsN=x.n;
        const t=P.map(p=>p.exists?String(p.data().s||""):null); if(t.includes(null)) throw new Error("parts-missing");
        return JSON.parse(t.join("")); /* 조각이 어긋나면(다른 기기가 쓰는 중) 던져서 이번 합치기를 건너뜀 — 빈 것으로 덮지 않게 */ }
      try{ return JSON.parse(x.data||"{}"); }catch(e){ return null; } },
    push(mem,wait){ if(!login) return; pend=mem; clearTimeout(pushT); pushT=setTimeout(run,wait==null?1500:wait); },
    /* 기다리는 저장을 지금 올림(로그아웃 직전 등) */
    async flush(){ clearTimeout(pushT); if(pend) await run(true); },
    /* 관리자: 구글 계정으로 로그인 → admins/{uid} 문서가 있으면 관리자 */
    admin:{
      async state(){ await init(); const u=firebase.auth().currentUser; if(!u||u.isAnonymous) return {in:false};
        let ok=false, err=""; try{ ok=(await fs.doc(`admins/${u.uid}`).get({source:"server"})).exists; }catch(e){ err=e.code||String(e); }
        return {in:true,ok,err,uid:u.uid,email:u.email||""}; },
      /* 지금은 관리자 비밀번호(이메일/비밀번호 계정의 비밀번호만 입력) */
      async login(pw){ await init(); const em=window.CBSR_ADMIN_EMAIL; if(!em) throw new Error("관리자 계정이 설정되지 않았습니다.");
        await firebase.auth().signInWithEmailAndPassword(em,String(pw||"")); },
      /* 나중에 구글 로그인으로 바꿀 때 쓰는 함수 */
      async loginGoogle(){ await init(); const pv=new firebase.auth.GoogleAuthProvider(); pv.setCustomParameters({prompt:"select_account"});
        try{ await firebase.auth().signInWithPopup(pv); }
        catch(e){ if(/popup-blocked|operation-not-supported/.test(e.code||"")) return firebase.auth().signInWithRedirect(pv); throw e; } },
      async logout(){ await init(); await firebase.auth().signOut(); await firebase.auth().signInAnonymously(); },
      async list(){ await init(); const q=await fs.collection("feedback").orderBy("at","desc").limit(300).get(); return q.docs.map(d=>({id:d.id,...d.data()})); },
      async remove(id){ await init(); await fs.doc(`feedback/${id}`).delete(); }
    },
    /* 개발자 모드: 화면 글자 바꾸기표 (모두에게 적용, 쓰기는 관리자만) */
    /* 새 소식 가운데 관리자가 지운 것 */
    news:{
      async get(){ await init(); const d=await fs.doc("config/news").get(); return d.exists?(d.data().hidden||[]):[]; },
      async set(hidden){ await init(); await fs.doc("config/news").set({hidden,at:Date.now()}); }
    },
    /* 그림 목록에서 관리자가 고른 그림 빼기(keep: 빼서 보관, del: 삭제, back: 되살리기) */
    photos:{
      async get(){ await init(); const d=await fs.doc("config/photos").get(); return d.exists?(d.data().map||{}):{}; },
      async set(id,act){ await init(); const ref=fs.doc("config/photos"); const up={at:Date.now()}; up["map."+id]=act?act:firebase.firestore.FieldValue.delete();
        try{ await ref.update(up); }catch(e){ if(/not-found/.test(e.code||"")){ const m={}; if(act) m[id]=act; await ref.set({map:m,at:Date.now()}); } else throw e; } }
    },
    texts:{
      async get(){ await init(); const d=await fs.doc("config/texts").get(); return d.exists?(d.data().map||{}):{}; },
      async set(map){ await init(); await fs.doc("config/texts").set({map,at:Date.now()}); }
    },
    /* 피드백 보내기 */
    async feedback(o){ try{ await init();
      const t=String(o.text||"").slice(0,3000); if(!t) return false;
      const w=fs.collection("feedback").add({text:t,name:String(o.name||"").slice(0,20),plan:String(o.plan||"").slice(0,10),day:String(o.day||"").slice(0,60),ua:String(o.ua||"").slice(0,200),at:Date.now()});
      await Promise.race([w,new Promise((_,rej)=>setTimeout(()=>rej(new Error("timeout")),12000))]); return true; }catch(e){ console.warn("feedback",e); return false; } },
    /* 함께 읽기(이름 공개를 켠 사람만): together/{날}/p/{공개 번호} 에 별명·작은 사진·아멘한 성품·붙잡은 구절 */
    together:{
      async who(){ if(!login) return null; if(login.g) return login.uid; /* 구글: 문서 이름이 곧 내 계정 번호(남이 고치거나 지울 수 없게 규칙에서 확인) */ if(login.pub) return login.pub; const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode("together|"+login.key)); login.pub=[...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,"0")).join("").slice(0,24); ls.set(LOGIN,login); return login.pub; },
      async put(day,doc){ const w=await this.who(); if(!w) return false; await init(); const d=Object.assign({},doc); if(d.ph===undefined||d.ph==="") d.ph=null; /* 사진이 없을 때 undefined는 Firebase가 거절함 */ await fs.doc(`together/${day}/p/${w}`).set(d); return true; },
      async del(day){ const w=await this.who(); if(!w) throw new Error("no-login"); await init(); /* 연결이 없으면 지우기 약속이 끝나지 않으므로 12초에 실패로 봄 */ await Promise.race([fs.doc(`together/${day}/p/${w}`).delete(),new Promise((_,rej)=>setTimeout(()=>rej(new Error("timeout")),12000))]); },
      async list(day){ await init(); const q=await fs.collection(`together/${day}/p`).limit(300).get(); return q.docs.map(d=>({who:d.id,...d.data()})); }
    },
    /* 소그룹 기록 넘겨주기(2026-11-20): 내용은 서버에 두고 링크에는 추측할 수 없는 번호만. 14일이 지나거나 받은 사람이 담으면 사라짐 */
    handoff:{
      async put(obj){ await init(); const b=crypto.getRandomValues(new Uint8Array(18)); const code=btoa(String.fromCharCode(...b)).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
        const u=firebase.auth().currentUser; await fs.doc(`handoff/${code}`).set({d:JSON.stringify(obj),by:u?u.uid:"",at:Date.now(),exp:firebase.firestore.Timestamp.fromMillis(Date.now()+14*864e5)}); return code; },
      async get(code){ await init(); const s=await fs.doc(`handoff/${code}`).get(); if(!s.exists) return null; const x=s.data(); if(x.exp&&x.exp.toMillis&&x.exp.toMillis()<Date.now()) return null; try{ return JSON.parse(x.d); }catch(e){ return null; } },
      async del(code){ try{ await init(); await fs.doc(`handoff/${code}`).delete(); }catch(e){} }
    },
    /* 함께 읽기 숫자(2026-10-30 고침): 예전에는 숫자를 1씩 더해서, 한 기기가 여러 번 더하면 숫자가 부풀었습니다(누가복음 14–16장 하루에 194).
       이제는 그 날 문서에 '읽은 사람 표시(기기 번호)'를 하나씩 남기고 그 개수를 셉니다. 같은 기기는 몇 번을 눌러도 한 번입니다. */
    async markDone(dayKey,dateStr){ try{ await init(); const u=firebase.auth().currentUser; if(!u) return; const m={u:{[u.uid]:true}};
      await Promise.all([fs.doc(`days2/${dayKey}`).set(m,{merge:true}),fs.doc(`dates2/${dateStr}`).set(m,{merge:true})]); }catch(e){ console.warn("count",e); } },
    async counts(dayKey,dateStr){ try{ await init(); const me=(firebase.auth().currentUser||{}).uid;
      const [a,b,c]=await Promise.all([fs.doc(`days2/${dayKey}`).get(),fs.doc(`dates2/${dateStr}`).get(),fs.doc("stats/church").get()]);
      const n=x=>x.exists?Object.keys(x.data().u||{}).length:0;
      return {day:n(a),date:n(b),mine:!!(a.exists&&me&&(a.data().u||{})[me]),readers:c.exists?(c.data().readers||0):0}; }catch(e){ return null; } }
  };
  if(window.SYNC.available) init().catch(e=>console.warn("firebase",e));
  if("serviceWorker" in navigator&&location.protocol==="https:"){ window.addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));
    /* 11-20 GPT 2차: 새 판을 받았으면 알림(쓰던 글을 끊지 않도록 바로 새로 고치지 않음) */
    const had=!!navigator.serviceWorker.controller; navigator.serviceWorker.addEventListener("controllerchange",()=>{ if(!had) return; setTimeout(()=>{ try{ if(typeof window.toast==="function") window.toast("앱의 새 판을 받았습니다. 다음에 열 때 적용됩니다."); }catch(e){} },500); }); }
})();
