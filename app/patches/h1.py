s=open('template3.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)>=1, a[:80]
    s=s.replace(a,b,n)

# ---------- CSS ----------
css='''.chips{gap:8px}
.chip{font-size:14.5px;padding:8px 14px;min-height:38px;display:inline-flex;align-items:center;gap:4px}
details.where{background:var(--accent-soft);border-radius:12px;padding:12px 14px}
details.where summary{cursor:pointer;list-style:none;display:grid;gap:3px}
details.where summary::-webkit-details-marker{display:none}
details.where .k{font-size:12px;font-weight:700;color:var(--accent);letter-spacing:.04em}
details.where .t{font-family:var(--f-text);font-size:15.5px;line-height:1.6}
details.where .more{font-size:12.5px;color:var(--accent);font-weight:600}
details.where[open] .more{display:none}
details.where p{margin:8px 0 0;font-family:var(--f-text);font-size:15px;line-height:1.7}
details.where p.c{color:var(--muted);font-size:14.5px}
.guide30{background:var(--card);border:1px solid var(--gold);border-radius:12px;padding:12px 14px;display:grid;gap:8px}
.guide30 .k{font-size:12px;font-weight:700;color:var(--gold);letter-spacing:.04em}
.guide30 dl{margin:0;display:grid;gap:7px}
.guide30 dt{font-size:12px;font-weight:700;color:var(--muted)}
.guide30 dd{margin:0;font-size:15px;line-height:1.6}
.guide30 dd.find{color:var(--accent);font-weight:600}
.mapfold{width:100%;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 14px;display:grid;gap:4px;font:inherit;color:var(--ink);cursor:pointer}
.mapfold b{color:var(--accent);margin-right:6px;font-size:13px}
.mapfold .go{font-size:13px;color:var(--accent);font-weight:600}
.resume{display:flex;align-items:center;gap:10px;background:var(--gold-soft);border-radius:12px;padding:10px 12px}
.resume .t{flex:1;min-width:0;font-size:14px;line-height:1.45}
.resume .t small{display:block;color:var(--gold);font-weight:700;font-size:12px}
.resume .x{border:0;background:none;color:var(--muted);font-size:16px;padding:6px;cursor:pointer}
.eye{background:var(--card);border:1px solid var(--accent);border-radius:12px;padding:14px 16px;display:grid;gap:10px}
.eye>p{margin:0;font-family:var(--f-text);font-size:17px;line-height:1.65}
.looks{display:grid;gap:8px}
.lookbtn{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;text-align:left;font:inherit;font-size:15px;font-weight:600;color:var(--accent);background:var(--accent-soft);border:0;border-radius:10px;padding:12px 14px;min-height:46px;cursor:pointer}
.lookbtn::after{content:"›";font-size:18px}
.oneline{display:grid;gap:6px}
.oneline label{font-size:14px;color:var(--muted)}
.oneline textarea{min-height:52px}
details.deep{background:var(--card);border:1px dashed var(--accent);border-radius:12px;padding:12px 14px}
details.deep>summary{cursor:pointer;font-weight:700;color:var(--accent);font-size:15px}
details.deep>summary small{display:block;font-weight:400;color:var(--muted);font-size:13px;margin-top:2px}
details.deep[open]>summary{margin-bottom:10px}
details.deep .sec{margin-top:12px}
details.mine{font-size:14px}
details.mine summary{cursor:pointer;color:var(--accent);font-weight:600;padding:6px 0}
'''
rep('</style>',css+'</style>')

# ---------- 읽기 탭 ----------
helpers=r'''
/* 지금 어디쯤 · 30초 길잡이 · 이어 읽기 */
function whereCard(p,w){
  let W=null;
  if(MODE==="rj") W=WEEKS[w-1];
  else { const [b,c]=p.ch[0]; const i=RJ_PLAN.findIndex(wk=>wk.some(dd=>dd.ch.some(x=>x[0]===b&&x[1]===c))); if(i>=0) W=RJ_WEEKS[i]; }
  if(!W||!W.story) return "";
  const ss=W.story.split(/(?<=[다요]\.)\s+/), first=ss[0], rest=ss.slice(1).join(" ");
  return `<details class="where"><summary><span class="k">지금 성경 이야기의 어디쯤?</span><span class="t">${esc(first)}</span><span class="more">더 보기 ›</span></summary>${rest?`<p>${esc(rest)}</p>`:""}${W.christ?`<p class="c">${esc(W.christ)}</p>`:""}</details>`;
}
function guideCard(k){ const g=GUIDE[k]; if(!g) return "";
  return `<div class="guide30"><span class="k">읽기 전 30초 길잡이</span><dl><dt>지난 이야기</dt><dd>${esc(g.prev)}</dd><dt>오늘 이야기</dt><dd>${esc(g.today)}</dd><dt>읽으면서 찾기</dt><dd class="find">${esc(g.find)}</dd></dl></div>`; }
const RESUME=(()=>{ const r=mem.last; if(!r||!r.w) return null; if(Date.now()-(r.at||0)>1000*60*60*24*10) return null; return r; })();
let resumeShow=!!RESUME;
function resumeCard(){
  if(!resumeShow||!RESUME) return "";
  const r=RESUME; if(!PLAN.plan[r.w-1]||!PLAN.plan[r.w-1][r.d]) return "";
  let t="";
  if(r.tab==="qt") t=`<small>QT 이어 하기</small>${esc(dayPlan(r.w,r.d).label)}`;
  else if(r.v){ const [b,c,v]=r.v.split("-").map(Number); const p=dayPlan(r.w,r.d); if(p.ch[0][0]===b&&p.ch[0][1]===c&&v<=2) return ""; t=`<small>지난번 읽던 곳</small>${esc(PLAN.full[b-1])} ${c}${b===19?"편":"장"} ${v}절`; }
  else return "";
  return `<div class="resume"><span class="t">${t}</span><button class="btn small" id="resumeGo">이어 하기</button><button class="x" id="resumeX" aria-label="닫기">✕</button></div>`;
}
let lastT=0;
function trackPos(){
  const now=Date.now(); if(now-lastT<700) return; lastT=now;
  if(isRev(view.d)) return;
  const L={w:view.w,d:view.d,tab:view.tab,at:now};
  if(view.tab==="read"&&view.open){ const vs=document.querySelectorAll("#bible .v"); for(const el of vs){ if(el.getBoundingClientRect().top>=70){ L.v=el.dataset.v; break; } } }
  if(view.tab==="record") return;
  if(view.tab==="read"&&!L.v){ const o=mem.last; if(o&&o.w===L.w&&o.d===L.d&&o.v) L.v=o.v; }
  mem.last=L; try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){}
}
window.addEventListener("scroll",trackPos,{passive:true});
'''
rep('/* 사용법 */',helpers+'/* 사용법 */')
rep('  let h=installCard("read")+progressMini();\n','  let h=installCard("read")+resumeCard()+progressMini()+whereCard(p,w);\n')
rep('''  h+=`<section class="sec" id="textSec"><span class="label">1 · 오늘 본문</span><h2>${esc(p.label)}</h2>
   <div class="steps">''','''  h+=`<section class="sec" id="textSec"><span class="label">1 · 오늘 본문</span><h2>${esc(p.label)}</h2>${guideCard(key)}
   <div class="steps">''')
rep('''  if(WEEKS[w-1].story) h+=`<details class="flow"><summary>이번 주 전체 흐름 · ${esc(WEEKS[w-1].t)}</summary><p>${esc(WEEKS[w-1].story)}</p><p style="color:var(--muted);font-size:14.5px">${esc(WEEKS[w-1].christ)}</p></details>`;\n''','')
# 지도 접기
rep('''  if(!pts.length&&!R.length) return `<section class="sec"><span class="label">4 · 지도</span><p class="lead">오늘 본문에는 지도에 표시할 장소가 나오지 않습니다.</p></section>`;''',
'''  if(!pts.length&&!R.length) return `<section class="sec"><span class="label">4 · 지도</span><p class="lead">오늘 본문에는 지도에 표시할 장소가 나오지 않습니다.</p></section>`;
  if(!view.mapOpen){ const names=pts.slice().sort((a,b)=>b.n-a.n).map(p=>p.name); const mv=R.map(r=>r.p.map(q=>q[0]).filter(Boolean).join(" → ")).filter(Boolean);
    return `<section class="sec"><span class="label">4 · 지도</span><button class="mapfold" id="mapOpen"><span>${mv.length?`<b>오늘의 이동</b>${esc(mv[0])}`:`<b>오늘 나오는 곳</b>${esc(names.slice(0,5).join(", "))}${names.length>5?` 외 ${names.length-5}곳`:""}`}</span>${mv.length&&names.length?`<span class="lead">나오는 곳 ${names.length}곳</span>`:""}<span class="go">지도 펼치기 ›</span></button></section>`; }''')
rep('''<div class="cap"><span>오늘 본문에 나오는 곳''','''<div class="cap"><button class="btn ghost small" id="mapClose">지도 접기</button><span>오늘 본문에 나오는 곳''')
rep('''  if(view.tab==="read"&&!isRev(view.d)&&BIBLE) initMap(dayA(view.w,view.d)); else destroyMap();''','''  if(view.tab==="read"&&!isRev(view.d)&&BIBLE&&view.mapOpen) initMap(dayA(view.w,view.d)); else destroyMap();''')
# 바인딩
rep('''  m.querySelectorAll("[data-toqt]").forEach(b=>b.onclick=toQT);''','''  m.querySelectorAll("[data-toqt]").forEach(b=>b.onclick=toQT);
  const mo=document.getElementById("mapOpen"); if(mo) mo.onclick=()=>{ view.mapOpen=true; const y=window.scrollY; render(); window.scrollTo({top:y}); };
  const mc=document.getElementById("mapClose"); if(mc) mc.onclick=()=>{ view.mapOpen=false; const y=window.scrollY; render(); window.scrollTo({top:y}); };
  const rg=document.getElementById("resumeGo"); if(rg) rg.onclick=()=>{ const r=RESUME; resumeShow=false; view.w=r.w; view.d=r.d; view.quiz=null; view.wquiz=null;
    if(r.tab==="qt"){ view.tab="qt"; render(); window.scrollTo({top:0}); return; }
    view.tab="read"; view.open=true; render(); const el=document.getElementById("v-"+r.v); if(el){ el.scrollIntoView({block:"center"}); el.classList.add("hl"); setTimeout(()=>el.classList.remove("hl"),2600);} };
  const rx=document.getElementById("resumeX"); if(rx) rx.onclick=()=>{ resumeShow=false; const y=window.scrollY; render(); window.scrollTo({top:y}); };
  m.querySelectorAll("[data-look]").forEach(b=>b.onclick=()=>showLook(+b.dataset.look));''')
open('template3.html','w').write(s)
print("ok")
