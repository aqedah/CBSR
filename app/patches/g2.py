import sys
F='/home/claude/rj/template3.html'
s=open(F).read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f"count {n}!={cnt} for: {old[:100]}")
    s=s.replace(old,new)

rep('''const DEFAULT_START="2026-02-23";
const KEY="rjnote:v2";''','''const MODE=window.CBSR_MODE||"rj", PI=PLAN_INFO[MODE];
const DEFAULT_START=PI.start;
const KEY=MODE==="y365"?"rjnote:y365":"rjnote:v2";''')
rep('''const dateOf=(w,d)=>{''','''const NW=PLAN.plan.length, READ_DAYS=PLAN.plan.flat().length, TOTAL_DAYS=MODE==="y365"?READ_DAYS:NW*7;
const isRev=d=>MODE==="rj"&&d===6;
const nd=w=>PLAN.plan[w-1]?PLAN.plan[w-1].length:0;
const dayNo=(w,d)=>(w-1)*7+d+1;
const dayName=(w,d)=>MODE==="y365"?`${dayNo(w,d)}일째`:`${w}주차 ${d+1}일째`;
const syncKey=k=>MODE==="y365"?"y-"+k:k;
const dateOf=(w,d)=>{''')
rep('''  if(diff>=45*7) return {w:45,d:6,state:"after",diff};''','''  if(diff>=TOTAL_DAYS){ const L=TOTAL_DAYS-1; return {w:Math.floor(L/7)+1,d:L%7,state:"after",diff}; }''')

# 머리
rep('''  document.getElementById("whereLine").innerHTML=`<b>${view.w}주차</b> · ${view.d===6?"주일 · 한 주 돌아보기":(view.d+1)+"일째 · "+esc(dayPlan(view.w,view.d).label)}`;''',
'''  document.getElementById("whereLine").innerHTML=isRev(view.d)?`<b>${view.w}주차</b> · 주일 · 한 주 돌아보기`:MODE==="y365"?`<b>${dayNo(view.w,view.d)}일째</b> · ${esc(dayPlan(view.w,view.d).label)}`:`<b>${view.w}주차</b> · ${view.d+1}일째 · ${esc(dayPlan(view.w,view.d).label)}`;''')
rep('''<div class="notice">45주 통독 일정이 끝났습니다. '나의 기록'에서 한 해를 돌아보세요.</div>''','''<div class="notice">${esc(PI.name)} 일정이 끝났습니다. '나의 기록'에서 한 해를 돌아보세요.</div>''')
rep('''  for(let d=0;d<7;d++){
    const b=document.createElement("button"), dt2=dateOf(view.w,d);
    const sc=d<6?dayScore(view.w,d):mem.wq[view.w]?.first;
    b.className="day"+(d===view.d?" sel":"")+(view.w===here.w&&d===here.d&&here.state==="in"?" today":"")+(sc?" done":"");
    b.innerHTML=`<span class="dn">${DAYN[dt2.getDay()]}</span><span class="dd">${dt2.getDate()}</span><span class="ds">${sc?sc.s+"/"+sc.t:(d<6?esc(shortRef(dayPlan(view.w,d))).replace(/ .*/,""):"복습")}</span>`;
    b.setAttribute("aria-label",fmt(dt2,{month:"long",day:"numeric"})+" "+(d<6?dayPlan(view.w,d).label:"주일 돌아보기"));''',
'''  for(let d=0;d<7;d++){
    const b=document.createElement("button"), dt2=dateOf(view.w,d);
    if(!isRev(d)&&d>=nd(view.w)){ b.className="day"; b.disabled=true; b.style.visibility="hidden"; st.appendChild(b); continue; }
    const sc=!isRev(d)?dayScore(view.w,d):mem.wq[view.w]?.first;
    const dn=!isRev(d)&&mem.done[keyOf(view.w,d)];
    b.className="day"+(d===view.d?" sel":"")+(view.w===here.w&&d===here.d&&here.state==="in"?" today":"")+(sc||dn?" done":"");
    b.innerHTML=`<span class="dn">${DAYN[dt2.getDay()]}</span><span class="dd">${dt2.getDate()}</span><span class="ds">${sc?sc.s+"/"+sc.t:dn?"✓":(!isRev(d)?esc(shortRef(dayPlan(view.w,d))).replace(/ .*/,""):"복습")}</span>`;
    b.setAttribute("aria-label",fmt(dt2,{month:"long",day:"numeric"})+" "+(!isRev(d)?dayPlan(view.w,d).label:"주일 돌아보기"));''')
rep('''  document.getElementById("nextW").disabled=view.w===45;''','''  document.getElementById("nextW").disabled=view.w===NW;
  document.getElementById("planName").textContent=PI.name; document.getElementById("planSrc").textContent=PI.src;''')
rep('''  document.querySelectorAll(".tab").forEach(t=>t.setAttribute("aria-selected",t.dataset.tab===view.tab));''','''  document.querySelectorAll(".bnav .tab").forEach(t=>t.setAttribute("aria-selected",t.dataset.tab===view.tab));''')
rep('''for(let w=1;w<=here.w;w++) for(let d=0;d<6;d++){ if(w===here.w&&d>here.d) break; n+=PLAN.plan[w-1][d].ch.length; } return n; }''','''for(let w=1;w<=here.w;w++) for(let d=0;d<nd(w);d++){ if(w===here.w&&d>here.d) break; n+=PLAN.plan[w-1][d].ch.length; } return n; }''')

# 오늘 통독
rep('''  const {w,d}=view; if(d===6) return renderReview();''','''  const {w,d}=view; if(isRev(d)) return renderReview();''')
rep('''  h+=`<section class="sec"><span class="label">2 · 본문 요약</span><p class="summary">${markGloss(SUMMARY[w-1][d],b0,new Set())}</p>`;''',
'''  const sumT=(SUMMARY[w-1]||[])[d]||"";
  h+=`<section class="sec"><span class="label">2 · 본문 요약</span>${p.topic?`<p class="topic">${esc(p.topic)}</p>`:""}${sumT?`<p class="summary">${markGloss(sumT,b0,new Set())}</p>`:`<p class="lead">이 날의 요약은 준비 중입니다.</p>`}`;''')
rep('''  h+=`<details class="flow"><summary>이번 주 전체 흐름 · ${esc(WEEKS[w-1].t)}</summary><p>${esc(WEEKS[w-1].story)}</p><p style="color:var(--muted);font-size:14.5px">${esc(WEEKS[w-1].christ)}</p></details>`;''',
'''  if(WEEKS[w-1].story) h+=`<details class="flow"><summary>이번 주 전체 흐름 · ${esc(WEEKS[w-1].t)}</summary><p>${esc(WEEKS[w-1].story)}</p><p style="color:var(--muted);font-size:14.5px">${esc(WEEKS[w-1].christ)}</p></details>`;
  h+=`<section class="sec"><button class="btn toqt" data-toqt="1">QT로 이어 가기 <span aria-hidden="true">›</span></button><p class="lead" style="text-align:center">읽은 말씀을 이야기로 다시 보고, 묵상하고 기도합니다.</p></section>`;''')
# 본문 절: 형광펜
rep('''BIBLE[b-1][c-1].map((t,i)=>`<span class="v" id="v-${b}-${c}-${i+1}"><sup>${i+1}</sup>${markGloss(t,b,s2)}</span> `).join("")''',
'''BIBLE[b-1][c-1].map((t,i)=>{const id=`${b}-${c}-${i+1}`, mk=HL[id]; return `<span class="v${mk?" mk-"+mk[0]:""}${HSEL.has(id)?" sel":""}" id="v-${id}" data-v="${id}"><sup>${i+1}</sup>${markGloss(t,b,s2)}</span> `;}).join("")''')
rep('''<span>점선 밑줄 친 말을 누르면 풀이가 나옵니다.</span>''','''<span>절을 누르면 형광펜을 칠할 수 있습니다. 점선 밑줄 친 말은 풀이가 나옵니다.</span>''')

# 단서
rep('''function dayOfRef(q){ for(let w=1;w<=45;w++) for(let d=0;d<6;d++) if(''','''function dayOfRef(q){ for(let w=1;w<=NW;w++) for(let d=0;d<nd(w);d++) if(''')
rep('''data-jump="${at[0]}-${at[1]}">${at[0]}주차 ${at[1]+1}일째 · ${esc(label)}</button>`;''','''data-jump="${at[0]}-${at[1]}">${dayName(at[0],at[1])} · ${esc(label)}</button>`;''')

# QT
rep('''const QT_GOALS=[[1,"첫 QT를 마쳤습니다"],[3,"QT 3일 달성"],[7,"QT 7일 달성"],[14,"QT 14일 달성"],[30,"QT 30일 달성"],[50,"QT 50일 달성"],[100,"QT 100일 달성"],[150,"QT 150일 달성"],[200,"QT 200일 달성"],[270,"45주 QT 완주"]];''',
'''const QT_GOALS=[[1,"첫 QT를 마쳤습니다"],[3,"QT 3일 달성"],[7,"QT 7일 달성"],[14,"QT 14일 달성"],[30,"QT 30일 달성"],[50,"QT 50일 달성"],[100,"QT 100일 달성"],[150,"QT 150일 달성"],[200,"QT 200일 달성"],[300,"QT 300일 달성"]].filter(g=>g[0]<READ_DAYS).concat([[READ_DAYS,PI.short+" QT 완주"]]);''')
rep('''function qtStreak(w,d){ let n=0; while(w>=1){ if(!(mem.qt[keyOf(w,d)]||{}).done) break; n++; d--; if(d<0){w--;d=5;} } return n; }''',
'''function prevDay(w,d){ d--; if(d<0){ w--; if(w<1) return null; d=nd(w)-1; } return [w,d]; }
function streakOf(ok,w,d){ let n=0, p=[w,d]; while(p&&ok(p[0],p[1])){ n++; p=prevDay(p[0],p[1]); } return n; }
function qtStreak(w,d){ return streakOf((a,b)=>(mem.qt[keyOf(a,b)]||{}).done,w,d); }''')
rep('''  const stamps=[0,1,2,3,4,5].map(i=>''','''  const stamps=Array.from({length:nd(w)},(_,i)=>i).map(i=>''')
rep('''<p class="lead" style="margin:6px 0 0">${w}주차 QT 도장''','''<p class="lead" style="margin:6px 0 0">이번 주 QT 도장''')
rep('''  if(/줄거리|편지 뒤|시간/.test(k)) return "요약 다시 보기: "+SUMMARY[w-1][d].split(/(?<=다\\.)\\s/)[0];''','''  if(/줄거리|편지 뒤|시간/.test(k)&&(SUMMARY[w-1]||[])[d]) return "요약 다시 보기: "+SUMMARY[w-1][d].split(/(?<=다\\.)\\s/)[0];''')
rep('''  if(d===6) return renderQTWeek();''','''  if(isRev(d)) return renderQTWeek();''')
rep('''<span class="label">QT · ${w}주차 ${d+1}일째</span>''','''<span class="label">QT · ${dayName(w,d)}</span>''')
rep('''  if(gap) h+=`<div class="qcard gapq"><span class="k">말하지 않은 것</span><p>${esc(gap.q)}</p><p class="clue">${esc(fullRef(gap.r))} · 성경이 일부러 비워 둔 자리입니다. 정답은 없습니다.</p></div>`;
  L.forEach(l=>{const c=clueFor(l.k,A,w,d); h+=`<div class="qcard"><span class="k">${esc(l.k)}</span><p>${esc(l.q)}</p>${c?`<p class="clue">${esc(c)}</p>`:""}</div>`;});
  h+=`<textarea id="qt-story" data-qt="story" placeholder="이야기를 읽으며 떠오른 생각을 짧게 적어 보세요">${esc(q.story||"")}</textarea></section>`;''',
'''  if(gap) h+=`<div class="qcard gapq"><span class="k">말하지 않은 것</span><p>${esc(gap.q)}</p><p class="clue">${esc(fullRef(gap.r))} · 성경이 일부러 비워 둔 자리입니다. 정답은 없습니다.</p><textarea data-qt="gap" placeholder="내가 생각한 빈자리">${esc(q.gap||"")}</textarea></div>`;
  L.forEach((l,i)=>{const c=clueFor(l.k,A,w,d); h+=`<div class="qcard"><span class="k">${esc(l.k)}</span><p>${esc(l.q)}</p>${c?`<p class="clue">${esc(c)}</p>`:""}<textarea data-qt="l${i}" placeholder="떠오른 생각을 짧게 적어 보세요">${esc(q["l"+i]||"")}</textarea></div>`;});
  if(q.story) h+=`<div class="qcard"><span class="k">전에 적은 메모</span><textarea data-qt="story">${esc(q.story)}</textarea></div>`;
  h+=`</section>`;''')
rep('''<p>${esc(det&&det.christ?det.christ:WEEKS[w-1].christ)}</p></div></section>`;''','''<p>${esc(det&&det.christ?det.christ:(DAYC[keyOf(w,d)]||WEEKS[w-1].christ||"오늘 본문이 예수 그리스도의 이야기와 어떻게 이어지는지 생각해 보세요."))}</p></div></section>`;''')
rep('''    if(q&&(q.story||q.med||q.pray)){ any=true; h+=`<div class="qcard"><span class="k">${d+1}일째 · ${esc(p.label)}${q.done?" · 완료":""}</span>${q.story?`<p>${esc(q.story)}</p>`:""}''',
'''    const st=qtStoryText(q);
    if(q&&(st||q.med||q.pray)){ any=true; h+=`<div class="qcard"><span class="k">${d+1}일째 · ${esc(p.label)}${q.done?" · 완료":""}</span>${st?`<p>${esc(st)}</p>`:""}''')
rep('''function renderQTWeek(){''','''const qtStoryText=q=>q?[q.gap,q.l0,q.l1,q.l2,q.story].filter(Boolean).join(" / "):"";
function renderQTWeek(){''')
rep('''  if(view.tab!=="qt"||view.d===6) return;''','''  if(view.tab!=="qt"||isRev(view.d)) return;''')
rep('''    for(const t of ["story","med","pray"]) r[t]''','''    for(const t of ["story","med","pray","gap","l0","l1","l2"]) r[t]''')

# 동기화 열쇠
rep('''SYNC.markDone(qz.key,todayStr())''','''SYNC.markDone(syncKey(qz.key),todayStr())''')
rep('''SYNC.markDone(k,todayStr())''','''SYNC.markDone(syncKey(k),todayStr())''')
rep('''  SYNC.counts(key,todayStr()).then''','''  SYNC.counts(syncKey(key),todayStr()).then''')

# 퀴즈·주간
rep('''${mode==="day"?`<button class="btn ghost" data-goweek="1">이번 주 기록 보기</button>`:""}''','''${mode==="day"&&MODE==="rj"?`<button class="btn ghost" data-goweek="1">이번 주 기록 보기</button>`:""}''')
rep('''    for(let dd=0;dd<6;dd++){ const A=dayA(w,dd);''','''    for(let dd=0;dd<nd(w);dd++){ const A=dayA(w,dd);''')
rep('''  let s=0,t=0,n=0; for(let d=0;d<6;d++){const f=dayScore(w,d);''','''  let s=0,t=0,n=0; for(let d=0;d<nd(w);d++){const f=dayScore(w,d);''')

# 그리기
rep('''  m.innerHTML=view.tab==="read"?renderRead():view.tab==="qt"?renderQT():view.tab==="record"?renderRecord():renderGuide();
  bind();
  if(view.tab==="read"&&view.d<6&&BIBLE)''','''  if(view.tab==="guide") view.tab="read";
  m.innerHTML=view.tab==="read"?renderRead():view.tab==="qt"?renderQT():renderRecord();
  bind(); syncHlBar();
  if(view.tab==="read"&&!isRev(view.d)&&BIBLE)''')
rep('''if(view.d===6){const dd=PLAN.plan[view.w-1].findIndex''','''if(isRev(view.d)){const dd=PLAN.plan[view.w-1].findIndex''')
rep('''  const tqt=document.getElementById("toQT"); if(tqt) tqt.onclick=()=>{view.tab="qt";render();window.scrollTo({top:0});};''',
'''  const toQT=()=>{view.tab="qt";render();window.scrollTo({top:0});};
  const tqt=document.getElementById("toQT"); if(tqt) tqt.onclick=toQT;
  m.querySelectorAll("[data-toqt]").forEach(b=>b.onclick=toQT);
  m.querySelectorAll(".v[data-v]").forEach(el=>el.onclick=e=>{ if(e.target.closest(".g")) return; toggleSel(el.dataset.v); });
  m.querySelectorAll("[data-hljump]").forEach(b=>b.onclick=()=>{const [bb,c,v]=b.dataset.hljump.split("-").map(Number); const at=dayOfRef([bb,c,v]); if(!at) return; view.w=at[0]; view.d=at[1]; view.tab="read"; seeVerse(bb,c,v);});
  bindProfile(m);''')

# 주 이동
rep('''document.getElementById("prevW").onclick=()=>{if(view.w>1){view.w--;view.quiz=null;view.wquiz=null;view.open=false;render();}};
document.getElementById("nextW").onclick=()=>{if(view.w<45){view.w++;view.quiz=null;view.wquiz=null;view.open=false;render();}};''',
'''const fixD=()=>{ if(!isRev(view.d)&&view.d>=nd(view.w)) view.d=nd(view.w)-1; };
document.getElementById("prevW").onclick=()=>{if(view.w>1){view.w--;fixD();view.quiz=null;view.wquiz=null;view.open=false;render();}};
document.getElementById("nextW").onclick=()=>{if(view.w<NW){view.w++;fixD();view.quiz=null;view.wquiz=null;view.open=false;render();}};
document.getElementById("menuBtn").onclick=openMenu;''')
rep('''document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{view.tab=t.dataset.tab;render();});
document.addEventListener("keydown",e=>{if(e.key==="Escape")document.getElementById("sheetRoot").innerHTML="";});''',
'''document.querySelectorAll(".bnav .tab").forEach(t=>t.onclick=()=>{const same=view.tab===t.dataset.tab; view.tab=t.dataset.tab; HSEL.clear(); render(); window.scrollTo({top:0,behavior:same?"smooth":"auto"});});
document.addEventListener("keydown",e=>{if(e.key==="Escape"){document.getElementById("sheetRoot").innerHTML=""; closeMenu();}});''')
open(F,'w').write(s); print("ok g2")
