/* ===== 공간 탐색(spaceOpen) — 세 번째 틀(GPT 2026-11-10 §3-1): 한 공간을 중심으로 여러 본문의 자리를 살펴봄.
   장소를 누르면 그 장소의 사건 목록이, 읽는 날에서 들어오면 그 장소가 강조됨. 사건을 누르면 그 구절(개역개정)이 위 말씀 카드에 뜸.
   첫 편: 헤롯 성전 뜰. 자리는 모두 복원도(r). 미문은 니가노르 문으로 보는 견해가 유력하나 확정하지 않음(?). ===== */
const SPACES={};
function spaceReg(sp){ SPACES[sp.id]=sp; return sp; }
function spaceCard(id){ const p=SPACES[id]; if(!p) return ""; const n=p.places.reduce((a,x)=>a+(x.ev||[]).length,0); return `<button class="bmtc" data-space="${id}"><i>▶</i><b>${esc(p.card||p.title)}</b><small><span>${esc(p.sub||"")}</span></small><em>장소 ${p.places.length} · 본문 ${n}</em></button>`; }
function spaceHere(p){ if(!p) return []; const has=(b,c)=>p.ch.some(x=>x[0]===b&&x[1]===c); const out=[];
  for(const id in SPACES){ const sp=SPACES[id]; let hit=null; for(const pl of sp.places){ const k=(pl.ev||[]).findIndex(ev=>has(ev.r[0],ev.r[1])); if(k>=0){ hit=[pl,pl.ev[k],k]; break; } } if(!hit) continue;
    out.push(`<button class="tourhere" data-space="${id}" data-pl="${hit[0].id}" data-ev="${hit[2]}"><i>▶</i><span><b>${esc(sp.title)}</b><small>오늘 본문의 자리: ${esc(hit[0].n)} · ${esc(hit[1].t)}</small></span></button>`); }
  return out; }
document.addEventListener("click",e=>{ const b=e.target.closest&&e.target.closest("[data-space]"); if(!b) return; e.preventDefault(); e.stopPropagation(); try{ document.querySelector("#sheetX")?.click(); }catch(e2){} spaceOpen(b.dataset.space,b.dataset.pl||"",b.dataset.ev); });
function spaceOpen(id,pl0,ev0){ const SP=SPACES[id]; if(!SP) return; document.querySelector(".atn")?.remove();
  const el=document.createElement("div"); el.className="bmt2 atn pln spc"; el.setAttribute("role","dialog"); el.setAttribute("aria-label",SP.title); const VB=SP.vb||[300,430];
  el.innerHTML=`<div class="bmtmap atmap"><svg class="map" id="sp_svg" preserveAspectRatio="xMidYMid meet" viewBox="0 0 ${VB[0]} ${VB[1]}" role="img" aria-label="${esc(SP.title)}">
    <defs><radialGradient id="pl_glow"><stop offset="0" stop-color="#fff3c0" stop-opacity=".98"/><stop offset=".55" stop-color="#ffd978" stop-opacity=".55"/><stop offset="1" stop-color="#ffd978" stop-opacity="0"/></radialGradient></defs>
    <g id="sp_base">${SP.svg}</g><g id="sp_hl"></g>
    <g id="sp_hot">${SP.places.map(p=>`<g class="sphot" data-pl="${p.id}" role="button" tabindex="0" aria-label="${esc(p.n)}"><rect class="hit" x="${Math.min(p.box[0],p.box[0]+p.box[2]/2-24)}" y="${Math.min(p.box[1],p.box[1]+p.box[3]/2-18)}" width="${Math.max(p.box[2],48)}" height="${Math.max(p.box[3],36)}" fill="rgba(0,0,0,0)"/><rect x="${p.box[0]}" y="${p.box[1]}" width="${p.box[2]}" height="${p.box[3]}" rx="4" fill="rgba(165,54,31,0)" stroke="rgba(165,54,31,0)" stroke-width="1.5"/><text class="pl" x="${p.lx??(p.box[0]+p.box[2]/2)}" y="${p.ly??(p.box[1]+p.box[3]/2+3)}" text-anchor="middle" style="font-size:${p.fs||8.5}px;fill:#8f1d0f;paint-order:stroke;stroke:#f3e6c4;stroke-width:3px">${esc(p.n)}${(p.ev||[]).length?` <tspan style="font-size:7px;fill:#6b4a24">${p.ev.length}</tspan>`:""}</text></g>`).join("")}</g>
  </svg></div>
   <div class="bmttop"><b>${esc(SP.title)}</b><button class="bmtic" data-t="back" aria-label="장소 목록">☰</button><button class="bmtic" data-t="x" aria-label="닫기">✕</button></div>
   <div class="bmtp spcp"><p class="bmtk"></p><h3 class="bmth"></h3><p class="bmtn"></p><div class="spev"></div>${SP.note?`<p class="plnote">${esc(SP.note)}</p>`:""}</div>
   <p class="bmthint">지도의 이름을 누르면 그 자리의 본문이 보입니다</p>`;
  document.body.appendChild(el); document.body.style.overflow="hidden";
  const $=s=>el.querySelector(s), NS="http://www.w3.org/2000/svg"; let cur=null;
  const K={t:"본문에 이름이 나오는 곳",r:"복원도(자리 추정)",i:"본문으로 미루어 추정",u:"자리 미상",v:"환상"};
  function home(){ cur=null; $("#sp_hl").innerHTML=""; el.querySelectorAll(".sphot").forEach(g=>g.classList.remove("on")); $(".bmtk").textContent=SP.kicker||""; $(".bmth").textContent=SP.title; $(".bmtn").textContent=SP.intro||"";
    $(".spev").innerHTML=`<div class="spls">${SP.places.filter(p=>(p.ev||[]).length).map(p=>`<button class="spl" data-pl="${p.id}"><b>${esc(p.n)}</b><small>${p.ev.map(e=>vLab(e.r).split(":")[0]).filter((x,i,a)=>a.indexOf(x)===i).join(" · ")}</small></button>`).join("")}</div>`; el.querySelectorAll(":scope>.mvnar").forEach(n=>{ if(n._c) n._c(); n.classList.remove("on"); }); }
  function show(plid,evi){ const p=SP.places.find(x=>x.id===plid); if(!p) return; cur=p; el.querySelectorAll(".sphot").forEach(g=>g.classList.toggle("on",g.dataset.pl===plid));
    const hl=$("#sp_hl"); hl.innerHTML=`<rect x="${p.box[0]-2}" y="${p.box[1]-2}" width="${p.box[2]+4}" height="${p.box[3]+4}" rx="5" fill="url(#pl_glow)" opacity=".55"/><rect x="${p.box[0]}" y="${p.box[1]}" width="${p.box[2]}" height="${p.box[3]}" rx="4" fill="none" stroke="#a5361f" stroke-width="2" stroke-dasharray="${p.k==="t"?"0":"5 4"}"/>`;
    $(".bmtk").textContent=`${K[p.k||"r"]}${p.alt?` · ${p.alt}`:""}`; $(".bmth").textContent=p.n; $(".bmtn").textContent=p.d||"";
    $(".spev").innerHTML=(p.ev||[]).length?`<div class="spls">${p.ev.map((e,i)=>`<button class="spl${evi===i?" on":""}" data-ev="${i}"><b>${esc(e.t)}</b><small>${esc(vLab(e.r))}${e.c?` · ${esc(e.c)}`:""}</small></button>`).join("")}</div>`:`<p class="plnote">이 자리를 직접 말하는 본문은 없습니다. 짜임을 알기 위한 표시입니다.</p>`;
    if(evi!=null&&p.ev[evi]){ const e=p.ev[evi]; $(".bmtn").textContent=e.d||p.d||""; mvNar(el,e.q,e.r,66,Math.max(6000,2000+e.q.length*70),e.god?(e.godn||"여호와"):undefined); } }
  const close=pop=>{ el.remove(); document.body.style.overflow=""; if(pop!==true) ovDone(close); }; ovOpen(close);
  el.addEventListener("click",e=>{ const t=e.target.closest("[data-t]"); if(t){ if(t.dataset.t==="x") close(); else if(t.dataset.t==="back") home(); return; }
    const ev=e.target.closest("[data-ev]"); if(ev&&cur){ show(cur.id,+ev.dataset.ev); return; } const pl=e.target.closest("[data-pl]"); if(pl){ show(pl.dataset.pl,0); } });
  el.addEventListener("keydown",e=>{ if(e.key==="Enter"||e.key===" "){ const pl=e.target.closest&&e.target.closest(".sphot"); if(pl){ e.preventDefault(); show(pl.dataset.pl,0); } } });
  if(pl0&&SP.places.some(p=>p.id===pl0)) show(pl0,ev0!=null&&ev0!==""?+ev0:0); else home(); } /* 2차 검수 P1-2: 오늘 본문의 사건부터 */
try{ window.spaceOpen=spaceOpen; window.SPACES=SPACES; }catch(e){}

/* ── 헤롯 성전 뜰 ── 위가 북. 바깥(이방인의 뜰)에서 안(지성소)으로 들어갈수록 높아짐. 짜임은 요세푸스·미쉬나에 따른 복원도 */
(function(){
function HT_SVG(){ return `
    <text class="pl m" x="8" y="14">↑ 북</text>
    <rect class="court" x="20" y="30" width="260" height="380" rx="3"/>
    <g stroke="#8a7a62" stroke-width="1" opacity=".7">${Array.from({length:12},(_,i)=>`<circle cx="${30+i*21.8}" cy="40" r="2" fill="#c9a24a"/><circle cx="${30+i*21.8}" cy="400" r="2" fill="#c9a24a"/>`).join("")}${Array.from({length:17},(_,i)=>`<circle cx="270" cy="${50+i*21.5}" r="2" fill="#c9a24a"/><circle cx="30" cy="${50+i*21.5}" r="2" fill="#c9a24a"/>`).join("")}</g>
    <text class="pl m pk-r" x="150" y="404" text-anchor="middle" style="font-size:7.5px">왕의 행각 (남쪽) · 복원도</text>
    <rect x="70" y="130" width="160" height="190" rx="2" fill="none" stroke="#8f1d0f" stroke-width="1.2" stroke-dasharray="3 3"/><text class="pl m pk-r" x="150" y="326" text-anchor="middle" style="font-size:7px">경계 담(소레그) · 이방인은 이 안으로 들어갈 수 없음 (행 21:28)</text>
    <rect class="court" x="80" y="226" width="140" height="80" rx="2"/>
    <rect class="court" x="80" y="140" width="140" height="80" rx="2"/><rect class="house" x="110" y="150" width="80" height="54" rx="2"/><rect class="hh" x="112" y="152" width="34" height="50"/><line x1="146" y1="152" x2="146" y2="202" stroke="#7a2a5a" stroke-width="2.4"/>
    <rect class="bronze" x="198" y="166" width="16" height="22"/>
    <rect class="gate" x="140" y="218" width="20" height="10"/>
    <rect class="gate" x="140" y="302" width="20" height="10"/>
    <text class="pl m pk-r" x="150" y="36" text-anchor="middle" style="font-size:7px">안토니아 요새 쪽 (북)</text>`; }
const E=(t,b,c,v,q,d,c2)=>({t,r:[b,c,v],q,d,c:c2});
spaceReg({id:"temple",title:"헤롯 성전 뜰",card:"헤롯 성전 뜰 · 자리 보기",sub:"복음서·사도행전 본문이 성전 어디에서 있었나",kicker:"공간 탐색 · 복원도",vb:[300,430],svg:HT_SVG(),
 intro:"예수님과 사도들의 일이 성전 어느 자리에서 있었는지 보는 지도입니다. 바깥 이방인의 뜰에서 안쪽 지성소로 갈수록 높아지고 들어갈 수 있는 사람이 줄어듭니다. 이름을 누르면 그 자리의 본문이 보입니다. 짜임은 복원도이며, 본문이 자리를 특정하지 않는 사건은 '성전'에 두었습니다.",
 note:"복원도 · 헤롯 성전의 짜임은 요세푸스와 미쉬나의 기록을 따른 그림이며 학자마다 다릅니다. 본문이 자리를 특정하지 않은 사건은 확정하지 않았습니다",
 places:[
  {id:"gent",n:"이방인의 뜰",k:"r",box:[26,46,248,80],lx:150,ly:96,d:"가장 바깥의 넓은 뜰. 이방인도 들어올 수 있습니다. 둘레에 기둥 행각이 있고, 남쪽은 왕의 행각입니다. 본문은 '성전'이라고만 하므로 아래 사건들의 자리는 전통적인 복원에 따른 추정입니다.",ev:[
    E("성전을 깨끗하게 하시다 (요)",43,2,15,"노끈으로 채찍을 만드사 양이나 소를 다 성전에서 내쫓으시고 돈 바꾸는 사람들의 돈을 쏟으시며 상을 엎으시고","요한은 공생애 첫 유월절에 둡니다. 장사하는 곳을 이방인의 뜰로 보는 것은 일반적인 복원이지 본문의 진술은 아닙니다.","자리 추정"),
    E("성전을 깨끗하게 하시다 (마)",40,21,12,"예수께서 성전에 들어가사 성전 안에서 매매하는 모든 사람들을 내쫓으시며 돈 바꾸는 사람들의 상과 비둘기 파는 사람들의 의자를 둘러 엎으시고","마태·마가·누가는 예루살렘 입성 뒤에 둡니다. 자리는 추정입니다.","자리 추정"),
    E("성전에서 가르치시다 · 무슨 권위로",40,21,23,"예수께서 성전에 들어가 가르치실새 대제사장들과 백성의 장로들이 나아와 이르되 네가 무슨 권위로 이런 일을 하느냐 또 누가 이 권위를 주었느냐","마지막 주간 날마다 성전에서 가르치십니다. 자리는 특정되지 않습니다.","자리 미상"),
    E("초대교회가 날마다 성전에 모이다",44,2,46,"날마다 마음을 같이하여 성전에 모이기를 힘쓰고 집에서 떡을 떼며 기쁨과 순전한 마음으로 음식을 먹고","오순절 뒤 믿는 사람들이 날마다 성전에 모입니다. 솔로몬 행각(행 5:12)이 그 자리로 보입니다.","자리 추정")]},
  {id:"solo",n:"솔로몬 행각",k:"t",box:[256,46,20,350],lx:266,ly:230,fs:7.5,d:"성전 동쪽의 기둥 행각. 본문이 이름으로 말하는 자리입니다(요 10:23, 행 3:11, 5:12). 동쪽이라는 것은 복원에 따릅니다.",ev:[
    E("겨울 수전절 · 솔로몬 행각에서 거니시다",43,10,23,"예수께서 성전 안 솔로몬 행각에서 거니시니","유대인들이 둘러싸고 \"그리스도이면 밝히 말씀하소서\" 합니다(10:24)."),
    E("걷게 된 사람이 붙잡으니 · 백성이 달려 모임",44,3,11,"나은 사람이 베드로와 요한을 붙잡으니 모든 백성이 크게 놀라며 달려 나아가 솔로몬의 행각이라 불리우는 행각에 모이거늘","미문(3:2)에서 걷게 된 사람이 사도들과 함께 성전에 들어가(3:8) 솔로몬 행각까지 이어집니다. 베드로의 두 번째 설교가 여기서."),
    E("믿는 사람이 다 솔로몬 행각에 모이다",44,5,12,"사도들의 손을 통하여 민간에 표적과 기사가 많이 일어나매 믿는 사람이 다 마음을 같이하여 솔로몬 행각에 모이고","초대교회의 모이는 자리.")]},
  {id:"gate",n:"미문?",k:"i",alt:"니가노르 문으로 보는 견해가 유력",box:[134,298,32,18],lx:150,ly:346,fs:8,d:"'미문이라는 성전 문'(행 3:2). 어느 문인지 본문은 말하지 않습니다. 여인의 뜰에서 안으로 들어가는 니가노르 문으로 보는 견해가 유력하지만 확정하지 않습니다.",ev:[
    E("미문에서 구걸하던, 나면서 못 걷게 된 사람",44,3,2,"나면서 못 걷게 된 이를 사람들이 메고 오니 이는 성전에 들어가는 사람들에게 구걸하기 위하여 날마다 미문이라는 성전 문에 두는 자라","\"은과 금은 내게 없거니와\" — 걷게 된 그가 뛰며 성전에 들어가고(3:8), 솔로몬 행각으로 이어집니다(3:11).")]},
  {id:"women",n:"여인의 뜰 · 헌금함",k:"r",box:[82,228,136,76],lx:150,ly:250,d:"이스라엘 여인도 들어올 수 있는 뜰. 헌금함(나팔 모양 열세 개)이 이 뜰 벽에 있었다는 것은 전통적인 성전 구조에 따른 추정입니다.",ev:[
    E("과부의 두 렙돈",41,12,41,"예수께서 헌금함을 대하여 앉으사 무리가 어떻게 헌금함에 돈 넣는가를 보실새 여러 부자는 많이 넣는데","한 가난한 과부가 두 렙돈을 넣습니다. \"이 과부는 그 모든 사람보다 많이 넣었도다\"(12:43). 헌금함 자리는 추정.","자리 추정"),
    E("부자들이 헌금 넣는 것을 보시고",42,21,1,"예수께서 눈을 들어 부자들이 헌금함에 헌금 넣는 것을 보시고","누가의 같은 장면.","자리 추정"),
    E("헌금함 앞에서 하신 말씀 · 세상의 빛",43,8,20,"이 말씀은 성전에서 가르치실 때에 헌금함 앞에서 하셨으나 잡는 사람이 없으니 이는 그의 때가 아직 이르지 아니하였음이러라","\"나는 세상의 빛이니\"(8:12)를 헌금함 앞에서 하셨다고 요한이 적습니다.","자리 추정")]},
  {id:"isr",n:"이스라엘의 뜰 · 제사장의 뜰 · 번제단",k:"r",box:[82,142,136,76],lx:150,ly:214,fs:7.5,d:"이스라엘 남자가 들어오는 뜰과, 그 안쪽 제사장들만 드나드는 뜰. 번제단이 성소 앞에 있습니다. 바리새인과 세리의 비유(눅 18:10)는 '성전에 올라가 기도'라고만 하므로 자리를 특정하지 않습니다.",ev:[
    E("바리새인과 세리, 기도하러 성전에",42,18,10,"두 사람이 기도하러 성전에 올라가니 하나는 바리새인이요 하나는 세리라","비유입니다. 세리는 \"멀리 서서\" 가슴을 칩니다(18:13). 자리는 특정하지 않습니다.","자리 미상")]},
  {id:"holy",n:"성소 · 지성소",k:"r",box:[110,150,80,54],lx:168,ly:180,fs:8,d:"제사장만 들어가는 성소와, 대제사장이 일 년에 한 번 들어가는 지성소. 그 사이의 휘장이 예수님이 숨지실 때 찢어집니다.",ev:[
    E("사가랴가 제비를 뽑아 분향하러 들어가다",42,1,9,"제사장의 전례를 따라 제비를 뽑아 주의 성전에 들어가 분향하고","향단 우편에 천사가 서서 세례 요한의 출생을 알립니다(1:11)."),
    E("성소 휘장이 찢어지다",40,27,51,"이에 성소 휘장이 위로부터 아래까지 찢어져 둘이 되고 땅이 진동하며 바위가 터지고","예수님이 숨지실 때. 마가 15:38, 누가 23:45에도.")]},
  {id:"temple",n:"성전 (자리를 말하지 않는 본문)",k:"u",box:[26,356,248,42],lx:150,ly:380,fs:8,d:"본문이 '성전'이라고만 하여 어느 뜰인지 알 수 없는 사건들입니다. 자리를 확정하지 않습니다.",ev:[
    E("시므온과 안나가 아기 예수를 만나다",42,2,27,"성령의 감동으로 성전에 들어가매 마침 부모가 율법의 관례대로 행하고자 하여 그 아기 예수를 데리고 오는지라","정결 예식을 위해 올라온 날. 성전 안 어느 자리인지는 말하지 않습니다.","자리 미상"),
    E("열두 살 예수, 선생들 가운데",42,2,46,"사흘 후에 성전에서 만난즉 그가 선생들 중에 앉으사 그들에게 듣기도 하시며 묻기도 하시니","특정 뜰로 확정하지 않습니다.","자리 미상"),
    E("성전 꼭대기에 세우고 · 시험",40,4,5,"이에 마귀가 예수를 거룩한 성으로 데려다가 성전 꼭대기에 세우고","광야 시험의 둘째. '꼭대기'가 어느 곳인지는 말하지 않습니다.","자리 미상")]},
  {id:"soreg",n:"경계 담 · 바울이 붙잡힌 곳",k:"i",box:[72,132,156,8],lx:150,ly:128,fs:7.5,d:"이방인이 넘으면 죽는다는 경고판이 있던 담. 바울에 대한 고발은 '헬라인을 데리고 성전에 들어가 더럽혔다'는 것이었습니다. 그러나 드로비모가 실제로 담 안에 들어갔다는 것은 고발자들의 추측이었습니다(21:29). 바울은 성전 밖으로 끌려 나가고 문들이 닫힙니다(21:30).",ev:[
    E("헬라인을 데리고 성전에 들어갔다는 고발",44,21,28,"외치되 이스라엘 사람들아 도우라 이 사람은 각처에서 우리 백성과 율법과 이 곳을 비방하여 모든 사람을 가르치는 그 자인데 또 헬라인을 데리고 성전에 들어가서 이 거룩한 곳을 더럽혔다 하니","아시아에서 온 유대인들의 고발."),
    E("드로비모를 데리고 들어간 줄로 생각함 — 추측",44,21,29,"이는 그들이 전에 에베소 사람 드로비모가 바울과 함께 시내에 있음을 보고 바울이 그를 성전에 데리고 들어간 줄로 생각함이러라","본문은 이것이 그들의 생각이었다고 적습니다. 드로비모가 들어가는 그림은 그리지 않습니다."),
    E("성전 밖으로 끌려 나가고 문들이 닫히다",44,21,30,"온 성이 소동하여 백성이 달려와 모여 바울을 잡아 성전 밖으로 끌고 나가니 문들이 곧 닫히더라","천부장이 영내에서 내려와 바울을 데려갑니다(21:31–34). 큰 여정 '예루살렘에서 로마까지'로 이어집니다.")]}
 ]});
})();
