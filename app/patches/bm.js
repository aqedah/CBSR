/* ===== 성경 지도(기록 탭, 2026-10-30 목사님): 본문 탭은 본문이 먼저이므로 지도는 기록 탭에서 엽니다.
   ① 내가 지나온 땅: 읽은 날의 본문에 나온 지명이 켜짐 ② 큰 길: 성경 이야기를 일곱 걸음으로 ③ 여정: 시대별 이동 경로(236개)와 걷기 재생 ===== */
const BM_ERA=[["족장","창세기"],["출애굽·광야","출애굽기–신명기"],["가나안·왕국","여호수아–열왕기상 11장"],["분열·포로·귀환","열왕기상 12장–말라기"],["예수님","복음서"],["사도행전","사도행전–요한계시록"]];
function bmEra(b,c){ if(b===1) return 0; if(b<=5) return 1; if(b<=10||b===13||(b===11&&c<=11)||(b===14&&c<=9)||(b>=18&&b<=22)) return 2; if(b<=39) return 3; if(b<=43) return 4; return 5; }
const BM_BIG=[
 {n:"부르심",t:"갈대아 우르 → 하란 → 가나안",ref:"창 11–12장",d:"하나님이 아브라함을 부르셔서 약속의 땅 가나안으로 이끄십니다.",e:0,c:"#8a5a2b",at:[35.4,43.4],p:[[30.96,46.1],[36.86,39.03],[33.6,36.6],[32.21,35.28]]},
 {n:"애굽으로",t:"가나안 → 애굽 고센",ref:"창 37–50장",d:"요셉이 애굽에 팔려 가고, 기근 때 야곱의 온 가족이 고센 땅으로 내려갑니다.",e:0,c:"#9a6417",at:[31.75,32.9],p:[[31.53,35.1],[31.24,34.79],[30.9,33.0],[30.75,31.7]]},
 {n:"출애굽과 광야",t:"애굽 → 홍해 → 시내 산 → 모압 → 여리고",ref:"출애굽기–여호수아",d:"하나님이 이스라엘을 애굽에서 이끌어 내시고, 시내 산에서 언약을 주시며, 광야 사십 년 뒤 요단을 건너 가나안에 들어가게 하십니다.",e:1,c:"#c45a3c",at:[28.4,32.7],p:[[30.8,31.83],[30.45,32.35],[29.73,32.37],[29.72,32.73],[28.54,33.97],[30.69,34.49],[30.5,35.5],[31.77,35.73],[31.87,35.44]]},
 {n:"가나안과 왕국",t:"여리고 → 실로 → 예루살렘",ref:"여호수아–열왕기상 11장",d:"땅을 얻고 사사 시대를 지나 다윗과 솔로몬의 왕국이 섭니다. 예루살렘에 성전이 세워집니다.",e:2,c:"#2c5c52",at:[32.4,33.7],p:[[31.87,35.44],[32.06,35.29],[31.78,35.23]]},
 {n:"포로",t:"사마리아·예루살렘 → 앗수르·바벨론",ref:"열왕기하 17·25장",d:"나라가 둘로 갈라진 뒤, 북이스라엘은 앗수르로, 남유다는 바벨론으로 끌려갑니다.",e:3,c:"#6b4fa0",at:[36.5,41.4],p:[[31.78,35.23],[33.51,36.29],[34.46,36.57],[36.83,38.01],[35.6,40.5],[32.54,44.42]]},
 {n:"돌아옴",t:"바벨론 → 예루살렘",ref:"에스라·느헤미야",d:"고레스의 조서로 백성이 돌아와 성전과 성벽을 다시 세웁니다.",e:3,c:"#2f6582",dash:1,at:[33.2,39.9],p:[[32.54,44.42],[34.3,41.0],[34.6,37.6],[33.51,36.29],[31.78,35.23]]},
 {n:"예수님과 복음",t:"갈릴리·예루살렘 → 안디옥 → 로마",ref:"복음서·사도행전",d:"예수님이 갈릴리와 예루살렘에서 하나님 나라를 전하시고, 십자가와 부활 뒤에 복음이 예루살렘에서 땅끝 로마까지 퍼집니다.",e:4,e2:5,c:"#b4432f",at:[39.7,21.3],p:[[32.88,35.58],[31.78,35.23],[36.2,36.16],[37.94,27.34],[40.94,24.41],[37.91,22.88],[41.9,12.5]]}];
const BM_BIGL=[["우르",30.96,46.1],["하란",36.86,39.03],["가나안",32.55,35.6],["애굽",30.3,31.2],["시내 산",28.54,33.97],["예루살렘",31.4,35.45],["바벨론",32.54,44.42],["니느웨",36.36,43.15],["로마",41.9,12.5],["에베소",37.94,27.34]];
/* 켜진 지명: 읽은 날(통독 완료)마다 본문의 지명. 날마다 계산은 한 번만 하고 이 기기에 기억(본문 분석이 무거움) */
const BM_V="1"; let BM_PC=null, BM_LIT=null, BM_LITK="";
function bmPC(){ if(BM_PC) return BM_PC; try{ const o=JSON.parse(localStorage.getItem("cbsr-bmpc")||"null"); BM_PC=o&&o.v===BM_V&&o.m===MODE?o:{v:BM_V,m:MODE,d:{}}; }catch(e){ BM_PC={v:BM_V,m:MODE,d:{}}; } return BM_PC; }
let bmPCT=null; function bmPCSave(){ clearTimeout(bmPCT); bmPCT=setTimeout(()=>{ try{ localStorage.setItem("cbsr-bmpc",JSON.stringify(BM_PC)); }catch(e){} },400); }
function bmDayPl(k){ const C=bmPC().d; if(C[k]) return C[k]; if(!BIBLE) return null; const [w,d]=k.split("-").map(Number); let A=null; try{ A=dayA(w,d); }catch(e){ return []; }
  const L=[...A.places.values()].filter(p=>PLACE.has(p.name)&&PLACE.get(p.name)[3]!=="r").map(p=>p.name); C[k]=L; bmPCSave(); return L; }
function bmDoneKeys(){ return Object.keys(mem.done).filter(k=>{ const [w,d]=k.split("-").map(Number); return !!dayPlan(w,d); }).sort((a,b)=>{ const [x,y]=a.split("-").map(Number),[u,v]=b.split("-").map(Number); return dayNo(x,y)-dayNo(u,v); }); }
/* 다 계산되지 않았으면 null(조금씩 나눠 계산하고 끝나면 cb) */
function bmLit(cb){ const ks=bmDoneKeys(), sig=MODE+":"+ks.length+":"+(ks[ks.length-1]||""); if(BM_LIT&&BM_LITK===sig) return BM_LIT;
  const C=bmPC().d, miss=ks.filter(k=>!C[k]);
  if(miss.length){ if(!BIBLE) return null; if(miss.length>25){ let i=0; const step=()=>{ const t=performance.now(); while(i<miss.length&&performance.now()-t<40) bmDayPl(miss[i++]); if(i<miss.length) setTimeout(step,0); else if(cb) cb(); }; if(!bmLit.busy){ bmLit.busy=1; setTimeout(()=>{ step(); },30); const c0=cb; cb=()=>{ bmLit.busy=0; c0&&c0(); }; } return null; } miss.forEach(bmDayPl); }
  const first=new Map(); ks.forEach(k=>(C[k]||[]).forEach(n=>{ if(!first.has(n)) first.set(n,k); }));
  let last=null, ls=""; ks.forEach(k=>{ const s=String(mem.done[k]); if(s>=ls){ ls=s; last=k; } });
  const fresh=last?[...first].filter(x=>x[1]===last).map(x=>x[0]):[];
  BM_LIT={first,fresh,last}; BM_LITK=sig; return BM_LIT; }
/* 이동 경로마다 읽는 날(통독표에서 그 장이 처음 나오는 날) */
let BM_RD=null; function bmRouteDay(r){ if(!BM_RD) BM_RD=new Map(); const id=ROUTES_B.indexOf(r); if(BM_RD.has(id)) return BM_RD.get(id); let o=null;
  outer: for(let wi=0;wi<PLAN.plan.length;wi++) for(let di=0;di<(PLAN.plan[wi]||[]).length;di++){ const P=PLAN.plan[wi][di]; if(P&&P.ch.some(x=>x[0]===r.b&&x[1]>=r.c[0]&&x[1]<=r.c[1])){ o=[wi+1,di]; break outer; } }
  BM_RD.set(id,o); return o; }
const BM_GOLD="#e0a526", BM_RED="#c0392b";
function bmCardHTML(){ const B=bmLit(()=>{ if(view.tab==="record"&&!view.recD){ const y=scrollY; render(); scrollTo({top:y}); } });
  const n=B?B.first.size:0, fr=B?B.fresh.slice(0,2):[];
  const sub=!B?`읽은 본문의 지명을 모으는 중입니다…`:n?`지금까지 <b>${n}곳</b>을 지났습니다${fr.length?` · 최근 <b>${fr.map(esc).join("·")}</b>${B.fresh.length>2?` 등 ${B.fresh.length}곳`:""}이 새로 켜졌습니다`:""}`:`본문을 읽으면 그 날 나온 곳이 지도에 하나씩 켜집니다.`;
  return `<section class="sec rcard"><div class="rhd"><b>내가 지나온 성경의 땅</b><button class="rmorelink" data-recgo="map">지도 열기 ›</button></div><button class="bmcard" data-recgo="map" aria-label="성경 지도 열기"><div class="bmmini" id="bmMini"></div></button><p class="rsub bmsub">${sub}</p></section>`; }
function bmCardInit(){ const el=document.getElementById("bmMini"); if(!el||!window.L) return; const B=bmLit(); setTimeout(()=>{ if(!document.body.contains(el)) return;
  const map=L.map(el,{zoomControl:false,attributionControl:false,dragging:false,scrollWheelZoom:false,touchZoom:false,doubleClickZoom:false,boxZoom:false,keyboard:false,tap:false,zoomSnap:.25}); mapBase(map,"natural");
  map.fitBounds([[29.0,29.5],[38.8,41.5]]); const fresh=new Set(B?B.fresh:[]);
  if(B) B.first.forEach((k,nm)=>{ if(fresh.has(nm)) return; const g=PLACE.get(nm); L.circleMarker([g[1],g[2]],{radius:3,color:"#fff",weight:1,fillColor:BM_GOLD,fillOpacity:1,interactive:false}).addTo(map); });
  fresh.forEach(nm=>{ const g=PLACE.get(nm); L.circleMarker([g[1],g[2]],{radius:6,color:"#fff",weight:2,fillColor:BM_RED,fillOpacity:1,interactive:false}).addTo(map); }); },40); }
/* 상세 화면 */
let BM_MAP=null;
function bmDetailHTML(){ const seg=view.bmSeg||"land"; let h=`<div class="rseg bmseg" role="tablist">${[["land","내가 지나온 땅"],["big","큰 길"],["trip","여정"]].map(([k,t])=>`<button role="tab" aria-selected="${seg===k}" class="${seg===k?"on":""}" data-bmseg="${k}">${t}</button>`).join("")}</div>`;
  if(seg==="trip"){ const e=view.bmEra==null?0:view.bmEra; h+=`<div class="bmeras" role="tablist">${BM_ERA.map((x,i)=>`<button class="${i===e?"on":""}" data-bmera="${i}" aria-selected="${i===e}">${x[0]}</button>`).join("")}</div>`; }
  h+=`<div class="bmmap" id="bmMap"></div><div class="bmpanel">`;
  if(seg==="land"){ const B=bmLit(()=>{ if(view.recD==="map") render(); }); const tot=[...PLACE.values()].filter(g=>g[3]!=="r").length;
    if(!B) h+=`<p class="lead">읽은 본문의 지명을 모으는 중입니다…</p>`;
    else { h+=`<p class="bmstat"><span class="bmk g"></span>켜진 곳 <b>${B.first.size}</b> <span class="bmk n"></span>아직 지나지 않은 곳 ${tot-B.first.size}</p>`;
      if(B.fresh.length) h+=`<p class="bmfr"><span>최근 새로 켜진 곳</span>${B.fresh.slice(0,12).map(n=>`<button data-bmpl="${esc(n)}">${esc(n)}</button>`).join("")}</p>`;
      h+=`<p class="lead rnote">점을 누르면 그곳이 처음 나온 날과 본문을 볼 수 있습니다. 두 손가락으로 지도를 넓혀 보세요.</p>`; } }
  if(seg==="big"){ const s=view.bmBig;
    h+=`<p class="lead rnote">성경 이야기 전체를 일곱 걸음으로 그렸습니다. 번호를 누르면 그 시대의 이야기와 여정을 볼 수 있습니다.</p><div class="bmbig">${BM_BIG.map((x,i)=>`<div class="bmbr${s===i?" on":""}"><button class="bmbh" data-bmbig="${i}"><span class="bmno" style="background:${x.c}">${i+1}</span><span><b>${esc(x.n)}</b><small>${esc(x.t)} · ${esc(x.ref)}</small></span></button>${s===i?`<div class="bmbd"><p>${esc(x.d)}</p><button class="btn small" data-bmgo="${x.e}">${esc(BM_ERA[x.e][0])} 여정 보기 ›</button>${x.e2!=null?` <button class="btn small ghost" data-bmgo="${x.e2}">${esc(BM_ERA[x.e2][0])} 여정 보기 ›</button>`:""}</div>`:""}</div>`).join("")}</div>`; }
  if(seg==="trip"){ const e=view.bmEra==null?0:view.bmEra, R=ROUTES_B.map((r,i)=>[r,i]).filter(([r])=>bmEra(r.b,r.c[0])===e), sel=view.bmSel;
    const rd=R.filter(([r])=>{ const D=bmRouteDay(r); return D&&mem.done[keyOf(D[0],D[1])]; }).length;
    h+=`<p class="bmstat">${esc(BM_ERA[e][0])} 시대 여정 <b>${R.length}</b>개 · 읽은 여정 <b>${rd}</b>개 <small>(${esc(BM_ERA[e][1])})</small></p><div class="bmrl">${R.map(([r,i])=>{ const D=bmRouteDay(r), done=D&&mem.done[keyOf(D[0],D[1])], on=sel===i;
      return `<div class="bmr${on?" on":""}${done?" done":""}" id="bmr${i}"><button class="bmrh" data-bmr="${i}"><span class="bmrd"></span><span><b>${esc(rmBase(r.n))}</b><small>${esc(PLAN.abbr[r.b-1])} ${r.c[0]}${r.c[1]!==r.c[0]?"–"+r.c[1]:""}장${D?` · ${esc(fmt(dateOf(D[0],D[1]),{month:"long",day:"numeric"}))}`:""}</small></span><em>${done?"✓ 읽음":""}</em></button>${on?`<div class="bmrb"><button class="btn small" data-bmplay="${i}">▶ 걸어 보기</button>${D?`<button class="btn small ghost" data-bmday="${D[0]}-${D[1]}">그날 본문 ›</button>`:""}</div>`:""}</div>`; }).join("")}</div>`; }
  return h+`</div>`; }
function bmInit(){ const el=document.getElementById("bmMap"); if(BM_MAP){ try{ BM_MAP.remove(); }catch(e){} BM_MAP=null; } if(!el||!window.L) return; const seg=view.bmSeg||"land";
  const map=L.map(el,{zoomControl:false,attributionControl:true,scrollWheelZoom:false,zoomSnap:.25}); map.attributionControl.setPrefix(false); mapBase(map,"natural"); BM_MAP=map;
  const lab=(ll,t,cls)=>L.marker(ll,{interactive:false,icon:L.divIcon({className:"",html:`<span class="spl bml${cls?" "+cls:""}">${esc(t)}</span>`,iconSize:[0,0],iconAnchor:[-7,9]})}).addTo(map);
  if(seg==="land"){ const B=bmLit()||{first:new Map(),fresh:[]}, fresh=new Set(B.fresh), pts=[];
    PLACE.forEach((g,nm)=>{ if(g[3]==="r"||B.first.has(nm)) return; L.circleMarker([g[1],g[2]],{radius:4,color:"#fff",weight:1,fillColor:"#8c8c84",fillOpacity:.75}).addTo(map).on("click",()=>bmPlace(nm)); });
    B.first.forEach((k,nm)=>{ const g=PLACE.get(nm); pts.push([g[1],g[2]]); L.circleMarker([g[1],g[2]],{radius:fresh.has(nm)?8:6,color:"#fff",weight:fresh.has(nm)?2.5:1.5,fillColor:fresh.has(nm)?BM_RED:BM_GOLD,fillOpacity:1}).addTo(map).on("click",()=>bmPlace(nm)); });
    B.fresh.slice(0,4).forEach(nm=>{ const g=PLACE.get(nm); lab([g[1],g[2]],nm,"new"); });
    if(view.bmFly){ const g=PLACE.get(view.bmFly); view.bmFly=null; if(g) map.setView([g[1],g[2]],8.5); } else map.setView([31.9,35.25],7.25); }
  if(seg==="big"){ const s=view.bmBig;
    BM_BIG.forEach((x,i)=>{ const dim=s!=null&&s!==i; L.polyline(x.p,{color:"#fff",weight:8,opacity:dim?.3:.85,interactive:false}).addTo(map); L.polyline(x.p,{color:x.c,weight:s===i?6:4,opacity:dim?.35:1,dashArray:x.dash?"8 7":null}).addTo(map).on("click",()=>bmBigSel(i));
      L.marker(x.at,{icon:L.divIcon({className:"",html:`<span class="bmno big" style="background:${x.c};opacity:${dim?.45:1}">${i+1}</span>`,iconSize:[0,0],iconAnchor:[13,13]})}).addTo(map).on("click",()=>bmBigSel(i)); });
    BM_BIGL.forEach(x=>lab([x[1],x[2]],x[0]));
    if(s!=null){ map.fitBounds(L.latLngBounds(BM_BIG[s].p.concat([BM_BIG[s].at])),{padding:[36,36],maxZoom:7}); } else map.fitBounds([[27.5,11.5],[41.5,47]],{padding:[6,6]}); }
  if(seg==="trip"){ const e=view.bmEra==null?0:view.bmEra, sel=view.bmSel, R=ROUTES_B.map((r,i)=>[r,i]).filter(([r])=>bmEra(r.b,r.c[0])===e), all=[];
    R.forEach(([r,i])=>{ if(i===sel) return; const D=bmRouteDay(r), done=D&&mem.done[keyOf(D[0],D[1])], ll=r.p.map(q=>[q[1],q[2]]); all.push(...ll);
      L.polyline(ll,{color:done?BM_RED:"#6f6a5e",weight:done?3:2.5,opacity:sel!=null?.35:(done?.85:.6),dashArray:done?null:"5 6"}).addTo(map).on("click",()=>bmRouteSel(i)); });
    if(sel!=null&&ROUTES_B[sel]){ const r=ROUTES_B[sel], ll=r.p.map(q=>[q[1],q[2]]); L.polyline(ll,{color:"#fff",weight:10,opacity:.9,interactive:false}).addTo(map); L.polyline(ll,{color:BM_RED,weight:5,interactive:false}).addTo(map);
      r.p.forEach((q,j)=>{ if(!q[0]) return; L.circleMarker([q[1],q[2]],{radius:j===0?6:4.5,color:"#fff",weight:2,fillColor:j===0?"#2c5c52":BM_RED,fillOpacity:1,interactive:false}).addTo(map); lab([q[1],q[2]],q[0]); });
      map.fitBounds(L.latLngBounds(ll),{padding:[40,40],maxZoom:9}); }
    else if(all.length) map.fitBounds(L.latLngBounds(all),{padding:[24,24],maxZoom:8}); else map.setView([31.8,35.2],6); }
  setTimeout(()=>{ try{ map.invalidateSize(); }catch(e){} },120); }
function bmPlace(nm){ const B=bmLit(), k=B&&B.first.get(nm), g=PLACE.get(nm); let h="";
  if(k){ const [w,d]=k.split("-").map(Number), p=dayPlan(w,d); h=`<p class="bmst on">● 지나온 곳</p><p>처음 지난 날: <b>${esc(fmt(dateOf(w,d),{month:"long",day:"numeric"}))}</b> · ${esc(p.label)}</p><button class="btn small" id="bmGoDay">그날 본문 보기 ›</button>`; }
  else h=`<p class="bmst">○ 아직 지나지 않은 곳</p><p class="lead">이곳이 나오는 본문을 읽으면 지도에 켜집니다.</p>`;
  const info=typeof PLACEINFO!=="undefined"&&PLACEINFO[nm]?PLACEINFO[nm]:null; let desc=""; try{ if(info) desc=placeEntry(nm,0)[1]; }catch(e){}
  sheet(nm,`${h}${desc?`<p class="src" style="margin-top:12px">${esc(desc)}</p>`:""}${g&&g[4]?`<p class="src plest">위치는 추정입니다.</p>`:""}`);
  const b=document.getElementById("bmGoDay"); if(b) b.onclick=()=>{ const [w,d]=k.split("-").map(Number); const x=document.getElementById("sheetClose"); if(x) x.click(); setTimeout(()=>{ bmLeave(); go(w,d); },60); }; }
function bmLeave(){ if(view.recD){ ovDone(recBackOv); view.recD=null; } }
function bmBigSel(i){ view.bmBig=view.bmBig===i?null:i; render(); }
function bmRouteSel(i){ view.bmSel=view.bmSel===i?null:i; render(); const r=document.getElementById("bmr"+i); if(r&&view.bmSel===i) r.scrollIntoView({block:"nearest"}); }
/* 걷기 재생: 스토리 지도와 같은 연출을 한 화면에 */
function bmPlay(i){ const r=ROUTES_B[i]; if(!r) return; const el=document.createElement("div"); el.className="rgm"; el.innerHTML=`<div class="rgmtop"><b>${esc(rmBase(r.n))}</b><button class="gpx" aria-label="닫기">✕</button></div><div class="rgmmap" id="bmPlayMap" style="height:calc(100vh - 140px);height:calc(100dvh - 140px)"></div>`; document.body.appendChild(el); document.body.style.overflow="hidden";
  let map=null; const close=pop=>{ if(pop!==true) ovDone(close); try{ map&&map.remove(); }catch(e){} el.remove(); document.body.style.overflow=""; }; ovOpen(close); el.querySelector(".gpx").onclick=()=>close();
  setTimeout(()=>{ const mel=el.querySelector("#bmPlayMap"); map=L.map(mel,{zoomControl:false,attributionControl:true,dragging:false,scrollWheelZoom:false,touchZoom:false,doubleClickZoom:false,zoomSnap:.25}); map.attributionControl.setPrefix(false); mapBase(map,"natural");
    map.fitBounds(L.latLngBounds(r.p.map(q=>[q[1],q[2]])),{paddingTopLeft:[40,60],paddingBottomRight:[60,140],maxZoom:10});
    const lab=L.layerGroup().addTo(map); r.p.forEach(q=>{ if(q[0]) L.marker([q[1],q[2]],{interactive:false,icon:L.divIcon({className:"",html:`<span class="spl">${esc(q[0])}</span>`,iconSize:[0,0],iconAnchor:[6,8]})}).addTo(lab); });
    const M={route:r.p.map(q=>[q[0],q[1],q[2],0,0]),extra:[],name:r.n,b:r.b}; M.ul=L.polyline(M.route.map(q=>[q[1],q[2]]),{color:"#fff",weight:10,opacity:.85,interactive:false}).addTo(map); M.rl=L.polyline(M.route.map(q=>[q[1],q[2]]),{color:"#e2603f",weight:5,interactive:false}).addTo(map);
    const D=bmRouteDay(r)||[1,0]; try{ mapActors(map,M,{h:""},D[0],D[1]); }catch(e){ console.warn(e); } },60); }
/* 다른 탭에서 성경 지도 열기: 오늘 탭 '오늘의 여정', 도전 '이 여정 전체 보기' */
function bmOpen(seg,o){ o=o||{}; view.bmSeg=seg; if(o.era!=null) view.bmEra=o.era; view.bmSel=o.sel!=null?o.sel:null; if(o.fly) view.bmFly=o.fly; if(view.tab!=="record"){ view.tab="record"; } view.recD=null; recGo("map"); }
function bmOpenRoute(r){ const i=ROUTES_B.indexOf(r); if(i<0) return; bmOpen("trip",{era:bmEra(r.b,r.c[0]),sel:i}); }
function bmBind(m){ m.querySelectorAll("[data-bmseg]").forEach(b=>b.onclick=()=>{ view.bmSeg=b.dataset.bmseg; render(); });
  m.querySelectorAll("[data-bmera]").forEach(b=>b.onclick=()=>{ view.bmEra=+b.dataset.bmera; view.bmSel=null; render(); });
  m.querySelectorAll("[data-bmbig]").forEach(b=>b.onclick=()=>bmBigSel(+b.dataset.bmbig));
  m.querySelectorAll("[data-bmgo]").forEach(b=>b.onclick=()=>{ view.bmSeg="trip"; view.bmEra=+b.dataset.bmgo; view.bmSel=null; render(); window.scrollTo({top:0}); });
  m.querySelectorAll("[data-bmr]").forEach(b=>b.onclick=()=>bmRouteSel(+b.dataset.bmr));
  m.querySelectorAll("[data-bmplay]").forEach(b=>b.onclick=()=>bmPlay(+b.dataset.bmplay));
  m.querySelectorAll("[data-bmday]").forEach(b=>b.onclick=()=>{ const [w,d]=b.dataset.bmday.split("-").map(Number); bmLeave(); go(w,d); });
  m.querySelectorAll("[data-bmpl]").forEach(b=>b.onclick=()=>{ const g=PLACE.get(b.dataset.bmpl); if(g&&BM_MAP) BM_MAP.flyTo([g[1],g[2]],8.5,{duration:.8}); bmPlace(b.dataset.bmpl); });
  if(view.recD==="map") bmInit(); else if(BM_MAP){ try{ BM_MAP.remove(); }catch(e){} BM_MAP=null; }
  bmCardInit(); }
window.CBSR_bm={lit:()=>{ const B=bmLit(); return B?{n:B.first.size,fresh:B.fresh,last:B.last}:null; },open:bmOpen,eras:()=>BM_ERA.map((x,i)=>[x[0],ROUTES_B.filter(r=>bmEra(r.b,r.c[0])===i).length])};
