/* 지도 (확대·축소, 지형/위성) */
const WATER={
 lakes:[[[32.88,35.60],[32.85,35.65],[32.78,35.65],[32.71,35.59],[32.72,35.55],[32.80,35.52],[32.86,35.54]],
        [[31.77,35.47],[31.75,35.56],[31.55,35.55],[31.35,35.53],[31.10,35.45],[31.05,35.40],[31.20,35.38],[31.45,35.40],[31.62,35.42]]],
 rivers:[[[33.10,35.62],[32.90,35.62]],[[32.71,35.57],[32.40,35.56],[32.10,35.53],[31.78,35.55]]]
};
const CTXL={israel:[["지중해",32.2,34.5],["염해",31.3,35.47],["요단 강",32.35,35.63],["갈릴리 바다",32.82,35.6]],asia:[["에게 해",38.6,25.2]],med:[["지중해",34.2,20.5]],neareast:[["지중해",33.6,27.5],["홍해",24.5,36.2],["유브라데 강",34.6,40.6],["힛데겔 강",35.0,43.7],["나일 강",27.0,31.0]]};
let LMAP=null;
const RC=["#7A2E8A","#1F5FA8"];
function destroyMap(){ if(LMAP){ try{LMAP.off();LMAP.stop&&LMAP.stop();LMAP.remove();}catch(e){} LMAP=null; } }
function renderMapBox(A){
  const pts=[...A.places.values()].filter(p=>PLACE.has(p.name));
  const R=ROUTES[view.w+"-"+(view.d+1)]||[];
  if(!pts.length&&!R.length) return `<section class="sec"><span class="label">4 · 지도</span><p class="lead">오늘 본문에는 지도에 표시할 장소가 나오지 않습니다.</p></section>`;
  return `<section class="sec"><span class="label">4 · 지도</span><div class="mapbox"><div id="lmap" role="region" aria-label="오늘 본문에 나오는 곳 지도"></div><div class="cap"><span>오늘 본문에 나오는 곳 ${pts.length}곳 · 점을 누르면 나오는 절을 봅니다</span>${R.length?`<span class="rleg">${R.map((r,i)=>`<span><i style="border-color:${RC[i%RC.length]}"></i>${esc(r.n)}</span>`).join("")}</span>`:""}</div></div></section>`;
}
function initMap(A){
  destroyMap();
  const el=document.getElementById("lmap"); if(!el) return;
  if(!window.L){ el.innerHTML=`<p class="lead" style="padding:16px">지도를 불러오지 못했습니다. 인터넷 연결을 확인해 주세요.</p>`; return; }
  const pts=[...A.places.values()].map(p=>({...p,g:PLACE.get(p.name)})).filter(p=>p.g).sort((a,b)=>b.n-a.n);
  const R=ROUTES[view.w+"-"+(view.d+1)]||[];
  const rpts=R.flatMap(r=>r.p.map(q=>({name:q[0],g:[q[0],q[1],q[2],"c"]})));
  const inF=(id,p)=>{const b=TERRAIN[id].bounds; return p.g[1]>=b[0][0]&&p.g[1]<=b[1][0]&&p.g[2]>=b[0][1]&&p.g[2]<=b[1][1];};
  const order=["israel","asia","med","neareast"];
  const must=rpts.length?rpts:pts;
  let fid=order.find(id=>must.every(p=>inF(id,p))&&(rpts.length?pts.filter(p=>inF(id,p)).length>=Math.min(pts.length,1):true));
  if(!fid) fid=order.map(id=>[id,must.filter(p=>inF(id,p)).length]).sort((a,b)=>b[1]-a[1])[0][0];
  const F=TERRAIN[fid], FB=L.latLngBounds(F.bounds);
  const map=L.map(el,{zoomSnap:0.5,zoomDelta:0.5,scrollWheelZoom:false,maxBounds:FB.pad(0.08),maxBoundsViscosity:0.9});
  LMAP=map;
  map.attributionControl.setPrefix(false);
  const terr=L.layerGroup([L.imageOverlay(F.url,F.bounds,{attribution:"지형: AWS Terrain Tiles(Mapzen) · 해안선: Natural Earth"})]);
  if(fid==="israel") terr.addLayer(L.imageOverlay(TERRAIN.israelhi.url,TERRAIN.israelhi.bounds));
  const water=L.layerGroup([...WATER.lakes.map(l=>L.polygon(l,{color:"#5f8fae",weight:1,fillColor:"#A8C6D6",fillOpacity:1,interactive:false})),...WATER.rivers.map(r=>L.polyline(r,{color:"#5f8fae",weight:2,interactive:false}))]);
  terr.addTo(map); water.addTo(map);
  // 최소 확대 = 전체 판
  map.fitBounds(FB,{animate:false}); map.setMinZoom(map.getZoom());
  const use=pts.filter(p=>inF(fid,p));
  const labels=[];
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
  function orient(){ arrows.forEach(o=>{ const p1=map.latLngToLayerPoint(o.a),p2=map.latLngToLayerPoint(o.b); const ang=Math.atan2(p2.y-p1.y,p2.x-p1.x)*180/Math.PI; const e=o.mk.getElement()?.querySelector(".rarrow"); if(e) e.style.transform=`translate(-50%,-50%) rotate(${ang}deg)`; }); }
  const open=p=>{const b0=A.verses[0].b; const kn={c:"성읍",r:"지역",m:"산",w:"강·바다·호수"}[p.g[3]];
    sheet(p.name,`<p>${kn} · 오늘 본문에 ${p.n}번 나옵니다.</p><p class="src">나오는 곳: ${esc(refList(p.refs,b0))}${p.n>p.refs.length?" …":""}</p><p class="src">위치는 대략적인 것입니다.</p>`);};
  use.forEach((p,i)=>{
    const ll=[p.g[1],p.g[2]], kind=p.g[3];
    if(kind==="r"){
      const mk=L.marker(ll,{icon:L.divIcon({className:"",html:`<span class="mlbl reg">${esc(p.name)}</span>`,iconSize:null}),keyboard:false}).addTo(map).on("click",()=>open(p));
      labels.push({mk,pri:200+i}); return;
    }
    L.circleMarker(ll,{radius:6,color:"#fff",weight:2,fillColor:kind==="m"?"#9A6417":kind==="w"?"#2f6582":"#B4432F",fillOpacity:1}).addTo(map).on("click",()=>open(p));
    const mk=L.marker(ll,{icon:L.divIcon({className:"",html:`<span class="mlbl">${esc(p.name)}</span>`,iconSize:null}),keyboard:false}).addTo(map).on("click",()=>open(p));
    labels.push({mk,pri:i});
  });
  for(const [n,la,lo] of (CTXL[fid]||[])){
    if(use.some(p=>p.name===n.replace(/ 강$/,""))) continue;
    const mk=L.marker([la,lo],{icon:L.divIcon({className:"",html:`<span class="mlbl wat">${n}</span>`,iconSize:null}),interactive:false,keyboard:false}).addTo(map);
    labels.push({mk,pri:500});
  }
  function declutter(){
    const kept=[];
    labels.slice().sort((a,b)=>a.pri-b.pri).forEach(l=>{
      const e=l.mk.getElement()?.querySelector(".mlbl"); if(!e) return;
      e.style.visibility="visible"; const r=e.getBoundingClientRect();
      if(kept.some(k=>!(r.right<k.left||r.left>k.right||r.bottom<k.top||r.top>k.bottom))) e.style.visibility="hidden"; else kept.push(r);
    });
  }
  map.on("zoomend moveend",declutter); map.on("zoomend",orient);
  const PB=R.length?L.latLngBounds(R.flatMap(r=>r.p.map(q=>[q[1],q[2]])).filter(q=>FB.contains(q))):L.latLngBounds(use.map(p=>[p.g[1],p.g[2]]));
  if(use.length===1&&!R.length) map.setView(PB.getCenter(),Math.max(map.getZoom(),fid==="israel"?8.5:6.5),{animate:false});
  else map.fitBounds(PB.pad(R.length?0.12:0.25),{maxZoom:fid==="israel"?8.5:(R.length?7.5:6.5),animate:false});
  setTimeout(()=>{if(LMAP!==map)return; map.invalidateSize({animate:false});orient();declutter();},60);
}
