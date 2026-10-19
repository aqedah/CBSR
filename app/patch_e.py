r=open('readcode.js').read()
# 단어 설명: 용어/이름 나누기
old=r[r.index('  const gl=glossInDay(A,b0);'):r.index('\n',r.index('  h+=`<section class="sec"><span class="label">3 · 단어 설명</span>`'))]
new='''  const gl=glossInDay(A,b0), glT=gl.filter(x=>!NAME_SET.has(x.it.t)), glN=gl.filter(x=>NAME_SET.has(x.it.t));
  h+=`<section class="sec"><span class="label">3 · 단어 설명</span>`+(glT.length?`<p class="lead">오늘 본문에 이런 말이 나옵니다. 모르는 말은 눌러 보세요.</p><div class="chips">${glT.slice(0,16).map(x=>`<button class="chip term" data-g="${esc(x.it.t)}">${esc(x.it.t)}</button>`).join("")}</div>`:(glN.length?"":`<p class="lead">오늘 본문에는 따로 풀이할 어려운 말이 없습니다.</p>`))+(glN.length?`<p class="lead"><b style="color:var(--accent)">이름의 뜻</b> 성경의 이름에는 이야기가 담겨 있습니다. 눌러 보세요.</p><div class="chips">${glN.map(x=>`<button class="chip nm" data-g="${esc(x.it.t)}">${esc(x.it.t)}</button>`).join("")}</div>`:"")+`</section>`;'''
r=r.replace(old,new)
# 단서 칸: curated rows
old_inc=r[r.index('  if(inc.length) h+=`<div class="kwrow"><p><b>봉투 구조</b>'):r.index('  return h+`</div>`;\n}',r.index('function renderKeyWords'))]
new_rows='''  const C=CLUES[k]||[], rows=[];
  const by=t=>C.filter(c=>c.t===t);
  if(inc.length) rows.push(`<div class="kwrow"><p><b>봉투 구조</b> 같은 말이나 장면으로 열고 닫아, 그 사이를 봉투처럼 감싸는 짜임입니다(inclusio). 가운데에 무엇이 들어 있는지 보면 글쓴이의 뜻이 보입니다.</p><div class="chips">${inc.map((x,i)=>`<button class="chip inc" data-inc="${i}">${esc(vref(x.a,b0))} ↔ ${esc(vref(x.z,b0))}</button>`).join("")}</div></div>`);
  const ROWDEF=[["turn","꺾이는 곳","여기서 이야기의 방향이 바뀝니다. 바뀌기 전과 후를 비교해 보세요.",c=>vref(c.r,b0)],
    ["echo","구약의 메아리","신약이 구약의 말씀을 다시 부릅니다. 처음 그 말씀이 나온 장면을 떠올려 보세요.",c=>vref(c.r,b0)+" ← "+PLAN.abbr[c.o[0]-1]+" "+c.o[1]+":"+c.o[2]],
    ["pair","나란히 보기","두 사람을 나란히 놓으면 차이가 보입니다. 누가 무엇을 택했나요?",c=>c.a+" ↔ "+c.b],
    ["scene","닮은 장면","전에 읽은 장면과 닮았습니다. 같은 점과 다른 점을 찾아보세요.",c=>c.g],
    ["irony","독자만 아는 것","인물은 모르지만 읽는 우리는 아는 것이 있습니다. 그래서 이 장면이 더 아프거나 우습습니다.",c=>vref(c.r,b0)],
    ["aside","글쓴이의 해설","이야기 중간에 글쓴이가 직접 설명을 덧붙인 곳입니다. 왜 여기서 멈추고 설명했을까요?",c=>vref(c.r,b0)]];
  for(const [t,lab,desc,chip] of ROWDEF){
    let list=by(t); if(t==="scene") list=list.filter(c=>c.prev.length);
    if(list.length) rows.push(`<div class="kwrow"><p><b>${lab}</b> ${desc}</p><div class="chips">${list.map(c=>`<button class="chip cl cl-${t}" data-clue="${C.indexOf(c)}">${esc(chip(c))}</button>`).join("")}</div></div>`);
  }
  if(em.length) rows.push(`<div class="kwrow"><p><b>강조</b> 같은 말을 연달아 부르는 곳은 감정이 북받치거나 힘주어 말하는 자리입니다. 말하는 사람의 마음을 생각해 보세요.</p><div class="chips">${em.map(x=>`<button class="chip em" data-em="${esc(x[0])}">${esc(Array(x[1]).fill(x[0]).join(" "))}</button>`).join("")}</div></div>`);
  h+=rows.slice(0,3).join("");
'''
r=r.replace(old_inc,new_rows)
r=r.replace("if(!ppl.length&&!lw.length&&!em.length&&!inc.length) return \"\";","if(!ppl.length&&!lw.length&&!em.length&&!inc.length&&!(CLUES[k]||[]).length) return \"\";")
# remove old em row inside (it was before inc). find and delete first em row occurrence (old)
old_em='''  if(em.length) h+=`<div class="kwrow"><p><b>강조</b> 같은 말을 연달아 부르는 곳은 감정이 북받치거나 힘주어 말하는 자리입니다. 말하는 사람의 마음을 생각해 보세요.</p><div class="chips">${em.map(x=>`<button class="chip em" data-em="${esc(x[0])}">${esc(Array(x[1]).fill(x[0]).join(" "))}</button>`).join("")}</div></div>`;\n'''
assert old_em in r; r=r.replace(old_em,'')
# popups + helpers
r=r.replace('function showINC(i){','''/* 단서 자료를 날짜별로 */
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
function showINC(i){''',1)
# QT gap card
r=r.replace('''  L.forEach(l=>{const c=clueFor(l.k,A,w,d);''','''  const gap=GAPS[w+"-"+(d+1)];
  if(gap) h+=`<div class="qcard gapq"><span class="k">말하지 않은 것</span><p>${esc(gap.q)}</p><p class="clue">${esc(fullRef(gap.r))} · 성경이 일부러 비워 둔 자리입니다. 정답은 없습니다.</p></div>`;
  L.forEach(l=>{const c=clueFor(l.k,A,w,d);''')
open('readcode.js','w').write(r)

c=open('css3.txt').read()
c=c.replace('/*LEAFLETCSS*/','''.chip.nm{border-color:var(--accent);border-style:dotted}
.g.nm{border-bottom-color:var(--accent)}
.chip.cl{border-color:#7A5AA8;color:#6a4a98}
.arc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;gap:8px}
.arc>b{font-family:var(--f-text);font-size:19px}
.arcflow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:14.5px}
.arcflow span{background:var(--accent-soft);border-radius:8px;padding:6px 10px;flex:1 1 140px;min-width:0}
.arcflow i{font-style:normal;color:var(--accent);font-weight:700}
.arc .vq{font-family:var(--f-text);background:var(--paper);border-radius:8px;padding:10px 12px;margin:0;font-size:15px}
.arc .vq b,.gapq .k{font-family:var(--f-ui);font-size:12px;color:var(--gold)}
.gapq{border-color:var(--gold)}
/*LEAFLETCSS*/''')
open('css3.txt','w').write(c)

mk=open('make3.py').read()
mk=mk.replace("print('ok6')","""s=open('template3.html').read()
rep('  bindQT(m);','  m.querySelectorAll("[data-clue]").forEach(b=>b.onclick=()=>showClue(+b.dataset.clue));\\n  bindQT(m);')
rep('  h+=`<section class="sec"><span class="label">이번 주 이야기 다시 보기</span>','  h+=renderArcs(w);\\n  h+=`<section class="sec"><span class="label">이번 주 이야기 다시 보기</span>')
rep('''  document.getElementById("sheetClose").focus();''','''  root.querySelectorAll("[data-jump]").forEach(b=>b.onclick=()=>{const [w,d]=b.dataset.jump.split("-").map(Number); close(); go(w,d);});
  document.getElementById("sheetClose").focus();''')
rep('''out+=esc(text.slice(last,m.index))+`<span class="g" tabindex="0"''','''out+=esc(text.slice(last,m.index))+`<span class="g${NAME_SET.has(it.t)?" nm":""}" tabindex="0"''')
rep('''function showGloss(t){const it=GI.by.get(t); if(it) sheet(it.t,`<p>${esc(it.d)}</p>`);}''','''function showGloss(t){const it=GI.by.get(t); if(it) sheet(NAME_SET.has(it.t)?it.t+" · 이름의 뜻":it.t,`<p>${esc(it.d)}</p>`);}''')
open('template3.html','w').write(s)
print('ok7')""")
open('make3.py','w').write(mk)
b=open('build3.py').read()
b=b.replace("'routes.js','incl.js']","'routes.js','incl.js','clues.js']")
b=b.replace('data+="\\nconst LEITWORT="','data+="\\nconst NAME_SET=new Set(NAME_MEAN.map(x=>x[0])); for(const n of NAME_MEAN){ if(!GLOSSARY.some(g=>g[0]===n[0])) GLOSSARY.push(n); }\\nconst LEITWORT="')
open('build3.py','w').write(b)
print('patched')
