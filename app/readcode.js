/* 진행률 */
const TOTAL_CH=PLAN.plan.flat().reduce((a,p)=>a+p.ch.length,0);
function chDone(){ let n=0; for(const k in mem.done){ const [w,d]=k.split("-").map(Number); if(PLAN.plan[w-1]&&PLAN.plan[w-1][d]) n+=PLAN.plan[w-1][d].ch.length; } return n; }
function chScheduled(){ if(here.state==="before") return 0; let n=0; for(let w=1;w<=here.w;w++) for(let d=0;d<6;d++){ if(w===here.w&&d>here.d) break; n+=PLAN.plan[w-1][d].ch.length; } return n; }
const pct1=(a,b)=>b?(a/b*100).toFixed(1):"0.0";
function progressCard(){
  const n=chDone(), s=chScheduled();
  return `<div class="prog"><div class="top"><span>성경 전체 진행률</span><b>${pct1(n,TOTAL_CH)}%</b></div><div class="bar" aria-hidden="true"><i style="width:${pct1(n,TOTAL_CH)}%"></i><u style="left:${pct1(s,TOTAL_CH)}%"></u></div><span class="lead">${TOTAL_CH.toLocaleString()}장 가운데 ${n.toLocaleString()}장을 읽었습니다. 노란 선은 일정상 오늘까지 읽을 분량(${pct1(s,TOTAL_CH)}%)입니다.</span></div>`;
}

function progressMini(){
  const n=chDone();
  return `<div class="pmini" role="button" tabindex="0" id="pmini" aria-label="자세한 기록 보기"><span>진행률 <b>${pct1(n,TOTAL_CH)}%</b></span><span class="bar" aria-hidden="true"><i style="width:${pct1(n,TOTAL_CH)}%"></i></span><span class="more">기록 ›</span></div>`;
}
/* 오늘 통독 */
function renderRead(){
  const {w,d}=view; if(d===6) return renderReview();
  const p=dayPlan(w,d), key=keyOf(w,d), b0=p.ch[0][0];
  if(!BIBLE) return `<div class="loading">${bibleErr||"본문을 준비하는 중입니다…"}</div>`;
  const A=dayA(w,d), sc=dayScore(w,d), done=!!mem.done[key];
  const mins=Math.max(5,Math.round(A.text.length/450));
  let h=installCard("read")+progressMini();
  // 1 본문
  h+=`<section class="sec" id="textSec"><span class="label">1 · 오늘 본문</span><h2>${esc(p.label)}</h2>
   <div class="steps"><span class="step on">약 ${mins}분</span><span class="step ${view.open?"on":""}">본문</span><span class="step ${sc?"on":""}">퀴즈${sc?` ${sc.s}/${sc.t}`:""}</span><span class="step ${done?"on":""}">통독 완료</span></div>`;
  if(!view.open){
    h+=`<button class="openbtn" id="openText">본문 펼치기 · ${p.ch.length}${b0===19?"편":"장"}</button><p class="lead">오디오 성경이나 종이 성경으로 읽으셨다면 펼치지 않아도 됩니다.</p>`;
  } else {
    h+=`<div class="bible" id="bible"><div class="bible-tools"><span>점선 밑줄 친 말을 누르면 풀이가 나옵니다.</span><span class="grp"><button class="iconbtn" id="fm" aria-label="글자 작게">가−</button><button class="iconbtn" id="fp" aria-label="글자 크게">가+</button><button class="iconbtn" data-close="1">접기</button></span></div>`;
    for(const [b,c] of p.ch){
      const s2=new Set();
      h+=`<div class="chap" id="ch-${b}-${c}"><h3>${esc(PLAN.full[b-1])} ${c}${b===19?"편":"장"}</h3><div class="vtext">`+BIBLE[b-1][c-1].map((t,i)=>`<span class="v" id="v-${b}-${c}-${i+1}"><sup>${i+1}</sup>${markGloss(t,b,s2)}</span> `).join("")+`</div></div>`;
    }
    h+=`<div class="row" style="margin-top:14px"><button class="btn ghost" data-close="1">본문 접기</button></div></div>`;
  }
  h+=`</section>`;
  // 2 요약
  h+=`<section class="sec"><span class="label">2 · 본문 요약</span><p class="summary">${markGloss(SUMMARY[w-1][d],b0,new Set())}</p>`;
  h+=renderKeyWords(A,w,d);
  h+=`</section>`;
  // 3 단어 설명
  const gl=glossInDay(A,b0), glT=gl.filter(x=>!NAME_SET.has(x.it.t)), glN=gl.filter(x=>NAME_SET.has(x.it.t));
  h+=`<section class="sec"><span class="label">3 · 단어 설명</span>`+(glT.length?`<p class="lead">오늘 본문에 이런 말이 나옵니다. 모르는 말은 눌러 보세요.</p><div class="chips">${glT.slice(0,16).map(x=>`<button class="chip term" data-g="${esc(x.it.t)}">${esc(x.it.t)}</button>`).join("")}</div>`:(glN.length?"":`<p class="lead">오늘 본문에는 따로 풀이할 어려운 말이 없습니다.</p>`))+(glN.length?`<p class="lead"><b style="color:var(--accent)">이름의 뜻</b> 성경의 이름에는 이야기가 담겨 있습니다. 눌러 보세요.</p><div class="chips">${glN.map(x=>`<button class="chip nm" data-g="${esc(x.it.t)}">${esc(x.it.t)}</button>`).join("")}</div>`:"")+`</section>`;
  // 4 지도
  h+=renderMapBox(A);
  // 5 퀴즈
  h+=`<section class="sec" id="quizSec"><span class="label">5 · 퀴즈</span>${renderQuiz(key,null,"day")}</section>`;
  // 완료
  const n=chDone(), after=n+(done?0:p.ch.length);
  h+=`<section class="sec" id="doneSec">`;
  if(done){
    h+=`<div class="done-card"><span class="label" style="color:var(--ok)">${view.justDone?"오늘 통독을 마쳤습니다!":"통독 완료"}</span><b>${pct1(n,TOTAL_CH)}%</b><span>성경 ${TOTAL_CH.toLocaleString()}장 가운데 ${n.toLocaleString()}장을 읽었습니다.${n>=TOTAL_CH?" 성경 일독을 마치셨습니다!":` 남은 장은 ${(TOTAL_CH-n).toLocaleString()}장입니다.`}</span>${window.SYNC&&SYNC.available?`<span class="church" id="churchDay"></span>`:""}${window.SYNC&&SYNC.available&&SYNC.loginEnabled&&!SYNC.loggedIn()?`<span class="lead">기록을 잃지 않으려면 ‘나의 기록’에서 이름을 등록하세요.</span>`:""}<div class="row" style="justify-content:center"><button class="btn small" id="toQT">QT로 이어 가기</button><button class="btn ghost small" id="doneBtn">완료 취소</button></div></div>`;
  } else {
    h+=`<button class="btn" id="doneBtn" style="width:100%;padding:15px">오늘 통독 완료</button><p class="lead" style="text-align:center">완료하면 진행률이 ${pct1(n,TOTAL_CH)}%에서 ${pct1(after,TOTAL_CH)}%로 올라갑니다. 퀴즈를 끝까지 풀면 자동으로 완료됩니다.</p>`;
  }
  h+=`</section>`;
  h+=`<details class="flow"><summary>이번 주 전체 흐름 · ${esc(WEEKS[w-1].t)}</summary><p>${esc(WEEKS[w-1].story)}</p><p style="color:var(--muted);font-size:14.5px">${esc(WEEKS[w-1].christ)}</p></details>`;
  view.justDone=false;
  return h;
}

/* 자주 나오는 말·봉투 구조 */
const vref=(x,b0)=>(x[0]!==b0?PLAN.abbr[x[0]-1]+" ":"")+x[1]+":"+x[2];
function renderKeyWords(A,w,d){
  const k=w+"-"+(d+1), b0=A.verses[0].b;
  const ppl=[...A.people.values()].filter(x=>x.n>=3).sort((a,b)=>b.n-a.n).slice(0,5);
  const lw=LEITWORT[k]||[], em=EMPH[k]||[], inc=INCL[k]||[];
  if(!ppl.length&&!lw.length&&!em.length&&!inc.length&&!(CLUES[k]||[]).length) return "";
  let h=`<div class="kw"><span class="kw-title">본문을 읽는 단서</span>`;
  if(ppl.length) h+=`<div class="kwrow"><p><b>주요 인물</b> 이름이 자주 나오는 사람이 이야기를 이끌어 갑니다. 누가 말하고 움직이는지 따라가 보세요.</p><div class="chips">${ppl.map(x=>`<button class="chip" data-person="${esc(x.name)}">${esc(x.name)}<small>${x.n}</small></button>`).join("")}</div></div>`;
  if(lw.length) h+=`<div class="kwrow"><p><b>주도어</b> 성경 전체보다 오늘 본문에 훨씬 자주 되풀이되는 말입니다. 이렇게 되풀이되며 이야기를 묶는 말을 주도어(Leitwort)라고 합니다. 이 말이 처음 나올 때와 마지막에 나올 때 무엇이 달라졌는지 살펴보세요.</p><div class="chips">${lw.map(x=>`<button class="chip lw" data-lw="${esc(x[0])}">${esc(x[0])}<small>${x[1]}</small></button>`).join("")}</div></div>`;
  const C=CLUES[k]||[], rows=[];
  const by=t=>C.filter(c=>c.t===t);
  if(inc.length) rows.push(`<div class="kwrow"><p><b>봉투 구조</b> 같은 말이나 장면으로 열고 닫아, 그 사이를 봉투처럼 감싸는 짜임입니다(inclusio). 가운데에 무엇이 들어 있는지 보면 글쓴이의 뜻이 보입니다.</p><div class="chips">${inc.map((x,i)=>`<button class="chip inc" data-inc="${i}">${esc(vref(x.a,b0))} ↔ ${esc(vref(x.z,b0))}</button>`).join("")}</div></div>`);
  const ROWDEF=[["turn","꺾이는 곳","여기서 이야기의 방향이 바뀝니다. 바뀌기 전과 후를 비교해 보세요.",c=>vref(c.r,b0)],
    ["scene","닮은 장면","전에 읽은 장면과 닮았습니다. 같은 점과 다른 점을 찾아보세요.",c=>c.g],
    ["echo","구약의 메아리","신약이 구약의 말씀을 다시 부릅니다. 처음 그 말씀이 나온 장면을 떠올려 보세요.",c=>vref(c.r,b0)+" ← "+PLAN.abbr[c.o[0]-1]+" "+c.o[1]+":"+c.o[2]],
    ["pair","나란히 보기","두 사람을 나란히 놓으면 차이가 보입니다. 누가 무엇을 택했나요?",c=>c.a+" ↔ "+c.b],
    ["irony","독자만 아는 것","인물은 모르지만 읽는 우리는 아는 것이 있습니다. 그래서 이 장면이 더 아프거나 우습습니다.",c=>vref(c.r,b0)],
    ["aside","글쓴이의 해설","이야기 중간에 글쓴이가 직접 설명을 덧붙인 곳입니다. 왜 여기서 멈추고 설명했을까요?",c=>vref(c.r,b0)]];
  for(const [t,lab,desc,chip] of ROWDEF){
    let list=by(t); if(t==="scene") list=list.filter(c=>c.prev.length);
    if(list.length) rows.push(`<div class="kwrow"><p><b>${lab}</b> ${desc}</p><div class="chips">${list.map(c=>`<button class="chip cl cl-${t}" data-clue="${C.indexOf(c)}">${esc(chip(c))}</button>`).join("")}</div></div>`);
  }
  if(em.length) rows.push(`<div class="kwrow"><p><b>강조</b> 같은 말을 연달아 부르는 곳은 감정이 북받치거나 힘주어 말하는 자리입니다. 말하는 사람의 마음을 생각해 보세요.</p><div class="chips">${em.map(x=>`<button class="chip em" data-em="${esc(x[0])}">${esc(Array(x[1]).fill(x[0]).join(" "))}</button>`).join("")}</div></div>`);
  h+=rows.slice(0,3).join("");
  return h+`</div>`;
}
const iga=w=>hasB(w.replace(/[^가-힣]/g,"").slice(-1)||"가")?"이":"가";
function showLW(word){
  const k=view.w+"-"+(view.d+1), x=(LEITWORT[k]||[]).find(y=>y[0]===word); if(!x) return; const b0=dayPlan(view.w,view.d).ch[0][0];
  sheet(word,`<p>오늘 본문에 ${x[1]}번 · 평소보다 약 ${Math.round(x[2])}배 자주 나옵니다.</p><p class="src">나오는 곳: ${esc(refList(x[3],b0))}${x[1]>x[3].length?" …":""}</p>`);
}
function showEM(word){
  const k=view.w+"-"+(view.d+1), x=(EMPH[k]||[]).find(y=>y[0]===word); if(!x) return; const b0=dayPlan(view.w,view.d).ch[0][0];
  const v=BIBLE[x[2][0]-1][x[2][1]-1][x[2][2]-1];
  sheet(Array(x[1]).fill(word).join(" "),`<p class="vq">${esc(v)}</p><p class="src">${esc(refList([x[2]],b0))}</p>`);
}
/* 단서 자료를 날짜별로 */
function dayOfRef(q){ for(let w=1;w<=45;w++) for(let d=0;d<6;d++) if(PLAN.plan[w-1][d].ch.some(([b,c])=>b===q[0]&&c===q[1])) return [w,d]; return null; }
const CLUES={};
for(const c of CLUE_LIST){ const at=dayOfRef(c.t==="pair"?c.ra:c.r); if(!at) continue; const key=at[0]+"-"+(at[1]+1); (CLUES[key] ||= []).push(c); }
for(const c of CLUE_LIST.filter(c=>c.t==="scene")){ const me=dayOfRef(c.r); c.prev=CLUE_LIST.filter(o=>o.t==="scene"&&o.g===c.g&&o!==c).map(o=>({o,at:dayOfRef(o.r)})).filter(x=>x.at&&(x.at[0]<me[0]||(x.at[0]===me[0]&&x.at[1]<me[1]))); }
const GAPS={}; for(const g of GAP_LIST){ const at=dayOfRef(g.r); if(at) GAPS[at[0]+"-"+(at[1]+1)]=g; }
const vtext=q=>BIBLE[q[0]-1][q[1]-1][q[2]-1];
const fullRef=q=>PLAN.abbr[q[0]-1]+" "+q[1]+":"+q[2];
const dayLink=(at,label)=>`<button class="btn ghost small" data-jump="${at[0]}-${at[1]}">${at[0]}주차 ${at[1]+1}일째 · ${esc(label)}</button>`;
function showClue(i){
  const k=view.w+"-"+(view.d+1), c=(CLUES[k]||[])[i]; if(!c) return;
  if(c.t==="turn") return sheet("꺾이는 곳",`<p class="vq"><b>${esc(fullRef(c.r))}</b><br>${esc(vtext(c.r))}</p><p>${esc(c.q)}</p>`);
  if(c.t==="echo"){ const at=dayOfRef(c.o); const past=at&&(at[0]<view.w||(at[0]===view.w&&at[1]<view.d));
    return sheet("구약의 메아리",`<p class="vq"><b>오늘 · ${esc(fullRef(c.r))}</b><br>${esc(vtext(c.r))}</p><p class="vq"><b>처음 나온 말씀 · ${esc(fullRef(c.o))}</b><br>${esc(vtext(c.o))}</p>${at?`<p class="src">${past?"이미 읽은 말씀입니다.":"앞으로 읽을 말씀입니다."}</p><div class="row">${dayLink(at,PLAN.plan[at[0]-1][at[1]].label)}</div>`:""}`); }
  if(c.t==="pair") return sheet(c.a+" ↔ "+c.b,`<p class="vq"><b>${esc(c.a)} · ${esc(fullRef(c.ra))}</b><br>${esc(vtext(c.ra))}</p><p class="vq"><b>${esc(c.b)} · ${esc(fullRef(c.rb))}</b><br>${esc(vtext(c.rb))}</p><p>${esc(c.q)}</p>`);
  if(c.t==="scene") return sheet(c.g,`<p class="vq"><b>오늘 · ${esc(c.n)} · ${esc(fullRef(c.r))}</b><br>${esc(vtext(c.r))}</p><p class="src">앞에서 읽은 닮은 장면</p>${c.prev.map(p=>`<p class="vq"><b>${esc(p.o.n)} · ${esc(fullRef(p.o.r))}</b><br>${esc(vtext(p.o.r))}</p><div class="row">${dayLink(p.at,PLAN.plan[p.at[0]-1][p.at[1]].label)}</div>`).join("")}`);
  if(c.t==="irony") return sheet("독자만 아는 것",`<p class="vq"><b>${esc(fullRef(c.r))}</b><br>${esc(vtext(c.r))}</p><p>${esc(c.d)}</p>`);
  if(c.t==="aside") return sheet("글쓴이의 해설",`<p class="vq"><b>${esc(fullRef(c.r))}</b><br>${esc(vtext(c.r))}</p><p>${esc(c.q)}</p>`);
}
function renderArcs(w){
  const list=ARC_LIST.filter(a=>a.w===w); if(!list.length||!BIBLE) return "";
  return `<section class="sec"><span class="label">이번 주 인물의 변화</span>${list.map(a=>`<div class="arc"><b>${esc(a.n)}</b><div class="arcflow"><span>${esc(a.from)}</span><i aria-hidden="true">→</i><span>${esc(a.to)}</span></div><p class="vq"><b>처음 · ${esc(fullRef(a.a))}</b><br>${esc(vtext(a.a))}</p><p class="vq"><b>나중 · ${esc(fullRef(a.z))}</b><br>${esc(vtext(a.z))}</p><p class="lead">무엇이 그를 바꾸었을까요?</p></div>`).join("")}</section>`;
}
function showINC(i){
  const k=view.w+"-"+(view.d+1), x=(INCL[k]||[])[i]; if(!x) return; const b0=dayPlan(view.w,view.d).ch[0][0];
  const t=q=>BIBLE[q[0]-1][q[1]-1][q[2]-1];
  sheet("봉투 구조",`<p class="vq"><b>여는 말 · ${esc(vref(x.a,b0))}</b><br>${esc(t(x.a))}</p><p class="vq"><b>닫는 말 · ${esc(vref(x.z,b0))}</b><br>${esc(t(x.z))}</p><p>${esc(x.d)}</p>`);
}
/* QT */
function qtOf(key){ return mem.qt[key] ||= {}; }
function lensesFor(w,d){
  const det=DETAIL[w+"-"+(d+1)]; if(det&&det.lenses) return det.lenses;
  const g=GENRE_OF(dayPlan(w,d).ch[0][0]); const L=LENSES[g], st=((w-1)*6+d)%L.length;
  return [0,1,2].map(i=>L[(st+i)%L.length]);
}
function clueFor(k,A,w,d){
  const top=(m,n)=>[...m.values()].sort((a,b)=>b.n-a.n).slice(0,n).map(x=>x.name).join(", ");
  if(/무대/.test(k)&&A.places.size) return "오늘 나오는 곳: "+top(A.places,6);
  if(/인물|내 자리/.test(k)&&A.people.size) return "오늘 나오는 사람: "+top(A.people,6);
  if(/줄거리|편지 뒤|시간/.test(k)) return "요약 다시 보기: "+SUMMARY[w-1][d].split(/(?<=다\.)\s/)[0];
  return "";
}
function qtVerses(A,traits,key){
  const det=DETAIL[key]; const list=[];
  if(det){ const txt=[det.god,det.christ,det.apply].join(" ");
    for(const m of txt.matchAll(/\((\d+):(\d+)\)/g)){ const v=A.verses.find(x=>x.c===+m[1]&&x.v===+m[2]); if(v) list.push(v); } }
  traits.forEach(t=>list.push(t.verse));
  // 짧고 하나님이 등장하는 구절 보충
  A.verses.filter(v=>DIVINE.test(v.t)&&v.t.length>=25&&v.t.length<=110).slice(0,40).forEach(v=>list.push(v));
  return [...new Set(list)];
}
function renderQT(){
  const {w,d}=view;
  if(!BIBLE) return `<div class="loading">${bibleErr||"본문을 준비하는 중입니다…"}</div>`;
  if(d===6) return renderQTWeek();
  const p=dayPlan(w,d), key=keyOf(w,d), det=DETAIL[w+"-"+(d+1)], A=dayA(w,d), q=qtOf(key);
  const traits=godTraits(A);
  let h=`<section class="sec"><span class="label">QT · ${w}주차 ${d+1}일째</span><h2>${esc(p.label)}</h2><p class="lead">본문을 읽은 뒤, 이야기 속으로 한 걸음 더 들어가 봅니다. 적는 칸은 비워 두어도 괜찮습니다.</p></section>`;
  // 1 이야기로 읽기
  const L=lensesFor(w,d);
  h+=`<section class="sec"><span class="label">1 · 이야기로 읽기</span>`;
  const gap=GAPS[w+"-"+(d+1)];
  if(gap) h+=`<div class="qcard gapq"><span class="k">말하지 않은 것</span><p>${esc(gap.q)}</p><p class="clue">${esc(fullRef(gap.r))} · 성경이 일부러 비워 둔 자리입니다. 정답은 없습니다.</p></div>`;
  L.forEach(l=>{const c=clueFor(l.k,A,w,d); h+=`<div class="qcard"><span class="k">${esc(l.k)}</span><p>${esc(l.q)}</p>${c?`<p class="clue">${esc(c)}</p>`:""}</div>`;});
  h+=`<textarea id="qt-story" data-qt="story" placeholder="이야기를 읽으며 떠오른 생각을 짧게 적어 보세요">${esc(q.story||"")}</textarea></section>`;
  // 2 하나님의 성품
  h+=`<section class="sec"><span class="label">2 · 본문에 나오는 하나님의 성품</span>`;
  if(det&&det.god) h+=`<div class="qcard"><p>${esc(det.god)}</p></div>`;
  if(traits.length){
    h+=`<p class="lead">오늘 본문에서 찾은 단서입니다.</p>`;
    traits.forEach(t=>{const v=t.verse; h+=`<div class="trait"><b>${esc(t.at.n)}</b><q>${esc(v.t)}</q><span class="lead">${esc(PLAN.abbr[v.b-1])} ${v.c}:${v.v}${t.vs.length>1?` 외 ${t.vs.length-1}절`:""}</span></div>`;});
  } else if(!det) h+=`<p class="lead">오늘 본문에서 하나님이 하신 말씀이나 행동을 하나 찾아보세요. 그 장면에서 하나님은 어떤 분으로 보이나요?</p>`;
  h+=`<div class="qcard"><span class="k">그리스도께로</span><p>${esc(det&&det.christ?det.christ:WEEKS[w-1].christ)}</p></div></section>`;
  // 3 묵상
  const vs=qtVerses(A,traits,w+"-"+(d+1));
  const vi=Math.min(q.vi||0,Math.max(0,vs.length-1)); const kv=vs[vi];
  h+=`<section class="sec"><span class="label">3 · 묵상</span>`;
  if(kv) h+=`<div class="keyv"><small>오늘 붙잡을 말씀 · ${esc(PLAN.abbr[kv.b-1])} ${kv.c}:${kv.v}</small>${esc(kv.t)}</div>${vs.length>1?`<div class="row"><button class="btn ghost small" id="qtNextV">다른 구절 보기 (${vi+1}/${vs.length})</button></div>`:""}`;
  h+=`<div class="qcard"><span class="k">이 구절과 함께 생각하기</span><p>${esc(kv?verseQuestion(kv):(det&&det.apply?det.apply:APPLY_Q))}</p></div><textarea id="qt-med" data-qt="med" placeholder="오늘 말씀 앞에서 내가 할 한 가지">${esc(q.med||"")}</textarea></section>`;
  // 4 기도
  const pray=makePrayer(key,vi,q.pv,p.label,kv,traits);
  h+=`<section class="sec"><span class="label">4 · 기도</span><p class="lead">이 기도로 시작해서 내 말로 이어 가 보세요.</p><p class="prayer">${esc(pray)}</p><textarea id="qt-pray" data-qt="pray" placeholder="나의 기도">${esc(q.pray||"")}</textarea>
   <div class="row"><button class="btn" id="qtDone">${q.done?"QT 완료 ✓":"QT 완료"}</button><span class="lead" id="qtSaved"></span></div></section>`;
  return h;
}
function renderQTWeek(){
  const w=view.w; let h=`<section class="sec"><span class="label">QT · 한 주 돌아보기</span><h2>${w}주차 ${esc(WEEKS[w-1].t)}</h2><p class="lead">이번 주에 적은 묵상과 기도를 다시 읽어 보세요.</p></section>`;
  let any=false;
  for(let d=0;d<6;d++){ const q=mem.qt[keyOf(w,d)]; const p=dayPlan(w,d);
    if(q&&(q.story||q.med||q.pray)){ any=true; h+=`<div class="qcard"><span class="k">${d+1}일째 · ${esc(p.label)}${q.done?" · 완료":""}</span>${q.story?`<p>${esc(q.story)}</p>`:""}${q.med?`<p><b>묵상</b> ${esc(q.med)}</p>`:""}${q.pray?`<p><b>기도</b> ${esc(q.pray)}</p>`:""}</div>`; } }
  if(!any) h+=`<p class="lead">아직 적은 내용이 없습니다. 날짜를 눌러 그날의 QT로 가 보세요.</p>`;
  return h;
}
let qtT;
function bindQT(m){
  if(view.tab!=="qt"||view.d===6) return;
  const key=keyOf(view.w,view.d), q=qtOf(key);
  m.querySelectorAll("[data-qt]").forEach(t=>t.oninput=()=>{q[t.dataset.qt]=t.value; clearTimeout(qtT); qtT=setTimeout(()=>{save(); const s=document.getElementById("qtSaved"); if(s) s.textContent="저장됨";},400);});
  const nv=document.getElementById("qtNextV"); if(nv) nv.onclick=()=>{q.vi=(q.vi||0)+1; const A=dayA(view.w,view.d); const n=qtVerses(A,godTraits(A),view.w+"-"+(view.d+1)).length; if(q.vi>=n) q.vi=0; save(); const y=window.scrollY; render(); window.scrollTo({top:y});};
  const np=document.getElementById("qtNextP"); if(np) np.onclick=()=>{q.pv=(q.pv||0)+1; save(); const y=window.scrollY; render(); window.scrollTo({top:y});};
  const dn=document.getElementById("qtDone"); if(dn) dn.onclick=()=>{q.done=!q.done; save(); const y=window.scrollY; render(); window.scrollTo({top:y});};
}

/* 기도문 30가지: {P}=하나님의 성품 꾸밈말, {L}=본문 범위, {V}=붙잡은 구절 */
const PRAYERS=[
"{P} 하나님, 오늘 {L} 말씀 앞에 머뭅니다. \"{V}\" 이 말씀이 제 하루의 중심이 되게 해 주세요. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 오늘 {L}을 읽으며 {P} 하나님을 다시 만났습니다. 아는 것에 그치지 않고 그 하나님을 신뢰하며 살게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"하나님 아버지, \"{V}\" 이 말씀을 제 마음에 새깁니다. 바쁜 하루 가운데서도 이 말씀이 떠오르게 하시고, 그 말씀대로 한 걸음 움직이게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 주님, 말씀을 읽으면서도 제 마음이 다른 곳에 가 있을 때가 많았습니다. 용서하여 주시고, 오늘 {L}에서 들려주신 음성에 귀 기울이게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 오늘 말씀 속 사람들의 모습에서 제 모습을 봅니다. {P} 하나님께서 그들을 빚으신 것처럼 저도 빚어 주소서. 예수님의 이름으로 기도합니다. 아멘.",
"하나님, \"{V}\" 이 말씀이 오늘 저에게 하시는 말씀으로 들리게 하소서. 듣기만 하고 잊는 사람이 아니라 행하는 사람이 되게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 하나님, 오늘도 성경을 펼칠 수 있는 시간을 주셔서 감사합니다. {L}의 이야기가 제 이야기와 만나게 하시고, 그 안에서 예수님을 더 깊이 알게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 저는 자주 제 힘으로 살려고 합니다. 오늘 {L}에서 보여 주신 {P} 하나님을 의지하며 제 계획을 주님 손에 맡깁니다. 예수님의 이름으로 기도합니다. 아멘.",
"아버지, \"{V}\" 이 말씀에 마음이 머뭅니다. 이 말씀이 필요한 사람을 오늘 제게 보여 주시고, 그 사람에게 주님의 사랑을 전하게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 하나님, 오늘 말씀 가운데 다 이해하지 못한 부분도 있었습니다. 그러나 주님은 아시니 감사합니다. 깨달은 한 가지를 붙들고 순종하게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 오늘 {L}을 읽으며 감사할 이유를 찾았습니다. {P} 하나님이 어제도 오늘도 같은 분이심을 믿습니다. 그 믿음으로 오늘을 살게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"하나님, \"{V}\" 이 말씀 앞에서 제 마음을 살펴봅니다. 주님 보시기에 고쳐야 할 것이 있다면 알려 주시고, 고칠 힘도 주소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 주님, 우리 교회와 가정이 함께 이 말씀을 읽고 있습니다. 같은 말씀으로 같은 마음을 품게 하시고, 서로 세워 주는 공동체가 되게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 성경을 끝까지 읽어 가는 이 길에서 지치지 않게 하소서. 오늘 {L}에서 만난 {P} 하나님이 내일 읽을 말씀에서도 저를 기다리고 계심을 믿습니다. 예수님의 이름으로 기도합니다. 아멘.",
"하나님 아버지, 말씀은 읽었지만 삶은 그대로일 때가 있습니다. \"{V}\" 이 한 구절만큼은 오늘 제 삶에서 열매 맺게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 하나님, 제 마음이 무겁고 흔들릴 때에도 주님은 변하지 않으십니다. 오늘 {L}의 말씀으로 제 마음을 붙들어 주소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 오늘 읽은 말씀 속에서 예수님을 바라보게 하시니 감사합니다. 십자가와 부활의 은혜가 오늘 제 걸음에도 이어지게 하소서. {P} 하나님을 찬양합니다. 예수님의 이름으로 기도합니다. 아멘.",
"하나님, \"{V}\" 이 말씀을 오늘 하루 동안 여러 번 떠올리겠습니다. 떠올릴 때마다 제가 주님 앞에 서 있음을 기억하게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 주님, 제 입술의 말과 마음의 생각이 오늘 읽은 {L} 말씀에 맞게 다듬어지게 하소서. 사람을 살리는 말, 주님을 높이는 말을 하게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 잘 안다고 생각했던 말씀을 오늘 새롭게 읽었습니다. 익숙함에 머물지 않고 날마다 새롭게 주님을 만나게 하소서. {P} 하나님께 감사드립니다. 예수님의 이름으로 기도합니다. 아멘.",
"하나님, 말씀 속 인물들처럼 저도 실수하고 넘어집니다. 그래도 끝까지 붙드시는 {P} 하나님을 신뢰합니다. 다시 일어나 걷게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"아버지, \"{V}\" 이 말씀으로 저를 위로해 주시니 감사합니다. 제가 받은 위로로 오늘 다른 사람을 위로하게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 하나님, 오늘 {L}에서 주님의 뜻을 조금 더 알게 되었습니다. 아는 만큼 순종하고, 순종하는 만큼 더 알게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 세상의 소리가 크게 들리는 하루입니다. 그 가운데서도 \"{V}\" 이 말씀이 가장 크게 들리게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"하나님, 제 시간과 물질과 마음이 모두 주님께로부터 왔음을 고백합니다. {P} 하나님께 오늘 하루를 드립니다. 주님 뜻대로 써 주소서. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 주님, 오늘 말씀을 읽으며 생각나는 사람이 있습니다. 그 사람을 위해 기도합니다. 주님께서 그의 삶에도 찾아가 주소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, 말씀이 제게 거울이 되게 하소서. \"{V}\" 이 말씀에 비추어 제 모습을 보고, 주님을 닮아 가게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"하나님, 오늘 {L} 말씀을 마쳤습니다. 읽은 것으로 끝나지 않고 기억하게 하시고, 기억한 것을 살아 내게 하소서. {P} 하나님을 찬양합니다. 예수님의 이름으로 기도합니다. 아멘.",
"{P} 하나님, 두려움보다 믿음을, 불평보다 감사를, 미움보다 사랑을 택하는 하루가 되게 하소서. 오늘 읽은 말씀이 그 선택을 도와주게 하소서. 예수님의 이름으로 기도합니다. 아멘.",
"주님, \"{V}\" 이 말씀을 제 기도로 삼습니다. 말씀하신 대로 이루어 주시고, 저도 그 말씀 안에 머물게 하소서. 예수님의 이름으로 기도합니다. 아멘."
];
const hashStr=s=>{let h=2166136261;for(const c of s){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;};
function traitOfVerse(v){ for(const at of ATTRS){ if((!at.ot||v.b<40)&&near(v.t,at.re)) return at; } return null; }
function cut(t,n){return t.length>n?t.slice(0,n-1).replace(/\s\S*$/,"")+"…":t;}
/* 고른 구절에 맞춘 묵상 질문 */
function verseKind(v){
  const t=v.t, at=traitOfVerse(v);
  const before=(i)=>{ const s=t.slice(Math.max(0,i-26),i); return ((i>26?"…":"")+s.replace(/^\S*\s/,"")); };
  let m;
  if((m=t.match(/\S*(하라|말라|지어다|할지니라|하여라|할지어다|있으라|받으라|오라|가라|주라|바치라|보라|믿으라|따르라|들으라|구하라|찾으라|두드리라)(?=[\s,.]|$)/))) return {k:"command",ph:(before(m.index)+m[0]).trim(),at};
  if((m=t.match(/\S*(리라|리니|리로다|이루리라)(?=[\s,.]|$)/))) return {k:"promise",ph:(before(m.index)+m[0]).trim(),at};
  if(/(아버지여|주여|하나님이여|여호와여|주님이여)/.test(t)&&!/(이르되|말하되)\s/.test(t.split(/아버지여|주여|하나님이여|여호와여/)[0].slice(-12))) return {k:"prayer",at};
  if(/인자가 온 것은|인자가 .{0,20}권세|나는 .{0,12}(이니|이라|니라)|내가 곧/.test(t)) return {k:"self",at};
  if((m=t.match(/\S*(하려 하노라|하려 함이라|하려 하심이라|위함이라|하려 하심이니)(?=[\s,.]|$)/))) return {k:"purpose",ph:(before(m.index)+m[0]).trim(),at};
  if(/(느냐|냐|니이까|리요|이까|는가|인가)(?=[\s,.]|$)/.test(t)) return {k:"question",at};
  if(at) return {k:"trait",at};
  if(/예수께서 .{0,20}(이르시되|말씀하시되)/.test(t)) return {k:"jesus",at};
  EI.re.lastIndex=0; const pm=[...t.matchAll(EI.re)].map(x=>x[1]).find(n=>EI.map.get(n).type==="person"&&n!=="예수");
  if(pm) return {k:"person",name:pm,at};
  return {k:"scene",at};
}
function verseQuestion(v){
  const K=verseKind(v);
  switch(K.k){
    case "command": return `이 구절은 '${K.ph}'라고 말합니다. 오늘 이 말씀을 그대로 따른다면 나는 구체적으로 무엇을 하게 될까요?`;
    case "promise": return `이 구절에는 '${K.ph}'라는 약속이 있습니다. 이 약속을 붙들어야 할 내 삶의 자리는 어디인가요?`;
    case "prayer": return "이 구절은 하나님께 드리는 기도입니다. 이 기도를 오늘 내 형편에 맞는 말로 바꾸어 드린다면 어떤 기도가 될까요?";
    case "self": return "이 구절에서 예수님은 자신이 누구이며 왜 오셨는지 말씀하십니다. 이 사실이 오늘 내 생각과 행동에서 무엇을 바꾸나요?";
    case "purpose": return `이 구절은 '${K.ph}'라고 그 목적을 밝힙니다. 그 목적이 오늘 나에게는 어떻게 이루어지고 있나요?`;
    case "question": return "이 구절은 질문을 던집니다. 그 질문을 오늘 내가 받는다면 나는 무엇이라고 대답하겠습니까?";
    case "trait": return `이 구절에서 하나님은 '${K.at.n}'으로 드러납니다. 오늘 내 삶에서 그런 하나님이 가장 필요한 자리는 어디인가요?`;
    case "jesus": return "예수님이 이 말씀을 누구에게 하셨나요? 같은 말씀을 오늘 나에게 하신다면 어떻게 들리나요?";
    case "person": return `${K.name}의 자리에 서서 이 장면을 다시 보세요. 그는 무엇을 느꼈을까요? 그 모습에서 나는 무엇을 배우나요?`;
    default: return "이 장면을 마음속에 그려 보세요. 무엇이 보이고 들리나요? 이 장면이 오늘 나에게 무엇을 말하나요?";
  }
}
function makePrayer(key,vi,pv,label,v,traits){
  const at=(v&&traitOfVerse(v))||(traits[0]&&traits[0].at);
  const P=at?at.p:"사랑의";
  const quotable=v&&["command","promise","prayer","self","purpose","trait","jesus"].includes(verseKind(v).k);
  let list=PRAYERS; if(!quotable) list=PRAYERS.filter(x=>!x.includes("{V}"));
  const t=list[hashStr(key+"|"+vi)%list.length];
  return t.replaceAll("{P}",P).replaceAll("{L}",label).replaceAll("{V}",v?cut(v.t,60):"");
}

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
    if(el2&&document.body.contains(el2)) el2.innerHTML=`<div class="stats"><div class="stat"><b>${c.date}</b><span>오늘 통독을 마친 사람</span></div><div class="stat"><b>${c.day}</b><span>이 본문을 읽은 사람</span></div>${SYNC.loginEnabled?`<div class="stat"><b>${c.readers}</b><span>이름을 등록한 사람</span></div>`:""}</div>`;
  });
}
function renderAccount(){
  if(!(window.SYNC&&SYNC.available)) return "";
  if(SYNC.loggedIn()){
    const t=SYNC.lastSaved();
    return `<section class="sec"><span class="label">기록 이어 보기</span><div class="acct"><p><b>${esc(SYNC.name())}</b>님의 기록이 저장되고 있습니다.${t?` <span class="lead">(마지막 저장 ${t.toLocaleTimeString("ko-KR",{hour:"2-digit",minute:"2-digit"})})</span>`:""}</p>${view.acctMsg?`<p class="church">${esc(view.acctMsg)}</p>`:""}<p class="lead">다른 휴대폰이나 컴퓨터에서 같은 이름과 숫자 4자리를 넣으면 이 기록이 이어집니다.</p><div class="row"><button class="btn ghost small" id="acctOut">이 기기에서 나가기</button></div></div></section>
    <section class="sec"><span class="label">우리 교회 함께 읽기</span><div id="churchBox"><p class="lead">불러오는 중…</p></div></section>`;
  }
  if(!SYNC.loginEnabled) return `<section class="sec"><span class="label">우리 교회 함께 읽기</span><div id="churchBox"><p class="lead">불러오는 중…</p></div></section>`;
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
      view.acctMsg=had?"저장된 기록을 불러와 이 기기의 기록과 합쳤습니다.":"새로 등록했습니다. 이제부터 기록이 저장됩니다."; render();
    }catch(e){ msg.textContent=e.message&&/[가-힣]/.test(e.message)?e.message:"연결하지 못했습니다. 인터넷 연결을 확인하고 다시 시도해 주세요."; } };
  const bo=document.getElementById("acctOut"); if(bo) bo.onclick=()=>{ SYNC.logout(); render(); };
  churchCounts();
}
