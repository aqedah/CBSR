m=open('mapcode.js').read()
# --- map: remove satellite, add routes
m=m.replace('''function renderMapBox(A){
  const pts=[...A.places.values()].filter(p=>PLACE.has(p.name));
  if(!pts.length) return''','''function renderMapBox(A){
  const pts=[...A.places.values()].filter(p=>PLACE.has(p.name));
  const R=ROUTES[view.w+"-"+(view.d+1)]||[];
  if(!pts.length&&!R.length) return''')
old_cap=m[m.index('<div id="mnote"></div><div class="cap">'):m.index('</div></div></section>`;\n}')]
m=m.replace(old_cap,'<div class="cap"><span>오늘 본문에 나오는 곳 ${pts.length}곳 · 점을 누르면 나오는 절을 봅니다</span>${R.length?`<span class="rleg">${R.map((r,i)=>`<span><i style="border-color:${RC[i%RC.length]}"></i>${esc(r.n)}</span>`).join("")}</span>`:""}')
i=m.index('  const sat=L.tileLayer'); j=m.index('  // 최소 확대 = 전체 판')
m=m[:i]+'  terr.addTo(map); water.addTo(map);\n'+m[j:]
m=m.replace('let LMAP=null;','let LMAP=null;\nconst RC=["#7A2E8A","#1F5FA8"];')
# frame selection include route pts
m=m.replace('''  const pts=[...A.places.values()].map(p=>({...p,g:PLACE.get(p.name)})).filter(p=>p.g).sort((a,b)=>b.n-a.n);
  const inF=''','''  const pts=[...A.places.values()].map(p=>({...p,g:PLACE.get(p.name)})).filter(p=>p.g).sort((a,b)=>b.n-a.n);
  const R=ROUTES[view.w+"-"+(view.d+1)]||[];
  const rpts=R.flatMap(r=>r.p.map(q=>({name:q[0],g:[q[0],q[1],q[2],"c"]})));
  const inF=''')
m=m.replace('''  let fid=order.find(id=>pts.every(p=>inF(id,p)));
  if(!fid) fid=order.map(id=>[id,pts.filter(p=>inF(id,p)).length]).sort((a,b)=>b[1]-a[1])[0][0];''','''  const must=rpts.length?rpts:pts;
  let fid=order.find(id=>must.every(p=>inF(id,p))&&(rpts.length?pts.filter(p=>inF(id,p)).length>=Math.min(pts.length,1):true));
  if(!fid) fid=order.map(id=>[id,must.filter(p=>inF(id,p)).length]).sort((a,b)=>b[1]-a[1])[0][0];''')
# draw routes before markers
m=m.replace('''  const use=pts.filter(p=>inF(fid,p));''','''  const use=pts.filter(p=>inF(fid,p));
  const arrows=[];
  R.forEach((r,ri)=>{
    const col=RC[ri%RC.length], ll=r.p.map(q=>[q[1],q[2]]);
    L.polyline(ll,{color:"#fff",weight:6,opacity:.7,interactive:false}).addTo(map);
    L.polyline(ll,{color:col,weight:3,dashArray:"8 6",interactive:false}).addTo(map);
    for(let k=0;k<ll.length-1;k++){ const a=ll[k],b=ll[k+1]; if(a[0]===b[0]&&a[1]===b[1]) continue;
      const mid=[(a[0]+b[0])/2,(a[1]+b[1])/2];
      const mk=L.marker(mid,{icon:L.divIcon({className:"",html:`<span class="rarrow" style="border-left-color:${col}"></span>`,iconSize:null}),interactive:false,keyboard:false}).addTo(map);
      arrows.push({mk,a,b}); }
    r.p.forEach((q,qi)=>{ if(!q[0]||use.some(p=>p.name===q[0])) return;
      L.circleMarker([q[1],q[2]],{radius:4,color:col,weight:2,fillColor:"#fff",fillOpacity:1,interactive:false}).addTo(map);
      const mk=L.marker([q[1],q[2]],{icon:L.divIcon({className:"",html:`<span class="mlbl rte">${esc(q[0])}</span>`,iconSize:null}),interactive:false,keyboard:false}).addTo(map);
      labels.push({mk,pri:300+qi}); });
  });
  function orient(){ arrows.forEach(o=>{ const p1=map.latLngToLayerPoint(o.a),p2=map.latLngToLayerPoint(o.b); const ang=Math.atan2(p2.y-p1.y,p2.x-p1.x)*180/Math.PI; const e=o.mk.getElement()?.querySelector(".rarrow"); if(e) e.style.transform=`translate(-50%,-50%) rotate(${ang}deg)`; }); }''')
m=m.replace('''  const labels=[];
  const open=''','''  const open=''')
m=m.replace('''  const use=pts.filter(p=>inF(fid,p));
  const arrows=[];''','''  const use=pts.filter(p=>inF(fid,p));
  const labels=[];
  const arrows=[];''')
m=m.replace('map.on("zoomend moveend",declutter);','map.on("zoomend moveend",declutter); map.on("zoomend",orient);')
m=m.replace('''  const PB=L.latLngBounds(use.map(p=>[p.g[1],p.g[2]]));
  if(use.length===1)''','''  const PB=L.latLngBounds([...use.map(p=>[p.g[1],p.g[2]]),...R.flatMap(r=>r.p.map(q=>[q[1],q[2]])).filter(q=>FB.contains(q))]);
  if(use.length===1&&!R.length)''')
m=m.replace('setTimeout(()=>{if(LMAP!==map)return; map.invalidateSize({animate:false});declutter();},60);','setTimeout(()=>{if(LMAP!==map)return; map.invalidateSize({animate:false});orient();declutter();},60);')
open('mapcode.js','w').write(m)

r=open('readcode.js').read()
old='''  const ppl=[...A.people.values()].sort((a,b)=>b.n-a.n).slice(0,7);
  if(ppl.length) h+=`<div class="chips" aria-label="오늘의 인물">${ppl.map(x=>`<button class="chip" data-person="${esc(x.name)}">${esc(x.name)}<small>${x.n}</small></button>`).join("")}</div>`;'''
new='''  h+=renderKeyWords(A,w,d);'''
assert old in r; r=r.replace(old,new)
r=r.replace('/* QT */','''/* 자주 나오는 말 */
function renderKeyWords(A,w,d){
  const k=w+"-"+(d+1);
  const ppl=[...A.people.values()].filter(x=>x.n>=3).sort((a,b)=>b.n-a.n).slice(0,5);
  const lw=LEITWORT[k]||[], em=EMPH[k]||[];
  if(!ppl.length&&!lw.length&&!em.length) return "";
  let h=`<div class="kw"><span class="kw-title">자주 나오는 말에는 이유가 있습니다</span>`;
  if(ppl.length) h+=`<div class="kwrow"><p><b>주요 인물</b> 이름이 자주 나오는 사람이 이야기를 이끌어 갑니다. 누가 말하고 움직이는지 따라가 보세요.</p><div class="chips">${ppl.map(x=>`<button class="chip" data-person="${esc(x.name)}">${esc(x.name)}<small>${x.n}</small></button>`).join("")}</div></div>`;
  if(lw.length) h+=`<div class="kwrow"><p><b>주도어</b> 성경 전체보다 오늘 본문에 훨씬 자주 되풀이되는 말입니다. 글쓴이가 이 말로 주제와 분위기를 끌고 갑니다.</p><div class="chips">${lw.map(x=>`<button class="chip lw" data-lw="${esc(x[0])}">${esc(x[0])}<small>${x[1]}</small></button>`).join("")}</div></div>`;
  if(em.length) h+=`<div class="kwrow"><p><b>강조</b> 같은 말을 연달아 부르는 곳은 감정이 크게 움직이거나 힘주어 말하는 자리입니다.</p><div class="chips">${em.map(x=>`<button class="chip em" data-em="${esc(x[0])}">${esc(Array(x[1]).fill(x[0]).join(" "))}</button>`).join("")}</div></div>`;
  return h+`</div>`;
}
const iga=w=>hasB(w.replace(/[^가-힣]/g,"").slice(-1)||"가")?"이":"가";
function showLW(word){
  const k=view.w+"-"+(view.d+1), x=(LEITWORT[k]||[]).find(y=>y[0]===word); if(!x) return; const b0=dayPlan(view.w,view.d).ch[0][0];
  sheet(word,`<p>'${esc(word)}'${iga(word)} 오늘 본문에 ${x[1]}번 나옵니다. 성경 전체에서 쓰이는 정도보다 약 ${Math.round(x[2])}배 자주 나옵니다.</p><p>이렇게 한 본문 안에서 되풀이되며 이야기를 묶어 주는 말을 주도어(Leitwort)라고 합니다. 이 말이 처음 나올 때와 마지막에 나올 때 무엇이 달라졌는지 살펴보세요.</p><p class="src">나오는 곳: ${esc(refList(x[3],b0))}${x[1]>x[3].length?" …":""}</p>`);
}
function showEM(word){
  const k=view.w+"-"+(view.d+1), x=(EMPH[k]||[]).find(y=>y[0]===word); if(!x) return; const b0=dayPlan(view.w,view.d).ch[0][0];
  sheet(Array(x[1]).fill(word).join(" "),`<p>같은 말을 ${x[1]}번 연달아 부릅니다. 히브리 사람들은 무언가를 강조하거나 마음이 북받칠 때 이렇게 말을 거듭했습니다.</p><p>이 말을 하는 사람은 지금 어떤 마음일까요?</p><p class="src">나오는 곳: ${esc(refList([x[2]],b0))}</p>`);
}
/* QT */''',1)
open('readcode.js','w').write(r)

c=open('css3.txt').read()
c=c.replace('/*LEAFLETCSS*/','''.kw{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:grid;gap:12px}
.kw-title{font-size:13px;font-weight:600;color:var(--muted)}
.kwrow{display:grid;gap:6px}
.kwrow p{margin:0;font-size:13.5px;color:var(--muted);line-height:1.55}
.kwrow p b{color:var(--accent);margin-right:6px}
.chip.lw{border-color:var(--accent);color:var(--accent);font-weight:600}
.chip.em{border-color:var(--bad);color:var(--bad)}
.rleg{display:flex;flex-wrap:wrap;gap:4px 12px}
.rleg span{display:inline-flex;align-items:center;gap:5px}
.rleg i{display:inline-block;width:20px;border-top:3px dashed}
.rarrow{display:inline-block;width:0;height:0;border-top:6px solid transparent;border-bottom:6px solid transparent;border-left:10px solid;transform-origin:50% 50%}
.mlbl.rte{font-size:11.5px;font-weight:600;color:#3a2c4a}
/*LEAFLETCSS*/''')
c=c.replace('.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}\n.seg button{border:0;background:var(--card);padding:5px 12px;font-size:13px}\n.seg button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink)}\n','')
c=c.replace('.sat .mlbl{color:#fff;text-shadow:0 0 3px #000,0 0 3px #000}\n.mnote{background:var(--gold-soft);color:var(--ink);font-size:13px;padding:8px 12px}\n','')
open('css3.txt','w').write(c)

mk=open('make3.py').read()
mk=mk.replace("print('ok4')","""s=open('template3.html').read()
rep('  bindQT(m);','  m.querySelectorAll("[data-lw]").forEach(b=>b.onclick=()=>showLW(b.dataset.lw));\\n  m.querySelectorAll("[data-em]").forEach(b=>b.onclick=()=>showEM(b.dataset.em));\\n  bindQT(m);')
rep("'위성'은 웹에 따로 올린 버전에서 보입니다.","오늘 이야기에 이동이 있으면 점선과 화살표로 경로를 보여 줍니다.")
open('template3.html','w').write(s)
print('ok5')""")
open('make3.py','w').write(mk)
b=open('build3.py').read()
b=b.replace("'qt_base.js','qt_extra.js']","'qt_base.js','qt_extra.js','routes.js']")
b=b.replace('data+="\\nconst GAZ="','data+="\\nconst LEITWORT="+open(\'leitwort.json\').read()+";\\nconst EMPH="+open(\'emph.json\').read()+";\\nconst GAZ="')
open('build3.py','w').write(b)
print('patched')
