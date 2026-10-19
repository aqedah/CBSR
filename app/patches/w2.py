p='/home/claude/rj/template3.html'; s=open(p).read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)>=1, a[:80]; s=s.replace(a,b,cnt)
# 주 점수(날짜 목록)
rep('''function weekTotals(w){''','''function weekTotalsList(L){ let s=0,t=0,n=0; for(const [w,d] of L){const f=dayScore(w,d); if(f){s+=f.s;t+=f.t;n++;}} return {s,t,n}; }
function weekTotals(w){''')
# 읽기·QT 화면 갈래
rep('''function renderRead(){
  const {w,d}=view; if(isRev(d)) return renderReview();''','''function renderRead(){
  if(view.pre) return renderPreview();
  if(view.revW) return renderReview365(view.revW);
  const {w,d}=view; if(isRev(d)) return renderReview();''')
rep('''  if(isRev(d)) return renderQTWeek();''','''  if(view.pre) return renderPreview();
  if(view.revW) return renderQTWeek(weekDays(view.revW),dispTitle(view.revW));
  if(isRev(d)) return renderQTWeek();''')
# QT 한 주 돌아보기: 날짜 목록도 받기
rep('''function renderQTWeek(){
  const w=view.w; let h=`<section class="sec"><span class="label">QT · 한 주 돌아보기</span><h2>${w}주차 ${esc(WEEKS[w-1].t)}</h2><p class="lead">이번 주에 적은 묵상과 기도를 다시 읽어 보세요.</p></section>`;
  let any=false;
  for(let d=0;d<6;d++){ const q=mem.qt[keyOf(w,d)]; const p=dayPlan(w,d);''','''function renderQTWeek(list,title){
  const w=view.w; const L=list||[0,1,2,3,4,5].map(d=>[w,d]);
  let h=`<section class="sec"><span class="label">QT · 한 주 돌아보기</span><h2>${esc(title||`${w}주차 ${WEEKS[w-1].t}`)}</h2><p class="lead">이번 주에 적은 묵상과 기도를 다시 읽어 보세요.</p></section>`;
  let any=false;
  for(const [ww,d] of L){ const q=mem.qt[keyOf(ww,d)]; const p=dayPlan(ww,d);''')
rep('''if(q&&(st||q.med||q.pray)){ any=true; h+=`<div class="qcard"><span class="k">${d+1}일째 · ${esc(p.label)}''','''if(q&&(st||q.med||q.pray)){ any=true; h+=`<div class="qcard"><span class="k">${esc(dayName(ww,d).replace(/^\\d+주차 /,""))} · ${esc(p.label)}''')
# 주간 도전 문제: 365 돌아보기는 달력 주의 날들로
rep('''    const qs=[]; const base=(Date.now()^Math.floor(Math.random()*1e9))>>>0;
    for(let dd=0;dd<nd(w);dd++){ const A=dayA(w,dd); const one=makeQuiz(A,CTX,base+dd*7919,{nOX:dd%2?0:1,nMC:dd%2?1:0}); if(one[0]) qs.push(one[0]); }
    view.wquiz={key:String(w),qs,i:0,first:[],state:{wrong:[],solved:false}};''','''    const qs=[]; const base=(Date.now()^Math.floor(Math.random()*1e9))>>>0;
    const L=view.revW?weekDays(view.revW):[...Array(nd(w)).keys()].map(dd=>[w,dd]);
    L.forEach(([ww,dd],k)=>{ const A=dayA(ww,dd); const one=makeQuiz(A,CTX,base+k*7919,{nOX:k%2?0:1,nMC:k%2?1:0}); if(one[0]) qs.push(one[0]); });
    view.wquiz={key:view.revW?"c"+view.revW:String(w),qs,i:0,first:[],state:{wrong:[],solved:false}};''')
# 새 화면들
new=r'''
/* 리딩지저스 시작 주일: 45주 여정 미리 보기 */
function renderPreview(){
  const W=WEEKS[0];
  let h=`<section class="sec"><span class="label">시작 주일</span><h2>45주 이야기 통독을 시작합니다</h2><p class="lead">월요일부터 토요일까지 날마다 정해진 본문을 읽고, 주일에는 지난 한 주를 돌아봅니다. 오늘은 첫 주를 미리 살펴보는 날입니다.</p></section>`;
  h+=`<section class="sec"><span class="label">1주차 미리 보기 · ${esc(W.t)}</span>${W.story?`<details class="where" open><summary><span class="k">이번 주 이야기</span></summary><p>${esc(W.story)}</p>${W.christ?`<p class="c">${esc(W.christ)}</p>`:""}</details>`:""}<div class="tbl">`;
  for(let d=0;d<6;d++){ const p=dayPlan(1,d), dt=dateOf(1,d); h+=`<button class="trow" data-jump="1-${d}"><span class="d">${DAYN[dt.getDay()]}</span><span class="r">${esc(p.label)}${GUIDE[keyOf(1,d)]?`<div class="lead" style="font-size:13px">${esc(GUIDE[keyOf(1,d)].today)}</div>`:""}</span><span class="s none">›</span></button>`; }
  h+=`</div></section><section class="sec"><button class="btn" data-jump="1-0" style="width:100%;padding:14px">첫날 본문 보기 · ${esc(dayPlan(1,0).label)}</button></section>`;
  return h;
}
/* 365: 달력 한 주(주일~토요일) 돌아보기 */
function renderReview365(W){
  const L=weekDays(W), T=weekTotalsList(L);
  const a=cellOf(W,0).dt, z=cellOf(W,6).dt;
  let h=`<section class="sec"><span class="label">한 주 돌아보기 · ${fmt(a,{month:"numeric",day:"numeric"})} – ${fmt(z,{month:"numeric",day:"numeric"})}</span><h2>${esc(dispTitle(W))}</h2></section>`;
  h+=`<section class="sec"><span class="label">이번 주 퀴즈 성적</span><div class="tbl">`;
  for(const [w,d] of L){ const f=dayScore(w,d), p=dayPlan(w,d), dt=dateOf(w,d), dn=mem.done[keyOf(w,d)];
    h+=`<button class="trow" data-jump="${w}-${d}"><span class="d">${DAYN[dt.getDay()]}</span><span class="r">${esc(p.label)}${f?`<div class="meter"><i style="width:${pct(f.s,f.t)}%"></i></div>`:""}</span><span class="s ${f?"":"none"}">${f?`${f.s}/${f.t}`:dn?"✓":"아직"}</span></button>`; }
  const [g,msg]=T.t?grade(T.s,T.t):["아직 시작 전","이번 주 날마다 퀴즈를 풀면 여기에 점수가 모입니다."];
  h+=`<div class="total"><span>${T.n}일 참여${T.t?` · 정답률 ${pct(T.s,T.t)}%`:""}</span><span class="big">${T.s} / ${T.t}</span></div></div>
   <div class="score"><span class="badge">${g}</span><p class="lead">${msg}${T.n&&T.n<L.length?` 아직 ${L.length-T.n}일이 남아 있어요. 놓친 날도 지금 풀 수 있습니다.`:""}</p></div></section>`;
  if(BIBLE) h+=`<section class="sec"><span class="label">주간 도전 문제</span>${renderQuiz("c"+W,null,"week")}</section>`;
  h+=`<section class="sec"><span class="label">이번 주 이야기 다시 보기</span><div class="sumlist">`;
  for(const [w,d] of L) h+=`<details><summary>${DAYN[dateOf(w,d).getDay()]} · ${esc(dayPlan(w,d).label)}</summary><p>${esc((SUMMARY[w-1]||[])[d]||"")}</p></details>`;
  h+=`</div></section>`+nextPreview(W);
  return h;
}
/* 다음 주 미리 보기 (두 통독표 공통) */
function nextPreview(W){
  const N=NDW(); if(W>=N) return "";
  const L=weekDays(W+1); if(!L.length) return "";
  const [w,d]=L[0]; let story="";
  if(MODE==="rj"&&WEEKS[w-1]&&WEEKS[w-1].story) story=WEEKS[w-1].story.split(/(?<=[다요]\.)\s+/)[0];
  else if(GUIDE[keyOf(w,d)]) story=GUIDE[keyOf(w,d)].today;
  return `<section class="sec"><span class="label">다음 주 미리 보기</span><div class="qcard"><span class="k">${esc(dispTitle(W+1))}</span>${story?`<p>${esc(story)}</p>`:""}<div class="row"><button class="btn ghost small" data-jump="${w}-${d}">다음 주 첫날 · ${esc(dayPlan(w,d).label)}</button></div></div></section>`;
}
'''
rep('/* 리딩지저스 시작 주일','/* 리딩지저스 시작 주일') if '/* 리딩지저스 시작 주일' in s else None
rep('function renderReview(){',new+'function renderReview(){')
# 리딩지저스 주일 돌아보기 끝에 다음 주 미리 보기
i=s.index('function renderReview(){'); j=s.index('\n}\n',i)
blk=s[i:j]
assert blk.rstrip().endswith('return h+`</div></section>`;')
blk=blk.rstrip()[:-len('return h+`</div></section>`;')]+'return h+`</div></section>`+nextPreview(weekOfDay(w,6));'
s=s[:i]+blk+s[j:]
# 365 토요일(또는 마지막 날) 끝에 돌아보기 안내
rep('''  h+=`<section class="sec"><button class="btn toqt" data-toqt="1">''','''  if(MODE==="y365"&&(dateOf(w,d).getDay()===6||dayNo(w,d)===READ_DAYS)) h+=`<section class="sec"><div class="qcard"><span class="k">한 주를 마무리하는 날</span><p>이번 주 읽은 본문을 돌아보고 주간 도전 문제를 풀어 보세요.</p><div class="row"><button class="btn small" id="toRev">이번 주 돌아보기 ›</button></div></div></section>`;
  h+=`<section class="sec"><button class="btn toqt" data-toqt="1">''')
rep('''  m.querySelectorAll("[data-toqt]").forEach(b=>b.onclick=toQT);''','''  m.querySelectorAll("[data-toqt]").forEach(b=>b.onclick=toQT);
  const trv=document.getElementById("toRev"); if(trv) trv.onclick=()=>{ view.revW=dispW(); view.quiz=null; view.wquiz=null; render(); window.scrollTo({top:0}); };''')
# 이어 읽기 기록: 특별 화면은 건너뛰기
rep('''  if(isRev(view.d)) return;
  const L={w:view.w''','''  if(isRev(view.d)||view.pre||view.revW) return;
  const L={w:view.w''')
# 시작 주일이 오늘이면 미리 보기로 열기
rep('''applySize(); render(); loadBible();''','''try{ if(hasPre()&&dayDiff(cellOf(1,0).dt,today0())===0) view.pre=true; }catch(e){}
applySize(); render(); loadBible();''')
rep('</style>','''.day.pre .ds{color:var(--gold);font-weight:700}
.revchip{display:flex;align-items:center;gap:8px;width:100%;margin-top:8px;font:inherit;text-align:left;background:var(--card);border:1px dashed var(--accent);border-radius:10px;padding:9px 12px;color:var(--accent);cursor:pointer}
.revchip span{font-weight:700;font-size:14px}
.revchip small{flex:1;color:var(--muted);font-size:12.5px}
.revchip.on{background:var(--accent);color:var(--accent-ink);border-style:solid}
.revchip.on small{color:var(--accent-ink);opacity:.85}
</style>''')
open(p,'w').write(s); print("ok")
