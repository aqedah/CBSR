r=open('readcode.js').read()
# church count line in done card
r=r.replace('<span>성경 ${TOTAL_CH.toLocaleString()}장 가운데 ${n.toLocaleString()}장을 읽었습니다.${n>=TOTAL_CH?" 성경 일독을 마치셨습니다!":` 남은 장은 ${(TOTAL_CH-n).toLocaleString()}장입니다.`}</span>',
 '<span>성경 ${TOTAL_CH.toLocaleString()}장 가운데 ${n.toLocaleString()}장을 읽었습니다.${n>=TOTAL_CH?" 성경 일독을 마치셨습니다!":` 남은 장은 ${(TOTAL_CH-n).toLocaleString()}장입니다.`}</span>${window.SYNC&&SYNC.available?`<span class="church" id="churchDay"></span>`:""}${window.SYNC&&SYNC.available&&!SYNC.loggedIn()?`<span class="lead">기록을 잃지 않으려면 ‘나의 기록’에서 이름을 등록하세요.</span>`:""}')
r+='''
/* ── 독립 웹앱: 기록 이어 보기와 함께 읽기 ── */
const todayStr=()=>{const d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");};
function mergeMem(a,b){
  if(!b) return a; const o=JSON.parse(JSON.stringify(a));
  if(b.start) o.start=b.start;
  o.done=Object.assign({},b.done||{},a.done||{});
  for(const f of ["q","wq"]){ o[f]=o[f]||{}; for(const k in (b[f]||{})){ const x=o[f][k], y=b[f][k]; if(!x){o[f][k]=y;continue;}
    const r={...x}; r.tries=Math.max(x.tries||0,y.tries||0);
    if(y.first&&(!x.first||(y.first.at||"9")<(x.first.at||"9"))) r.first=y.first;
    if(y.best&&(!x.best||y.best.s/y.best.t>x.best.s/x.best.t)) r.best=y.best;
    if((y.tries||0)>(x.tries||0)) r.last=y.last; o[f][k]=r; } }
  o.qt=o.qt||{}; for(const k in (b.qt||{})){ const x=o.qt[k]||{}, y=b.qt[k]; const r={...y,...x};
    for(const t of ["story","med","pray"]) r[t]=((x[t]||"").length>=(y[t]||"").length?x[t]:y[t])||"";
    r.done=!!(x.done||y.done); o.qt[k]=r; }
  return o;
}
function churchCounts(){
  if(!(window.SYNC&&SYNC.available)) return;
  const el=document.getElementById("churchDay"), el2=document.getElementById("churchBox"); if(!el&&!el2) return;
  const key=keyOf(view.w,view.d);
  SYNC.counts(key,todayStr()).then(c=>{ if(!c) return;
    if(el&&document.body.contains(el)) el.textContent=c.day>0?`이 본문을 우리 교회 ${c.day}명이 함께 읽었습니다.`:"";
    if(el2&&document.body.contains(el2)) el2.innerHTML=`<div class="stats"><div class="stat"><b>${c.date}</b><span>오늘 통독을 마친 사람</span></div><div class="stat"><b>${c.day}</b><span>이 본문을 읽은 사람</span></div><div class="stat"><b>${c.readers}</b><span>이름을 등록한 사람</span></div></div>`;
  });
}
function renderAccount(){
  if(!(window.SYNC&&SYNC.available)) return "";
  if(SYNC.loggedIn()){
    const t=SYNC.lastSaved();
    return `<section class="sec"><span class="label">기록 이어 보기</span><div class="acct"><p><b>${esc(SYNC.name())}</b>님의 기록이 저장되고 있습니다.${t?` <span class="lead">(마지막 저장 ${t.toLocaleTimeString("ko-KR",{hour:"2-digit",minute:"2-digit"})})</span>`:""}</p><p class="lead">다른 휴대폰이나 컴퓨터에서 같은 이름과 숫자 4자리를 넣으면 이 기록이 이어집니다.</p><div class="row"><button class="btn ghost small" id="acctOut">이 기기에서 나가기</button></div></div></section>
    <section class="sec"><span class="label">우리 교회 함께 읽기</span><div id="churchBox"><p class="lead">불러오는 중…</p></div></section>`;
  }
  return `<section class="sec"><span class="label">기록 이어 보기</span><div class="acct"><p>이름과 숫자 4자리를 정하면, 휴대폰을 바꾸거나 컴퓨터에서 열어도 진행률·퀴즈·QT 기록이 그대로 이어집니다. 회원 가입은 필요 없습니다.</p>
   <div class="acctform"><input id="acctName" type="text" maxlength="20" placeholder="이름 (예: 홍길동)" autocomplete="name"><input id="acctPin" type="password" inputmode="numeric" pattern="[0-9]*" maxlength="4" placeholder="숫자 4자리"><button class="btn small" id="acctIn">시작하기</button></div>
   <p class="lead">같은 이름을 쓰는 분이 있을 수 있으니, 숫자는 생일처럼 남이 짐작하기 쉬운 것은 피해 주세요. 이름과 숫자를 잊으면 기록을 다시 찾을 수 없습니다.</p><p class="lead" id="acctMsg" role="status"></p></div></section>
   <section class="sec"><span class="label">우리 교회 함께 읽기</span><div id="churchBox"><p class="lead">불러오는 중…</p></div></section>`;
}
function bindAccount(m){
  const bi=document.getElementById("acctIn");
  if(bi) bi.onclick=async()=>{ const msg=document.getElementById("acctMsg"); msg.textContent="확인하는 중…";
    try{ const remote=await SYNC.login(document.getElementById("acctName").value,document.getElementById("acctPin").value);
      const had=remote&&Object.keys(remote).length;
      mem=mergeMem(mem,remote||{}); save(); Object.assign(here,posOfToday());
      render(); const m2=document.getElementById("acctMsg"); if(m2) m2.textContent=had?"저장된 기록을 불러와 합쳤습니다.":"새로 등록했습니다. 이제부터 기록이 저장됩니다.";
    }catch(e){ msg.textContent=e.message&&/[가-힣]/.test(e.message)?e.message:"연결하지 못했습니다. 인터넷 연결을 확인하고 다시 시도해 주세요."; } };
  const bo=document.getElementById("acctOut"); if(bo) bo.onclick=()=>{ SYNC.logout(); render(); };
  churchCounts();
}
'''
open('readcode.js','w').write(r)

c=open('css3.txt').read()
c=c.replace('/*LEAFLETCSS*/','''.acct{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;gap:10px}
.acct p{margin:0}
.acctform{display:flex;gap:8px;flex-wrap:wrap}
.acctform input{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:9px 11px;flex:1 1 120px;min-width:0}
.acctform #acctPin{flex:0 1 110px;letter-spacing:.3em}
.church{font-size:14px;color:var(--ok);font-weight:600}
/*LEAFLETCSS*/''')
open('css3.txt','w').write(c)

mk=open('make3.py').read()
mk=mk.replace("print('ok7')","""s=open('template3.html').read()
rep('function save(){try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){}}','function save(){try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){} if(window.SYNC&&SYNC.loggedIn()) SYNC.push(mem);}')
rep('if(mode==="day"&&!mem.done[qz.key]){mem.done[qz.key]=new Date().toISOString().slice(0,10); view.justDone=true;}','if(mode==="day"&&!mem.done[qz.key]){mem.done[qz.key]=new Date().toISOString().slice(0,10); view.justDone=true; if(window.SYNC&&SYNC.available) SYNC.markDone(qz.key,todayStr());}')
rep('else {mem.done[k]=new Date().toISOString().slice(0,10); view.justDone=true;}','else {mem.done[k]=new Date().toISOString().slice(0,10); view.justDone=true; if(window.SYNC&&SYNC.available) SYNC.markDone(k,todayStr());}')
rep('let h=`<section class="sec"><span class="label">나의 기록</span><h2>45주 통독 여정</h2>${progressCard()}','let h=renderAccount()+`<section class="sec"><span class="label">나의 기록</span><h2>45주 통독 여정</h2>${progressCard()}')
rep('  bindQT(m);','  bindAccount(m); if(view.tab==="read") churchCounts();\\n  bindQT(m);')
rep('applySize(); render(); loadBible();','''applySize(); render(); loadBible();
if(window.SYNC&&SYNC.loggedIn()) SYNC.pull().then(remote=>{ if(remote){ mem=mergeMem(mem,remote); try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){} Object.assign(here,posOfToday()); render(); } }).catch(()=>{});
if(window.SYNC) SYNC.onChange(()=>{ if(view.tab==="record"){ const a=document.activeElement; if(!(a&&a.tagName==="INPUT")) render(); } });''')
open('template3.html','w').write(s)
print('ok8')""")
open('make3.py','w').write(mk)
print('ok')
