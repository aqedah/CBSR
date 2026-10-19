r=open('readcode.js').read()
i=r.index('/* 자주 나오는 말 */'); j=r.index('/* QT */')
r=r[:i]+'''/* 자주 나오는 말·봉투 구조 */
const vref=(x,b0)=>(x[0]!==b0?PLAN.abbr[x[0]-1]+" ":"")+x[1]+":"+x[2];
function renderKeyWords(A,w,d){
  const k=w+"-"+(d+1), b0=A.verses[0].b;
  const ppl=[...A.people.values()].filter(x=>x.n>=3).sort((a,b)=>b.n-a.n).slice(0,5);
  const lw=LEITWORT[k]||[], em=EMPH[k]||[], inc=INCL[k]||[];
  if(!ppl.length&&!lw.length&&!em.length&&!inc.length) return "";
  let h=`<div class="kw"><span class="kw-title">본문을 읽는 단서</span>`;
  if(ppl.length) h+=`<div class="kwrow"><p><b>주요 인물</b> 이름이 자주 나오는 사람이 이야기를 이끌어 갑니다. 누가 말하고 움직이는지 따라가 보세요.</p><div class="chips">${ppl.map(x=>`<button class="chip" data-person="${esc(x.name)}">${esc(x.name)}<small>${x.n}</small></button>`).join("")}</div></div>`;
  if(lw.length) h+=`<div class="kwrow"><p><b>주도어</b> 성경 전체보다 오늘 본문에 훨씬 자주 되풀이되는 말입니다. 이렇게 되풀이되며 이야기를 묶는 말을 주도어(Leitwort)라고 합니다. 이 말이 처음 나올 때와 마지막에 나올 때 무엇이 달라졌는지 살펴보세요.</p><div class="chips">${lw.map(x=>`<button class="chip lw" data-lw="${esc(x[0])}">${esc(x[0])}<small>${x[1]}</small></button>`).join("")}</div></div>`;
  if(em.length) h+=`<div class="kwrow"><p><b>강조</b> 같은 말을 연달아 부르는 곳은 감정이 북받치거나 힘주어 말하는 자리입니다. 말하는 사람의 마음을 생각해 보세요.</p><div class="chips">${em.map(x=>`<button class="chip em" data-em="${esc(x[0])}">${esc(Array(x[1]).fill(x[0]).join(" "))}</button>`).join("")}</div></div>`;
  if(inc.length) h+=`<div class="kwrow"><p><b>봉투 구조</b> 같은 말이나 장면으로 열고 닫아, 그 사이를 봉투처럼 감싸는 짜임입니다(inclusio). 가운데에 무엇이 들어 있는지 보면 글쓴이의 뜻이 보입니다.</p><div class="chips">${inc.map((x,i)=>`<button class="chip inc" data-inc="${i}">${esc(vref(x.a,b0))} ↔ ${esc(vref(x.z,b0))}</button>`).join("")}</div></div>`;
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
function showINC(i){
  const k=view.w+"-"+(view.d+1), x=(INCL[k]||[])[i]; if(!x) return; const b0=dayPlan(view.w,view.d).ch[0][0];
  const t=q=>BIBLE[q[0]-1][q[1]-1][q[2]-1];
  sheet("봉투 구조",`<p class="vq"><b>여는 말 · ${esc(vref(x.a,b0))}</b><br>${esc(t(x.a))}</p><p class="vq"><b>닫는 말 · ${esc(vref(x.z,b0))}</b><br>${esc(t(x.z))}</p><p>${esc(x.d)}</p>`);
}
'''+r[j:]
open('readcode.js','w').write(r)
c=open('css3.txt').read()
c=c.replace('/*LEAFLETCSS*/','.chip.inc{border-color:var(--gold);color:var(--gold);font-weight:600}\n.sheet .vq{font-family:var(--f-text);background:var(--paper);border-radius:8px;padding:10px 12px}\n.sheet .vq b{font-family:var(--f-ui);font-size:12px;color:var(--gold)}\n/*LEAFLETCSS*/')
open('css3.txt','w').write(c)
mk=open('make3.py').read()
mk=mk.replace("print('ok5')","""s=open('template3.html').read()
rep('  bindQT(m);','  m.querySelectorAll("[data-inc]").forEach(b=>b.onclick=()=>showINC(+b.dataset.inc));\\n  bindQT(m);')
open('template3.html','w').write(s)
print('ok6')""")
open('make3.py','w').write(mk)
b=open('build3.py').read()
b=b.replace("'routes.js']","'routes.js','incl.js']")
open('build3.py','w').write(b)
print('ok')
