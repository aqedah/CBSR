/* ===== 공용 평면도 여정 엔진 planOpen (목사님 2026-11-10 승인: 세부 지도 7편 + 사사기)
   대속죄일(atoneOpen)과 같은 틀(전체 화면 양피지 · 위 진행 막대 · 위 말씀 카드 · 아래 장면 카드 · 가운데 ▶)을 쓰되,
   그림(SVG)과 장면 자료만 바꿔 끼우는 공용 함수. 대속죄일 코드는 손대지 않음(이미 검수됨).
   장면 자료 한 칸:
     s   장·절 글자("40:17–19")      t 제목   d 풀이(서술)   q 개역개정 인용(그대로)   r [책,장,절] 인용 자리
     god 참이면 하나님 말씀 표지     who 움직이는 인물 열쇠(기본 "me")   path [[x,y],…] 걷는 길   moves {인물:path} 여럿이 동시에
     show/hide [id,…] 그림 요소 켜고 끄기   label [[x,y,글,k,anchor],…] 잠깐 뜨는 꼬리표   fx [[이름,…인자],…] 또는 함수
     night 참이면 밤   map 열쇠(그림 바꾸기, 에스겔)   hold 읽는 시간(ms)   pray 참이면 🙏
   정보 성격 k(GPT 2026-11-10 §5-①): t 본문 명시(실선) · i 본문 근거 추론(점선, ?) · r 복원도(회색) · u 위치 미상(흐림) · v 환상(보라)
   앞 장면들의 show/hide/위치를 합산해 상태를 만들므로, 장면을 건너뛰어도 그림이 어긋나지 않음. */
const PLANS={};
function planReg(sp){ PLANS[sp.id]=sp; return sp; }
const PLAN_K={t:"",i:"pk-i",r:"pk-r",u:"pk-u",v:"pk-v"};
function planCard(id){ const p=PLANS[id]; if(!p) return ""; return `<button class="bmtc" data-plan="${id}"><i>▶</i><b>${esc(p.card||p.title)}</b><small><span>${esc(p.sub||p.kicker||"")}</span></small><em>${p.scenes.length}장면 따라가기</em></button>`; }
/* 오늘 읽는 장에 걸린 평면도 여정 단추(tourHere에서 부름) */
function planHere(p){ if(!p) return []; const has=(b,c)=>p.ch.some(x=>x[0]===b&&x[1]===c); const out=[];
  for(const id in PLANS){ const sp=PLANS[id]; if(!sp.open) continue; const si=sp.scenes.findIndex(sc=>sc.r&&has(sc.r[0],sc.r[1])); const hit=si>=0||sp.open.some(([b,c])=>has(b,c)); if(!hit) continue;
    out.push(`<button class="tourhere" data-plan="${id}" data-s="${Math.max(0,si)}"><i>▶</i><span><b>${esc(sp.title)}</b><small>${esc(sp.here||sp.kicker||"")} · ${sp.scenes.length}장면${si>0?` · ${si+1}번째 장면부터`:""}</small></span></button>`); }
  return out; }
document.addEventListener("click",e=>{ const b=e.target.closest&&e.target.closest("[data-plan]"); if(!b) return; e.preventDefault(); e.stopPropagation(); try{ document.querySelector("#sheetX")?.click(); }catch(e2){} planOpen(b.dataset.plan,+(b.dataset.s||0)); });

function planOpen(id,s0){ const SP=PLANS[id]; if(!SP) return; document.querySelector(".atn")?.remove();
  const el=document.createElement("div"); el.className="bmt2 atn pln"; el.setAttribute("role","dialog"); el.setAttribute("aria-label",SP.title);
  const VB=SP.vb||[300,430], S=SP.scenes, maps=SP.maps||{}, map0=S[0].map||Object.keys(maps)[0]||null;
  el.innerHTML=`<div class="bmtmap atmap"><svg class="map" id="pl_svg" preserveAspectRatio="xMidYMid meet" viewBox="0 0 ${VB[0]} ${VB[1]}" role="img" aria-label="${esc(SP.aria||SP.title)}">
    <defs><radialGradient id="pl_smk"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
      <radialGradient id="pl_glow"><stop offset="0" stop-color="#fff3c0" stop-opacity=".98"/><stop offset=".55" stop-color="#ffd978" stop-opacity=".55"/><stop offset="1" stop-color="#ffd978" stop-opacity="0"/></radialGradient>
      <filter id="pl_blur"><feGaussianBlur stdDeviation="2.4"/></filter><filter id="pl_blur6"><feGaussianBlur stdDeviation="6"/></filter></defs>
    <g id="pl_base">${map0?maps[map0].svg||maps[map0]:(SP.svg||"")}</g>
    <rect id="pl_night" x="-20" y="-20" width="${VB[0]+40}" height="${VB[1]+40}" fill="#0d1230" opacity="0" style="transition:opacity 1.2s;pointer-events:none"/>
    <g id="pl_fx"></g><g id="pl_trails"></g><g id="pl_actors"></g>
  </svg></div><div class="bmtbars">${S.map(()=>`<span><i></i></span>`).join("")}</div>
   ${SP.parts?`<div class="bmtparts"><div class="bmtpc">${SP.parts.map((p,k)=>`<button data-t="part" data-k="${k}">${esc(p.t)}</button>`).join("")}</div></div>`:""}
   <div class="bmttop"><b>${esc(SP.title)}</b><button class="bmtic" data-t="prev" aria-label="이전 장면">‹</button><button class="bmtic" data-t="pause" aria-label="멈춤">❚❚</button><button class="bmtic" data-t="nextS" aria-label="다음 장면">›</button><button class="bmtic" data-t="x" aria-label="닫기">✕</button></div>
   <div class="bmtp"><p class="bmtk"></p><h3 class="bmth"></h3><p class="bmtn"></p><p class="athold"></p>${SP.note?`<p class="plnote">${esc(SP.note)}</p>`:""}<div class="bmtend" hidden><button class="btn bmtag" data-t="again">↺ 처음부터</button><button class="btn bmtcl" data-t="x">닫기</button></div></div>
   <p class="bmthint">‹ › 장면 넘기기 · ❚❚ 멈춤</p>`;
  document.body.appendChild(el); document.body.style.overflow="hidden";
  const $=i=>el.querySelector("#"+i), NS="http://www.w3.org/2000/svg", svg=$("pl_svg"); let fx=$("pl_fx");
  const IMG={}; const img=k=>{ if(IMG[k]) return IMG[k]; try{ IMG[k]="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(C(k).replace("<svg ",'<svg xmlns="http://www.w3.org/2000/svg" width="60" height="92" ')); }catch(e){ IMG[k]=""; } return IMG[k]; };
  const mk=(tag,attrs,par)=>{ const e=document.createElementNS(NS,tag); for(const k in attrs) e.setAttribute(k,attrs[k]); (par||fx).appendChild(e); return e; };
  const LBL=(x,y,t,k,anchor,par,sz)=>{ const e=mk("text",{x,y,class:"pl "+(PLAN_K[k||"t"]||""),"text-anchor":anchor||"middle",style:`font-size:${sz||9.5}px;font-weight:700;paint-order:stroke;stroke:#f3e6c4;stroke-width:3px`},par); e.textContent=(k==="i"&&!/\?$/.test(t))?t+"?":t; return e; };
  /* 인물: SP.actors={me:{ch:"moses",n:"모세",w:26,side:1}} — 그림은 CH_DEF 도트 인물 */
  const AC={}; const actor=k=>{ if(AC[k]) return AC[k]; const a=(SP.actors||{})[k]||{ch:"man",n:k}; const g=mk("g",{id:"pl_a_"+k,opacity:0},$("pl_actors")); const w=a.w||24, h=Math.round(w*1.54);
    g.innerHTML=`<ellipse cx="0" cy="0" rx="${w*.32}" ry="${w*.1}" fill="rgba(60,40,20,.33)"/>${a.svg?`<g class="pimg">${a.svg}</g>`:`<image class="pimg" href="${img(a.ch)}" x="${-w/2}" y="${-h+3}" width="${w}" height="${h}"/>`}${a.n?`<text x="${a.side<0?-(w/2+2):w/2+2}" y="${-h+14}" text-anchor="${a.side<0?"end":"start"}" style="font:700 ${a.fs||8.5}px 'Noto Serif KR',serif;fill:${a.col||"#3e2a12"};paint-order:stroke;stroke:#f3e6c4;stroke-width:3px">${esc(a.n)}</text>`:""}`;
    const tr=mk("path",{class:"route pl_tr",d:"",style:a.trail===false?"display:none":""},$("pl_trails")); AC[k]={g,tr,pts:[],at:null,def:a}; return AC[k]; };
  const setAt=(k,x,y)=>{ const a=actor(k); a.at=[x,y]; a.g.setAttribute("transform",`translate(${x} ${y})`); a.g.setAttribute("opacity",1); };
  const hideA=k=>{ const a=actor(k); a.g.setAttribute("opacity",0); };
  const D=a=>a.length>1?"M"+a.map(p=>p.join(" ")).join(" L"):"";
  const bars=[...el.querySelectorAll(".bmtbars i")], RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
  let cur=0, paused=false, tok=0;
  const sleep=async ms=>{ if(RM) ms=0; let t=0; while(t<ms){ const d=Math.min(60,ms-t); await new Promise(r=>setTimeout(r,d)); if(!paused) t+=d; } };
  async function walk(k,path,my,spd){ const a=actor(k); if(!a.at&&path.length){ setAt(k,...path[0]); } a.pts=[a.at?a.at.slice():path[0]]; const im=a.g.querySelector(".pimg"); if(im) im.classList.add("pwalk");
    for(let i=0;i<path.length;i++){ const [x0,y0]=a.at||path[0], [x1,y1]=path[i]; const n=Math.max(1,Math.round(Math.hypot(x1-x0,y1-y0)/(spd||2.4)));
      for(let j=1;j<=n;j++){ if(my!==tok){ if(im) im.classList.remove("pwalk"); return false; } while(paused&&my===tok) await sleep(120); const x=x0+(x1-x0)*j/n, y=y0+(y1-y0)*j/n; setAt(k,x,y); a.pts.push([+x.toFixed(1),+y.toFixed(1)]); a.tr.setAttribute("d",D(a.pts)); await sleep(16); } }
    if(im) im.classList.remove("pwalk"); return true; }
  const vis=(id,on,ms)=>{ const e=$(id); if(!e) return; e.getAnimations().forEach(a=>a.cancel()); if(ms){ e.animate([{opacity:on?0:1},{opacity:on?1:0}],{duration:ms,fill:"forwards"}); } else e.style.opacity=on?1:0; e.setAttribute("data-on",on?1:0); };
  const setMap=k=>{ if(!k||!maps[k]) return; const m=maps[k]; $("pl_base").innerHTML=m.svg||m; if(m.vb) svg.setAttribute("viewBox",`0 0 ${m.vb[0]} ${m.vb[1]}`); };
  /* 공용 효과 */
  const FX={
    fire:(x,y,r)=>{ const c=mk("circle",{cx:x,cy:y,r:r||6,fill:"#e98a2b",opacity:.85}); c.animate([{r:(r||6)*.8,opacity:.5},{r:(r||6)*1.6,opacity:1},{r:(r||6)*1.1,opacity:.8}],{duration:1500,iterations:Infinity}); const s=mk("circle",{cx:x,cy:y-12,r:7,fill:"url(#pl_smk)",filter:"url(#pl_blur)"}); s.animate([{cy:y-10,opacity:.8},{cy:y-38,opacity:0}],{duration:2200,iterations:Infinity}); },
    smoke:(x,y,n)=>{ for(let k=0;k<(n||5);k++){ const c=mk("circle",{cx:x+(k-((n||5)-1)/2)*5,cy:y,r:5,fill:"url(#pl_smk)",filter:"url(#pl_blur)",opacity:0}); c.animate([{opacity:0,r:4},{opacity:.95,r:18}],{duration:1800,delay:k*240,fill:"forwards"}); } },
    water:(x,y)=>{ for(let r=0;r<3;r++){ const c=mk("circle",{cx:x,cy:y,r:8,fill:"none",stroke:"#5b8fa8","stroke-width":1.6}); c.animate([{r:8,opacity:.9},{r:22,opacity:0}],{duration:1200,delay:r*350,fill:"forwards"}); } },
    glow:(x,y,r,ms)=>{ const c=mk("circle",{cx:x,cy:y,r:r||26,fill:"url(#pl_glow)",opacity:0}); c.animate([{opacity:0},{opacity:1}],{duration:ms||1200,fill:"forwards"}); return c; },
    cloud:(x,y,w,h)=>{ const g=mk("g",{opacity:0}); for(let k=0;k<9;k++){ const c=document.createElementNS(NS,"circle"); c.setAttribute("cx",x+(k%3-1)*w*.3+(Math.random()-.5)*w*.15); c.setAttribute("cy",y+(Math.floor(k/3)-1)*h*.3); c.setAttribute("r",Math.max(w,h)*.3); c.setAttribute("fill","#fff"); c.setAttribute("filter","url(#pl_blur6)"); g.appendChild(c); } g.animate([{opacity:0},{opacity:.92}],{duration:1800,fill:"forwards"}); return g; },
    dark:(a)=>{ const r=mk("rect",{x:-20,y:-20,width:VB[0]+40,height:VB[1]+40,fill:"#120b06",opacity:0}); r.animate([{opacity:0},{opacity:a||.55}],{duration:2200,fill:"forwards"}); },
    quake:()=>{ svg.animate([{transform:"translate(0,0)"},{transform:"translate(-3px,2px)"},{transform:"translate(3px,-1px)"},{transform:"translate(-2px,-2px)"},{transform:"translate(2px,2px)"},{transform:"translate(0,0)"}],{duration:700,iterations:3}); },
    tear:(x,y1,y2)=>{ const l=mk("line",{x1:x,y1:y1,x2:x,y2:y1,stroke:"#2a1d0c","stroke-width":2.2}); l.animate([{y2:y1},{y2:y2}],{duration:900,fill:"forwards"}); },
    emo:(x,y,t,ms)=>{ const e=mk("text",{x,y,"text-anchor":"middle",style:"font-size:15px"}); e.textContent=t; e.animate([{opacity:0,transform:"translateY(6px)"},{opacity:1,transform:"none",offset:.15},{opacity:1,offset:.85},{opacity:0,transform:"translateY(-6px)"}],{duration:ms||3600,fill:"forwards"}); },
    dot:(x,y,col,r)=>{ const c=mk("circle",{cx:x,cy:y,r:r||3,fill:col||"#a5361f"}); c.animate([{opacity:0},{opacity:1}],{duration:300,fill:"forwards"}); return c; },
    ring:(x,y,col)=>{ for(let r=0;r<3;r++){ const c=mk("circle",{cx:x,cy:y,r:6,fill:"none",stroke:col||"#a5361f","stroke-width":1.8}); c.animate([{r:6,opacity:.9},{r:24,opacity:0}],{duration:1400,delay:r*400,fill:"forwards"}); } },
    sound:(x,y,n)=>{ for(let r=0;r<(n||4);r++){ const c=mk("circle",{cx:x,cy:y,r:10,fill:"none",stroke:"#8a6a20","stroke-width":1.4,opacity:0}); c.animate([{r:10,opacity:.9},{r:60+r*10,opacity:0}],{duration:1600,delay:r*300,fill:"forwards"}); } },
    label:(x,y,t,k,anchor)=>{ const e=LBL(x,y,t,k,anchor); e.animate([{opacity:0},{opacity:1,offset:.12},{opacity:1,offset:.86},{opacity:0}],{duration:3000,fill:"forwards"}); },
    pin:(x,y,t,k,anchor)=>{ LBL(x,y,t,k,anchor); },
    x:(x,y,t)=>{ const e=mk("text",{x,y,"text-anchor":"middle",class:"pl",style:"font-size:10px;font-weight:800;fill:#8f1d0f;paint-order:stroke;stroke:#f3e6c4;stroke-width:3px"}); e.textContent="✕ "+t; e.animate([{opacity:0},{opacity:1}],{duration:600,fill:"forwards"}); }
  };
  const runFx=async(list,my,sc)=>{ if(!list) return true; if(typeof list==="function") return (await list({el,svg,fx,mk,FX,actor,setAt,hideA,walk,sleep,vis,LBL,my,tok:()=>tok,sc,SP,img,NS}))!==false;
    for(const it of list){ if(my!==tok) return false; if(typeof it==="function"){ if((await it({el,svg,fx,mk,FX,actor,setAt,hideA,walk,sleep,vis,LBL,my,tok:()=>tok,sc,SP,img,NS}))===false) return false; continue; }
      const [n,...a]=it; if(n==="wait"){ await sleep(a[0]||800); continue; } if(n==="walk"){ if(!(await walk(a[0],a[1],my,a[2]))) return false; continue; } if(n==="at"){ setAt(a[0],a[1],a[2]); continue; } if(n==="hideA"){ hideA(a[0]); continue; } if(n==="show"){ vis(a[0],true,a[1]||700); continue; } if(n==="hide"){ vis(a[0],false,a[1]||700); continue; }
      if(SP.fx&&SP.fx[n]){ if((await SP.fx[n]({el,svg,fx,mk,FX,actor,setAt,hideA,walk,sleep,vis,LBL,my,tok:()=>tok,sc,SP,img,NS},...a))===false) return false; continue; } if(FX[n]) FX[n](...a); }
    return my===tok; };
  function cap(i){ const s=S[i]; const bk=s.r?PLAN.abbr[s.r[0]-1]:(SP.abbr||""); el.querySelector(".bmtk").textContent=`${i+1} / ${S.length} · ${bk} ${s.s||""}`; el.querySelector(".bmth").textContent=s.t; el.querySelector(".bmtn").textContent=s.d||""; el.querySelector(".athold").innerHTML=s.h?`<em>${esc(s.h)}</em>`:""; bars.forEach((b,j)=>{ b.style.transition="none"; b.style.width=j<i?"100%":"0"; }); el.querySelector(".bmtend").hidden=true;
    if(SP.parts){ let a=0; SP.parts.forEach((p,k)=>{ if(p.at<=i) a=k; }); el.querySelectorAll(".bmtpc button").forEach((b,k)=>b.classList.toggle("on",k===a)); } }
  /* 상태 재구성: 0..i-1 장면의 show/hide·위치·지도·밤을 합산 */
  function build(i){ { const nf=fx.cloneNode(false); fx.replaceWith(nf); fx=nf; } let mp=map0; for(let j=0;j<=i;j++) if(S[j].map) mp=S[j].map; setMap(mp);
    const on={}; (SP.init||[]).forEach(id=>on[id]=1); for(let j=0;j<i;j++){ (S[j].show||[]).forEach(id=>on[id]=1); (S[j].hide||[]).forEach(id=>on[id]=0); for(const L of [S[j].pre,S[j].fx]) if(Array.isArray(L)) L.forEach(it=>{ if(Array.isArray(it)&&(it[0]==="show"||it[0]==="hide")) on[it[1]]=it[0]==="show"?1:0; }); }
    svg.querySelectorAll("#pl_base [id]").forEach(e=>{ const id=e.id; if(id in on){ e.getAnimations().forEach(a=>a.cancel()); e.style.opacity=on[id]?1:0; } else if(e.hasAttribute("data-off")) e.style.opacity=0; });
    for(const k in AC){ AC[k].g.getAnimations().forEach(a=>a.cancel()); AC[k].g.setAttribute("opacity",0); AC[k].at=null; AC[k].pts=[]; AC[k].tr.setAttribute("d",""); }
    const pos={}, gone={}, oldT={}; for(let j=0;j<i;j++){ const s=S[j]; const mv=Object.assign({},s.moves||{}); if(s.path) mv[s.who||"me"]=s.path; for(const k in mv){ pos[k]=mv[k][mv[k].length-1]; delete gone[k]; (oldT[k]=oldT[k]||[]).push(...mv[k]); } (s.at||[]).forEach(([k,x,y])=>{ pos[k]=[x,y]; delete gone[k]; }); (s.gone||[]).forEach(k=>{ gone[k]=1; }); for(const L of [s.pre,s.fx]) if(Array.isArray(L)) L.forEach(it=>{ if(!Array.isArray(it)) return; if(it[0]==="hideA") gone[it[1]]=1; else if(it[0]==="at"){ pos[it[1]]=[it[2],it[3]]; delete gone[it[1]]; } else if(it[0]==="walk"&&it[2]&&it[2].length){ pos[it[1]]=it[2][it[2].length-1]; delete gone[it[1]]; } }); }
    for(const k in pos){ if(gone[k]) continue; setAt(k,...pos[k]); } for(const k in oldT){ if(gone[k]) continue; const a=actor(k); if(a.def.trail===false) continue; let o=$("pl_old_"+k); if(!o){ o=mk("path",{id:"pl_old_"+k,class:"route",style:"opacity:.28"},$("pl_trails")); } o.setAttribute("d",D(oldT[k])); }
    svg.querySelectorAll("#pl_trails [id^=pl_old_]").forEach(o=>{ const k=o.id.slice(7); if(!(k in oldT)||gone[k]) o.setAttribute("d",""); });
    let night=false; for(let j=0;j<=i;j++) if("night" in S[j]) night=!!S[j].night; $("pl_night").setAttribute("opacity",night?.42:0); }
  async function go(i){ const my=++tok; cur=Math.max(0,Math.min(S.length-1,i)); cap(cur); build(cur); el.querySelectorAll(":scope>.mvnar").forEach(n=>{ if(n._c) n._c(); n.classList.remove("on"); });
    const st=S[cur]; (st.at||[]).forEach(([k,x,y])=>setAt(k,x,y)); (st.gone||[]).forEach(k=>hideA(k));
    const hold=st.hold||Math.max(5200,Math.min(11000,1800+((st.q||"").length+(st.d||"").length*.4)*95)), b=bars[cur]; b.style.transition="none"; b.style.width="0"; void b.offsetWidth;
    (st.show||[]).forEach(id=>vis(id,true,900)); (st.hide||[]).forEach(id=>vis(id,false,900)); (st.label||[]).forEach(([x,y,t,k,an])=>FX.label(x,y,t,k,an));
    if(st.pre) await runFx(st.pre,my,st); if(my!==tok) return false;
    const mv=Object.assign({},st.moves||{}); if(st.path) mv[st.who||"me"]=st.path; const ks=Object.keys(mv); if(ks.length){ const rs=await Promise.all(ks.map(k=>walk(k,mv[k],my,st.spd))); if(rs.some(x=>!x)) return false; }
    const NT=SP.parts?106:66; if(st.q) mvNar(el,st.q,st.r,NT,hold,st.god?(st.godn||"여호와"):undefined); else if(st.say) mvNar(el,st.say,st.r,NT,hold,st.sayer?st.sayer:undefined);
    if(st.pray){ const a=actor(st.who||"me"); if(a.at) FX.emo(a.at[0],a.at[1]-44,"🙏"); }
    if(!(await runFx(st.fx,my,st))) return false;
    let t=0; while(t<hold){ if(my!==tok) return false; await new Promise(r=>setTimeout(r,150)); if(!paused){ t+=150; b.style.width=Math.min(100,t/hold*100)+"%"; } } return my===tok; }
  async function run(i){ for(let k=i;k<S.length;k++){ const ok=await go(k); if(!ok) return; } if(SP.end){ el.querySelector(".bmtn").textContent=SP.end; } el.querySelector(".bmtend").hidden=false; }
  const setPause=v=>{ paused=v; el.classList.toggle("paused",v); try{ document.getAnimations().forEach(a=>{ const tg=a.effect&&a.effect.target; if(tg&&el.contains(tg)) v?a.pause():a.play(); }); }catch(e){} const pb=el.querySelector('[data-t="pause"]'); pb.textContent=v?"▶":"❚❚"; pb.setAttribute("aria-label",v?"이어 보기":"멈춤"); };
  const close=pop=>{ tok++; el.remove(); document.body.style.overflow=""; if(pop!==true) ovDone(close); }; ovOpen(close);
  el.addEventListener("click",e=>{ const t=e.target.closest("[data-t]"); if(!t) return; const k=t.dataset.t;
    if(k==="x") close(); else if(k==="prev") run(Math.max(0,cur-1)); else if(k==="nextS") run(Math.min(S.length-1,cur+1)); else if(k==="pause") setPause(!paused); else if(k==="again"){ setPause(false); run(0); } else if(k==="part"){ el.querySelector(".bmtgo0")?.remove(); run(SP.parts[+t.dataset.k].at); } });
  /* 첫 화면: 설명을 보여 주고 가운데 ▶ 시작 */
  el.querySelector(".bmtk").textContent=SP.kicker||""; el.querySelector(".bmth").textContent=SP.title; el.querySelector(".bmtn").textContent=SP.intro||""; build(0); (S[0].at||[]).forEach(([k,x,y])=>setAt(k,x,y)); if(S[0].path&&!S[0].at) setAt(S[0].who||"me",...S[0].path[0]);
  { const st0=Math.max(0,Math.min(S.length-1,+s0||0)), b=document.createElement("button"); b.className="bmtgo0"; b.setAttribute("aria-label",st0?`${st0+1}번째 장면부터 시작`:"시작"); b.innerHTML=`<i>▶</i><span>${st0?`${st0+1}번째 장면부터`:"시작"}</span>`; el.appendChild(b); setTimeout(()=>b.focus(),30); b.onclick=e=>{ e.stopPropagation(); b.remove(); run(st0); }; }
  el.querySelector(".atmap").addEventListener("click",e=>{ if(el.querySelector(".bmtgo0")) return; if(e.target.closest(".bmtparts")) return; if(e.clientX<el.clientWidth*.3) run(Math.max(0,cur-1)); else if(cur<S.length-1) run(cur+1); }); }

/* 시험·점검용으로 바깥에서도 열 수 있게 */ try{ window.planOpen=planOpen; window.PLANS=PLANS; }catch(e){}
