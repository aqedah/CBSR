/* 이야기 통독 노트 — 독립 웹앱용 기록 동기화 (Firebase: 익명 로그인 + Firestore)
   이름 + 숫자 4자리로 '열쇠'를 만들어, 같은 이름·번호를 넣은 기기끼리 기록을 이어 봅니다. */
(function(){
  "use strict";
  const cfg=window.CBSR_FIREBASE_CONFIG;
  const LOGIN="cbsr-login-v1";
  const ls={get(k,d){try{const v=localStorage.getItem(k);return v==null?d:JSON.parse(v);}catch(e){return d;}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}},del(k){try{localStorage.removeItem(k);}catch(e){}}};
  const LOGIN_ON=window.CBSR_LOGIN!==false;
  let fs=null,ready=null,login=LOGIN_ON?ls.get(LOGIN,null):null,pushT=null,lastSaved=null,listeners=[];
  const inc=n=>firebase.firestore.FieldValue.increment(n);
  function init(){ if(ready) return ready;
    ready=(async()=>{
      if(!cfg||!cfg.apiKey||!window.firebase) throw new Error("firebase-config");
      firebase.initializeApp(cfg); const auth=firebase.auth(); fs=firebase.firestore();
      if(cfg.emulator){ auth.useEmulator("http://127.0.0.1:9099"); fs.useEmulator("127.0.0.1",8080); }
      try{ await fs.enablePersistence({synchronizeTabs:true}); }catch(e){}
      try{ await auth.getRedirectResult(); }catch(e){ console.warn("redirect",e); }
      await new Promise((res,rej)=>{ let first=true; const off=auth.onAuthStateChanged(u=>{ if(u){off();res();} else if(first){ first=false; auth.signInAnonymously().catch(rej); } }); });
    })(); return ready; }
  async function keyOf(name,pin){
    const s=`cbsr|${name.replace(/\s+/g,"")}|${pin}`;
    const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(s));
    return [...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,"0")).join("");
  }
  const notify=()=>listeners.forEach(f=>{try{f();}catch(e){}});
  window.SYNC={
    available:!!(cfg&&cfg.apiKey),
    loginEnabled:LOGIN_ON,
    loggedIn:()=>!!login,
    name:()=>login?login.name:"",
    lastSaved:()=>lastSaved,
    onChange(f){listeners.push(f);},
    /* 들어가기: 서버에 있던 기록(없으면 null)을 돌려줍니다 */
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
    logout(){ login=null; ls.del(LOGIN); notify(); },
    async pull(){ if(!login) return null; await init(); const s=await fs.doc(`readers/${login.key}`).get(); if(!s.exists) return null; try{ return JSON.parse(s.data().data||"{}"); }catch(e){ return null; } },
    push(mem,wait){ if(!login) return; clearTimeout(pushT);
      pushT=setTimeout(async()=>{ try{ await init(); await fs.doc(`readers/${login.key}`).set({name:login.name,data:JSON.stringify(mem),updatedAt:Date.now()},{merge:true}); lastSaved=new Date(); notify(); }catch(e){ console.warn("sync",e); } },wait==null?1500:wait); },
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
        catch(e){ if(/popup|operation-not-supported/.test(e.code||"")) return firebase.auth().signInWithRedirect(pv); throw e; } },
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
      async who(){ if(!login) return null; if(login.pub) return login.pub; const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode("together|"+login.key)); login.pub=[...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,"0")).join("").slice(0,24); ls.set(LOGIN,login); return login.pub; },
      async put(day,doc){ const w=await this.who(); if(!w) return false; await init(); await fs.doc(`together/${day}/p/${w}`).set(doc); return true; },
      async del(day){ const w=await this.who(); if(!w) return; await init(); await fs.doc(`together/${day}/p/${w}`).delete(); },
      async list(day){ await init(); const q=await fs.collection(`together/${day}/p`).limit(300).get(); return q.docs.map(d=>({who:d.id,...d.data()})); }
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
  if("serviceWorker" in navigator&&location.protocol==="https:") window.addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));
})();
