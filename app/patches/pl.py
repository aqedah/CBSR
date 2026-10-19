p='/home/claude/rj/template3.html'; s=open(p).read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)>=1, a[:80]; s=s.replace(a,b,cnt)
code=r'''
/* 지명: 본문에 나오는 땅 이름 풀이 */
const PL_PART="(?:이라는|이라고|으로부터|에서부터|에서는|에서도|이여|이란|이라|이요|이며|이니|이나|으로|에서|에게|까지|부터|에도|에는|보다|라는|이|가|은|는|을|를|과|와|로|여|아|야|라|요|며|니|나|에|의|도|만|인|란)";
const PL_NAMES=Object.keys(PLACEINFO).filter(n=>!GI.by.has(n)).sort((a,b)=>b.length-a.length);
const PL_RE=new RegExp("(?<![가-힣])("+PL_NAMES.map(escRe).join("|")+")(?="+PL_PART+"{0,3}(?![가-힣]))","g");
const plIn=(n,b)=>{ const p=PLACEINFO[n]; return !!p&&(!p.s||p.s.includes(b)); };
function placesIn(A){ const found=[], seen=new Set();
  for(const v of A.verses){ PL_RE.lastIndex=0; let m; while((m=PL_RE.exec(v.t))){ const n=m[1]; if(!seen.has(n)&&plIn(n,v.b)){ seen.add(n); found.push({n,ref:[v.b,v.c,v.v]}); } } }
  return found; }
function placeEntry(n,b){ const p=PLACEINFO[n]; if(!p) return null;
  let e=p.v.find(x=>x[0].includes(b)); if(!e){ let best=null,bd=1e9; for(const x of p.v){ for(const bb of x[0]){ const dd=Math.abs(bb-b); if(dd<bd){bd=dd;best=x;} } } e=best||p.v[0]; }
  return e; }
function showPlace(n){
  const p=PLACEINFO[n]; if(!p) return; const b=(view.pre||view.revW||isRev(view.d))?0:dayPlan(view.w,view.d).ch[0][0];
  const e=placeEntry(n,b); const onMap=PLACE.has(n);
  sheet(n,`<p class="src">지명 · ${esc(p.k)}${onMap?" · 오늘 지도에 표시되는 곳":""}</p><p>${esc(e[1])}</p>${p.m?`<p class="vq"><b>이름의 뜻</b><br>${esc(p.m)}</p>`:""}${p.v.length>1?`<p class="src">같은 이름이 성경의 다른 곳에도 나옵니다. 지금 읽는 책에 맞는 설명을 보여 드립니다.</p>`:""}`);
}
'''
rep('/* 팝업 */',code+'/* 팝업 */')
# 본문 속 표시: 용어와 지명을 함께
i=s.index('function markGloss(text,b,seen){'); j=s.index('\n}\n',i)+3
s=s[:i]+r'''function markGloss(text,b,seen){
  const hits=[]; let m;
  GI.re.lastIndex=0; while((m=GI.re.exec(text))){ const it=GI.by.get(m[1]); if(it&&inScope(it,b)) hits.push({i:m.index,l:m[1].length,t:"g",k:it.t,s:m[1]}); }
  PL_RE.lastIndex=0; while((m=PL_RE.exec(text))){ if(plIn(m[1],b)) hits.push({i:m.index,l:m[1].length,t:"p",k:m[1],s:m[1]}); }
  hits.sort((a,c)=>a.i-c.i||c.l-a.l);
  let out="",last=0;
  for(const h of hits){ if(h.i<last) continue; const key=(h.t==="p"?"pl:":"")+h.k; if(seen.has(key)) continue; seen.add(key);
    out+=esc(text.slice(last,h.i))+(h.t==="g"?`<span class="g${NAME_SET.has(h.k)?" nm":""}" tabindex="0" role="button" data-g="${esc(h.k)}">${esc(h.s)}</span>`:`<span class="g pl" tabindex="0" role="button" data-pl="${esc(h.k)}">${esc(h.s)}</span>`);
    last=h.i+h.l; }
  return out+esc(text.slice(last));
}
'''+s[j:]
# 3 단어 설명 섹션에 지명 줄
a='''+(glN.length?`<p class="lead"><b style="color:var(--accent)">이름의 뜻</b> 성경의 이름에는 이야기가 담겨 있습니다. 눌러 보세요.</p><div class="chips">${glN.map(x=>`<button class="chip nm" data-g="${esc(x.it.t)}">${esc(x.it.t)}</button>`).join("")}</div>`:"")+`</section>`;'''
assert a in s
s=s.replace(a,'''+(glN.length?`<p class="lead"><b style="color:var(--accent)">이름의 뜻</b> 성경의 사람 이름에는 이야기가 담겨 있습니다. 눌러 보세요.</p><div class="chips">${glN.map(x=>`<button class="chip nm" data-g="${esc(x.it.t)}">${esc(x.it.t)}</button>`).join("")}</div>`:"")+(()=>{ const pl=placesIn(A); if(!pl.length) return ""; const lim=view.plAll?pl.length:24;
    return `<p class="lead"><b style="color:var(--gold)">지명</b> 오늘 본문에 나오는 곳 ${pl.length}곳입니다. 어디쯤 있는 어떤 곳인지 눌러 보세요.</p><div class="chips">${pl.slice(0,lim).map(x=>`<button class="chip pl" data-pl="${esc(x.n)}">${esc(x.n)}</button>`).join("")}${pl.length>lim?`<button class="chip" id="plAll">${pl.length-lim}곳 더 보기</button>`:""}</div>`; })()+`</section>`;''',1)
s=s.replace(''' <p class="lead">오늘 본문에는 따로 풀이할 어려운 말이 없습니다.</p>`''',''' <p class="lead">오늘 본문에는 따로 풀이할 어려운 말이 없습니다.</p>`''')
rep('''  m.querySelectorAll("[data-g]").forEach(el=>{''','''  m.querySelectorAll("[data-pl]").forEach(el=>{el.onclick=()=>showPlace(el.dataset.pl); el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();showPlace(el.dataset.pl);}};});
  const pa=document.getElementById("plAll"); if(pa) pa.onclick=()=>{ view.plAll=true; const y=scrollY; render(); scrollTo({top:y}); };
  m.querySelectorAll("[data-g]").forEach(el=>{''')
rep('</style>','''.g.pl{border-bottom:1.5px dotted var(--gold)}
.chip.pl{border-color:var(--gold);color:var(--gold)}
</style>''')
open(p,'w').write(s); print('ok')
