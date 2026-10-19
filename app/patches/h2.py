import re
s=open('template3.html').read()
i=s.index('function renderQT(){'); j=s.index('\nfunction renderQTWeek(){')
new=r'''const CLUE_LAB={turn:"꺾이는 곳",echo:"구약의 메아리",pair:"나란히 보기",scene:"닮은 장면",irony:"독자만 아는 것",aside:"글쓴이의 해설"};
function eyeFor(w,d,L){
  const k=keyOf(w,d), e=EYE[k];
  if(e) return {q:e.q,looks:e.look.map((l,i)=>`<button class="lookbtn" data-look="${i}">${esc(l.t)}</button>`)};
  const C=(CLUES[w+"-"+(d+1)]||[]).filter(c=>c.t!=="scene"||c.prev.length).slice(0,3);
  return {q:L[0].q,looks:C.map(c=>`<button class="lookbtn" data-clue="${CLUES[w+"-"+(d+1)].indexOf(c)}">${esc(CLUE_LAB[c.t]||"살펴보기")}${c.t==="pair"?` · ${esc(c.a)}와 ${esc(c.b)}`:""}</button>`),skip0:true};
}
function showLook(i){
  const e=EYE[keyOf(view.w,view.d)]; if(!e) return; const l=e.look[i]; if(!l) return;
  sheet(l.t,`<p class="vq"><b>${esc(fullRef(l.r))}</b><br>${esc(vtext(l.r))}</p><p>${esc(l.n)}</p><div class="row"><button class="btn ghost small" data-see="${l.r.join("-")}" onclick="closeSheet&&closeSheet()">본문에서 보기</button></div>`);
}
function renderQT(){
  const {w,d}=view;
  if(!BIBLE) return `<div class="loading">${bibleErr||"본문을 준비하는 중입니다…"}</div>`;
  if(isRev(d)) return renderQTWeek();
  const p=dayPlan(w,d), key=keyOf(w,d), det=DETAIL[w+"-"+(d+1)], A=dayA(w,d), q=qtOf(key);
  const traits=godTraits(A);
  const L=lensesFor(w,d), eye=eyeFor(w,d,L);
  let h=`<section class="sec"><span class="label">QT · ${dayName(w,d)}</span><h2>${esc(p.label)}</h2><p class="lead">누르며 살펴보고, 마지막에 한 줄만 적으면 됩니다. 더 깊이 하고 싶으면 맨 아래를 펼치세요.</p></section>`;
  // 1 오늘의 읽는 눈
  h+=`<section class="sec"><span class="label">1 · 오늘의 읽는 눈</span><div class="eye"><p>${esc(eye.q)}</p>${eye.looks.length?`<div class="looks">${eye.looks.join("")}</div>`:`<p class="lead">본문을 다시 훑어보며 찾아보세요.</p>`}</div></section>`;
  // 2 하나님은 어떤 분
  h+=`<section class="sec"><span class="label">2 · 하나님은 어떤 분인가</span>`;
  if(det&&det.god) h+=`<div class="qcard"><p>${esc(det.god)}</p></div>`;
  if(traits.length) traits.slice(0,det&&det.god?1:2).forEach(t=>{const v=t.verse; h+=`<div class="trait"><b>${esc(t.at.n)}</b><q>${esc(v.t)}</q><span class="lead">${esc(PLAN.abbr[v.b-1])} ${v.c}:${v.v}</span></div>`;});
  else if(!det) h+=`<p class="lead">오늘 본문에서 하나님이 하신 말씀이나 행동을 하나 찾아보세요. 그 장면에서 하나님은 어떤 분으로 보이나요?</p>`;
  h+=`</section>`;
  // 3 그리스도께로
  h+=`<section class="sec"><span class="label">3 · 그리스도께로</span><div class="qcard"><p>${esc(det&&det.christ?det.christ:(DAYC[keyOf(w,d)]||WEEKS[w-1].christ||"오늘 본문이 예수 그리스도의 이야기와 어떻게 이어지는지 생각해 보세요."))}</p></div></section>`;
  // 4 한 구절
  const vs=qtVerses(A,traits,w+"-"+(d+1));
  const vi=Math.min(q.vi||0,Math.max(0,vs.length-1)); const kv=vs[vi];
  h+=`<section class="sec"><span class="label">4 · 오늘 붙잡을 한 구절</span>`;
  if(kv) h+=`<div class="keyv"><small>${esc(PLAN.abbr[kv.b-1])} ${kv.c}:${kv.v}</small>${esc(kv.t)}</div>${vs.length>1?`<div class="row"><button class="btn ghost small" id="qtNextV">다른 구절 보기 (${vi+1}/${vs.length})</button></div>`:""}`;
  h+=`</section>`;
  // 5 한 줄 묵상
  h+=`<section class="sec"><span class="label">5 · 한 줄 묵상</span><div class="oneline"><label for="qt-med">${esc(kv?verseQuestion(kv):(det&&det.apply?det.apply:APPLY_Q))}</label><textarea id="qt-med" data-qt="med" rows="2" placeholder="오늘 말씀 앞에서 내가 기억할 한 가지">${esc(q.med||"")}</textarea></div></section>`;
  // 6 기도
  const pray=makePrayer(key,vi,q.pv,p.label,kv,traits);
  h+=`<section class="sec"><span class="label">6 · 기도</span><p class="prayer">${esc(pray)}</p><details class="mine"${q.pray?" open":""}><summary>내 기도 한 줄 더하기</summary><textarea id="qt-pray" data-qt="pray" rows="2" placeholder="나의 기도">${esc(q.pray||"")}</textarea></details>
   ${q.done?"":`<div class="row"><button class="btn" id="qtDone">QT 완료</button><span class="lead" id="qtSaved"></span></div>`}</section>`;
  if(q.done) h+=`<section class="sec" id="qtDoneSec">${qtDoneCard(w,d,kv,q)}</section>`;
  // 더 깊이
  const gap=GAPS[w+"-"+(d+1)];
  const filled=["gap","l0","l1","l2","story"].some(f=>q[f]);
  let dp=`<details class="deep" id="deepBox"${filled||view.deepOpen?" open":""}><summary>더 깊이 묵상하기<small>무대·인물·줄거리 같은 질문과 '말하지 않은 것'을 천천히 생각하고 적어 봅니다.</small></summary>`;
  if(gap) dp+=`<div class="qcard gapq"><span class="k">말하지 않은 것</span><p>${esc(gap.q)}</p><p class="clue">${esc(fullRef(gap.r))} · 성경이 일부러 비워 둔 자리입니다. 정답은 없습니다.</p><textarea data-qt="gap" placeholder="내가 생각한 빈자리">${esc(q.gap||"")}</textarea></div>`;
  L.forEach((l,i)=>{ if(i===0&&!eye.skip0&&!EYE[key]) return; const c=clueFor(l.k,A,w,d); dp+=`<div class="qcard"><span class="k">${esc(l.k)}</span><p>${esc(l.q)}</p>${c?`<p class="clue">${esc(c)}</p>`:""}<textarea data-qt="l${i}" placeholder="떠오른 생각을 짧게 적어 보세요">${esc(q["l"+i]||"")}</textarea></div>`;});
  if(q.story) dp+=`<div class="qcard"><span class="k">전에 적은 메모</span><textarea data-qt="story">${esc(q.story)}</textarea></div>`;
  if(traits.length>2) dp+=`<span class="label" style="margin-top:6px">본문에서 찾은 하나님의 성품 더 보기</span>`+traits.slice(2).map(t=>{const v=t.verse; return `<div class="trait"><b>${esc(t.at.n)}</b><q>${esc(v.t)}</q><span class="lead">${esc(PLAN.abbr[v.b-1])} ${v.c}:${v.v}${t.vs.length>1?` 외 ${t.vs.length-1}절`:""}</span></div>`;}).join("");
  dp+=`</details>`;
  h+=`<section class="sec">${dp}</section>`;
  view.qtJust=false;
  return h;
}'''
s=s[:i]+new+s[j:]
s=s.replace('''  const dn=document.getElementById("qtDone"); if(dn) dn.onclick=''','''  const db=document.getElementById("deepBox"); if(db) db.ontoggle=()=>{view.deepOpen=db.open;};
  const dn=document.getElementById("qtDone"); if(dn) dn.onclick=''',1)
# 상태 기록: 탭 바뀔 때도
s=s.replace('''  bind(); syncHlBar();''','''  bind(); syncHlBar(); if(typeof trackPos==="function"){ lastT=0; trackPos(); }''',1)
open('template3.html','w').write(s)
print('ok')
