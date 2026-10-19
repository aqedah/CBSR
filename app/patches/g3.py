import sys
F='/home/claude/rj/template3.html'
s=open(F).read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f"count {n}!={cnt} for: {old[:100]}")
    s=s.replace(old,new)

# ---- 형광펜 ----
hl=r'''
/* 형광펜: 통독표와 상관없이 절마다 저장 */
const HLKEY="cbsr-hl";
let HL={}; try{HL=JSON.parse(localStorage.getItem(HLKEY)||"{}")||{};}catch(e){}
const HSEL=new Set();
const saveHL=()=>{try{localStorage.setItem(HLKEY,JSON.stringify(HL));}catch(e){}};
const HLC={y:"노랑",g:"초록",p:"분홍",b:"파랑"};
function toggleSel(id){ if(HSEL.has(id)) HSEL.delete(id); else HSEL.add(id); const el=document.getElementById("v-"+id); if(el) el.classList.toggle("sel",HSEL.has(id)); syncHlBar(); }
function syncHlBar(){
  const bar=document.getElementById("hlbar"); if(!bar) return;
  [...HSEL].forEach(id=>{ if(!document.getElementById("v-"+id)) HSEL.delete(id); });
  if(!HSEL.size||view.tab!=="read"){ bar.hidden=true; bar.innerHTML=""; return; }
  const anyMk=[...HSEL].some(id=>HL[id]);
  bar.innerHTML=`<span class="cnt">${HSEL.size}절</span>${Object.entries(HLC).map(([k,n])=>`<button class="sw ${k}" data-mk="${k}" aria-label="${n} 형광펜"></button>`).join("")}${anyMk?`<button class="sw x" data-mk="x" aria-label="형광펜 지우기">✕</button>`:""}<button class="cl" data-mk="close">취소</button>`;
  bar.hidden=false;
  bar.querySelectorAll("[data-mk]").forEach(b=>b.onclick=()=>{ const k=b.dataset.mk;
    if(k!=="close"){ const t=Date.now(); for(const id of HSEL){ if(k==="x") delete HL[id]; else HL[id]=[k,t]; const el=document.getElementById("v-"+id); if(el){ el.className="v"+(HL[id]?" mk-"+HL[id][0]:""); } } saveHL(); }
    else for(const id of HSEL){ document.getElementById("v-"+id)?.classList.remove("sel"); }
    HSEL.clear(); syncHlBar(); });
}
'''
rep('''/* 지도 (확대·축소, 지형/위성) */''',hl+'''/* 지도 (확대·축소, 지형/위성) */''')

# ---- 나의 기록 (프로필) ----
start=s.index('/* 나의 기록 */\nfunction renderRecord(){')
end=s.index('/* 사용법 */')
prof=r'''/* 나의 기록 (프로필) */
const PROFKEY="cbsr-profile";
let PROF={}; try{PROF=JSON.parse(localStorage.getItem(PROFKEY)||"{}")||{};}catch(e){}
function readStreak(){ let p=[here.w,here.d]; if(isRev(p[1])) p=[p[0],5]; if(here.state==="before") return 0;
  const ok=(w,d)=>!!mem.done[keyOf(w,d)]; if(!ok(p[0],p[1])) p=prevDay(p[0],p[1]); return p?streakOf(ok,p[0],p[1]):0; }
function bookProgress(){ const tot={},got={}; PLAN.plan.flat().forEach(p=>p.ch.forEach(([b])=>{tot[b]=(tot[b]||0)+1;}));
  for(const k in mem.done){ const [w,d]=k.split("-").map(Number); const p=PLAN.plan[w-1]&&PLAN.plan[w-1][d]; if(p) p.ch.forEach(([b])=>{got[b]=(got[b]||0)+1;}); }
  return {tot,got}; }
function ringSVG(p){ const r=34,c=2*Math.PI*r; return `<svg width="84" height="84" viewBox="0 0 84 84" aria-hidden="true"><circle cx="42" cy="42" r="${r}" fill="none" stroke="var(--line)" stroke-width="9"/><circle cx="42" cy="42" r="${r}" fill="none" stroke="var(--accent)" stroke-width="9" stroke-linecap="round" stroke-dasharray="${(c*p/100).toFixed(1)} ${c.toFixed(1)}" transform="rotate(-90 42 42)"/></svg>`; }
function renderRecord(){
  let qd=0,s=0,t=0,perfect=0; for(const k in mem.q){const f=mem.q[k].first; if(f){qd++;s+=f.s;t+=f.t; if(mem.q[k].best&&mem.q[k].best.s===mem.q[k].best.t) perfect++;}}
  const doneN=Object.keys(mem.done).length, qtN=Object.values(mem.qt).filter(x=>x.done).length, hlN=Object.keys(HL).length;
  const rs=readStreak(), qs=(()=>{ let p=[here.w,isRev(here.d)?5:here.d]; const ok=(w,d)=>(mem.qt[keyOf(w,d)]||{}).done; if(!ok(p[0],p[1])) p=prevDay(p[0],p[1]); return p?streakOf(ok,p[0],p[1]):0; })();
  const n=chDone(), pc=+pct1(n,TOTAL_CH), sch=chScheduled();
  const nick=PROF.nick||"";
  const since=here.state==="before"?`시작까지 ${-here.diff}일`:`함께한 지 ${Math.min(here.diff+1,TOTAL_DAYS)}일째`;
  let h=`<section class="sec"><div class="prof"><div class="prof-top"><div class="avatar" aria-hidden="true">${nick?esc([...nick][0]):`<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>`}</div>
    <div class="prof-name" id="profName">${view.editNick?`<div class="acctform"><input id="nickIn" maxlength="12" value="${esc(nick)}" placeholder="불릴 이름"><button class="btn small" id="nickSave">저장</button></div>`:`<b>${nick?esc(nick):"이름을 정해 주세요"} <button class="edit" id="nickEdit">${nick?"바꾸기":"정하기"}</button></b>`}<span class="lead">${esc(PI.name)} · ${since}</span></div></div>
    <div class="ring">${ringSVG(pc)}<div class="rt"><span class="lead">성경 전체 진행률</span><b>${pct1(n,TOTAL_CH)}%</b><span class="lead">${TOTAL_CH.toLocaleString()}장 중 ${n.toLocaleString()}장 · 일정상 오늘까지 ${pct1(sch,TOTAL_CH)}%</span></div></div>
    <div class="pstats"><div class="pstat"><b>${doneN}</b><span>통독한 날 / ${READ_DAYS}</span></div><div class="pstat"><b>${rs}일</b><span>연속 통독</span></div><div class="pstat"><b>${t?pct(s,t)+"%":"–"}</b><span>퀴즈 정답률</span></div><div class="pstat"><b>${qtN}</b><span>QT 한 날</span></div><div class="pstat"><b>${qs}일</b><span>연속 QT</span></div><div class="pstat"><b>${hlN}</b><span>형광펜 절</span></div></div></div></section>`;
  // 배지
  const B=[["📖","첫 통독",doneN>=1],["7","7일 연속 통독",rs>=7],["30","통독 30일",doneN>=30],["100","통독 100일",doneN>=100],
    ["✎","첫 QT",qtN>=1],["7","QT 7일 연속",qs>=7],["★","퀴즈 만점",perfect>=1],["✓","만점 10번",perfect>=10],
    ["◐","성경 25%",pc>=25],["◑","성경 50%",pc>=50],["●","성경 100%",pc>=100],["🖍","형광펜 10절",hlN>=10]];
  const got=B.filter(b=>b[2]).length;
  h+=`<section class="sec"><span class="label">모은 배지 ${got}/${B.length}</span><div class="badges">${B.map(b=>`<div class="bdg${b[2]?" on":""}"><i>${b[0]}</i>${esc(b[1])}</div>`).join("")}</div></section>`;
  // 책별
  const {tot,got:gb}=bookProgress();
  h+=`<section class="sec"><span class="label">책별로 읽은 곳</span><div class="books">${PLAN.abbr.map((a,i)=>{const T=tot[i+1]||0,G=gb[i+1]||0,p=T?G/T*100:0; return `<div class="bk${T&&G>=T?" full":""}" title="${esc(PLAN.full[i])} ${G}/${T}장"><i style="width:${p}%"></i><span>${esc(a)}</span></div>`;}).join("")}</div><p class="lead">다 읽은 책은 진한 색으로 바뀝니다.</p></section>`;
  // 형광펜
  const hls=Object.entries(HL).sort((a,b)=>b[1][1]-a[1][1]);
  h+=`<section class="sec"><span class="label">내 형광펜</span>`;
  if(!hls.length) h+=`<p class="lead">본문을 펼쳐 마음에 닿는 절을 누르면 형광펜을 칠할 수 있습니다. 칠한 절이 여기에 모입니다.</p>`;
  else { const lim=view.hlAll?hls.length:5; h+=`<div class="hllist">${hls.slice(0,lim).map(([id,[k]])=>{const [b,c,v]=id.split("-").map(Number); const tx=BIBLE?BIBLE[b-1][c-1][v-1]:""; return `<button class="hlitem" data-hljump="${id}"><small>${esc(PLAN.abbr[b-1])} ${c}:${v} · ${HLC[k]}</small><span class="v mk-${k}">${esc(tx)}</span></button>`;}).join("")}</div>${hls.length>5&&!view.hlAll?`<button class="btn ghost small" id="hlAll">${hls.length}절 모두 보기</button>`:""}`; }
  h+=`</section>`;
  // 최근 QT
  const qtl=Object.entries(mem.qt).filter(([k,q])=>q.med||q.pray||qtStoryText(q)).map(([k,q])=>{const [w,d]=k.split("-").map(Number); return {w,d,q};}).filter(x=>PLAN.plan[x.w-1]&&PLAN.plan[x.w-1][x.d]).sort((a,b)=>dayNo(b.w,b.d)-dayNo(a.w,a.d)).slice(0,5);
  h+=`<section class="sec"><span class="label">최근 QT 노트</span>${qtl.length?qtl.map(x=>`<button class="hlitem" data-qtjump="${x.w}-${x.d}"><small>${dayName(x.w,x.d)} · ${esc(dayPlan(x.w,x.d).label)}${x.q.done?" · 완료":""}</small>${esc(x.q.med||qtStoryText(x.q)||x.q.pray)}</button>`).join(""):`<p class="lead">QT 탭에서 적은 내용이 여기에 모입니다.</p>`}</section>`;
  h+=renderAccount();
  // 주차별 점수
  let rows="";
  for(let w=NW;w>=1;w--){ const T=weekTotals(w); if(!T.n&&w!==here.w) continue;
    rows+=`<button class="trow" data-jump="${w}-${MODE==="rj"?6:0}"><span class="d">${w}주차</span><span class="r">${esc(WEEKS[w-1].t)}${T.t?`<div class="meter"><i style="width:${pct(T.s,T.t)}%"></i></div>`:""}</span><span class="s ${T.t?"":"none"}">${T.t?`${T.s}/${T.t}`:"아직"}</span></button>`; }
  h+=`<details class="more"><summary>주차별 퀴즈 점수</summary><div class="tbl">${rows}</div><p class="lead">주차를 누르면 그 주로 갑니다.</p></details>`;
  return h;
}
function bindProfile(m){
  if(view.tab!=="record") return;
  const ne=document.getElementById("nickEdit"); if(ne) ne.onclick=()=>{view.editNick=true;render();document.getElementById("nickIn")?.focus();};
  const ns=document.getElementById("nickSave"); if(ns){ const sv=()=>{PROF.nick=document.getElementById("nickIn").value.trim(); try{localStorage.setItem(PROFKEY,JSON.stringify(PROF));}catch(e){} view.editNick=false; render();}; ns.onclick=sv; document.getElementById("nickIn").onkeydown=e=>{if(e.key==="Enter")sv();}; }
  const ha=document.getElementById("hlAll"); if(ha) ha.onclick=()=>{view.hlAll=true;const y=scrollY;render();scrollTo({top:y});};
  m.querySelectorAll("[data-qtjump]").forEach(b=>b.onclick=()=>{const [w,d]=b.dataset.qtjump.split("-").map(Number); view.w=w;view.d=d;view.tab="qt";render();scrollTo({top:0});});
}

'''
s=s[:start]+prof+s[end:]

# ---- 사용법·설정 → ☰ 메뉴 ----
old_g_start=s.index('function renderGuide(){')
old_g_end=s.index('/* 그리기 */')
guide=r'''function renderGuide(){
  const rj=MODE==="rj";
  return `<section class="sec"><span class="label">통독표</span><h2>어떤 순서로 읽을까요?</h2><div class="plans" role="radiogroup">
   <button class="plan" role="radio" aria-checked="${rj}" data-plan="rj"><i class="dot"></i><b>리딩지저스 45주</b><span class="lead">한 주에 엿새 읽고 주일에는 돌아봅니다. 성경 이야기의 흐름을 따라 읽습니다.</span></button>
   <button class="plan" role="radio" aria-checked="${!rj}" data-plan="y365"><i class="dot"></i><b>365 성경통독</b><span class="lead">하루도 쉬지 않고 날마다 읽어 1년에 성경을 한 번 읽습니다. 창세기부터 요한계시록까지 차례대로 읽습니다.</span></button></div>
   <p class="lead">통독표마다 진행률·퀴즈·QT 기록이 따로 저장됩니다. 바꿔도 다른 통독표의 기록은 지워지지 않습니다. 형광펜은 함께 씁니다.</p></section>`
  +installCard("guide")+`<section class="sec guide"><span class="label">사용법</span><h2>하루 10분, 빠르게 읽고 확인하기</h2>
  <ol><li>아래 <b>오늘 통독</b>: 본문을 펼쳐 읽고, 요약·단어 설명·지도로 이해를 돕고, 퀴즈로 확인합니다. 퀴즈를 끝까지 풀거나 '오늘 통독 완료'를 누르면 진행률이 올라갑니다.</li>
  <li><b>형광펜</b>: 본문에서 절을 누르면(여러 절도 됩니다) 아래에 색이 나옵니다. 칠한 절은 '나의 기록'에 모입니다.</li>
  <li>아래 <b>QT</b>: 이야기로 읽기, 하나님의 성품, 묵상, 기도 순서로 말씀을 깊이 붙잡습니다. 칸마다 적은 내용은 이 기기에 저장됩니다.</li>
  <li>아래 <b>나의 기록</b>: 진행률, 연속 기록, 배지, 책별로 읽은 곳, 형광펜, QT 노트를 봅니다.</li>
  <li><b>지도</b>는 두 손가락으로 벌리거나 +/− 버튼으로 확대·축소합니다. 이동이 있으면 점선과 화살표로 경로를 보여 줍니다.</li>
  ${rj?`<li><b>주일</b>에는 한 주 점수를 보고 주간 도전 문제를 풉니다.</li>`:""}</ol></section>
  <section class="sec"><span class="label">설정</span><h2>통독 시작일</h2>
  <p class="lead">${rj?"1주차 1일째가 시작된 날입니다. 그날부터 엿새는 1–6일째, 일곱째 날은 주일 돌아보기로 계산합니다.":"1일째를 읽기 시작한 날입니다. 그날부터 하루에 하나씩 365일째까지 이어집니다."} 지금 설정: ${fmt(parseD(mem.start),{year:"numeric",month:"long",day:"numeric",weekday:"short"})}</p>
  <div class="row"><input type="date" id="startIn" value="${mem.start}"><button class="btn small" id="startSave">적용</button></div>
  <span class="label" style="margin-top:10px">이미 읽어 오신 분</span><p class="lead">중간부터 쓰기 시작했다면, 오늘 이전 날을 모두 읽은 것으로 표시해 진행률을 맞출 수 있습니다.</p><div class="row"><button class="btn ghost small" id="markPast">오늘 이전 날 모두 완료로 표시</button></div>
  <span class="label" style="margin-top:10px">기록 지우기</span><p class="lead">기록은 이 기기의 브라우저에만 저장됩니다.</p><div id="resetBox"><button class="btn ghost small" id="resetAsk">이 통독표의 기록 모두 지우기</button></div></section>
  ${rj?`<section class="sec"><span class="label">시험판 안내</span><p class="lead">33주차(마태복음 19장–마가복음 16장)에는 직접 만든 '생각해 보기' 문제와 QT 질문이 함께 나옵니다. 다른 날은 본문에서 자동으로 문제를 만듭니다.</p></section>`:""}`;
}
function closeMenu(){ const r=document.getElementById("drawerRoot"); if(r&&r.innerHTML){ r.innerHTML=""; document.body.style.overflow=""; } }
function openMenu(){
  const r=document.getElementById("drawerRoot");
  r.innerHTML=`<div class="drawer-bg" id="drawerBg"><aside class="drawer" role="dialog" aria-modal="true" aria-label="사용법과 설정"><div class="drawer-head"><b>사용법 · 설정</b><button class="iconbtn" id="drawerX" aria-label="닫기">✕</button></div>${renderGuide()}</aside></div>`;
  document.body.style.overflow="hidden";
  document.getElementById("drawerX").onclick=closeMenu;
  document.getElementById("drawerBg").onclick=e=>{if(e.target.id==="drawerBg")closeMenu();};
  r.querySelectorAll("[data-plan]").forEach(b=>b.onclick=()=>{ if(b.dataset.plan===MODE) return; try{localStorage.setItem("cbsr-mode",b.dataset.plan);}catch(e){} location.reload(); });
  bindInstall();
  document.getElementById("startSave").onclick=()=>{const v=document.getElementById("startIn").value; if(!v) return; mem.start=v; save(); Object.assign(here,posOfToday()); closeMenu(); go(here.w,here.d);};
  document.getElementById("markPast").onclick=()=>{ for(let w=1;w<=here.w;w++) for(let d=0;d<nd(w);d++){ if(w===here.w&&d>=here.d) break; const k=keyOf(w,d); if(!mem.done[k]) mem.done[k]="past"; } save(); closeMenu(); view.tab="record"; render(); window.scrollTo({top:0}); };
  document.getElementById("resetAsk").onclick=()=>{
    document.getElementById("resetBox").innerHTML=`<div class="confirm"><span>이 통독표의 퀴즈, 진행률, QT 기록을 모두 지울까요? 되돌릴 수 없습니다.</span><div class="row"><button class="btn small" id="resetYes">지우기</button><button class="btn ghost small" id="resetNo">취소</button></div></div>`;
    document.getElementById("resetYes").onclick=()=>{mem.q={};mem.wq={};mem.done={};mem.qt={};save();closeMenu();render();};
    document.getElementById("resetNo").onclick=()=>{closeMenu();openMenu();};
  };
}

'''
s=s[:old_g_start]+guide+s[old_g_end:]
# 이전 guide 바인딩 제거
i=s.index('  if(view.tab==="guide"){\n    document.getElementById("startSave")')
j=s.index('function applySize()')
blk=s[i:j]
s=s[:i]+"}\n"+s[j:]
# installCard: 메뉴 안에서도 동작
rep('''window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();INSTALL_EVT=e;if(view.tab==="read"||view.tab==="guide")render();});''','''window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();INSTALL_EVT=e;if(view.tab==="read")render();});''')
open(F,'w').write(s); print("ok g3"); print(blk[-200:])
