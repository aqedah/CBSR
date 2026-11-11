/* ===== 공용 여정 부품 (2026-11-12, 목사님 승인: claude/CBSR_여정화면_통일안_2026-11-11.md) =====
   모든 여정(큰 여정·대속죄일·평면도·공간 탐색·성 안 지도)이 같은 부품을 씁니다. 새로 만들지 않고 큰 여정에 있던 것을 꺼내 옮겼습니다.
   1 머리줄 jKick      장면 n / N · 책 장:절 (부제는 쓰지 않음, 목사님 결정 2)
   2 두 단추 jGo*      📖 본문 펼치기 + ○장 읽는 날 (모든 여정)
   3 인물의 말 jBub*   인물 옆 말풍선(.tvb.say, 꼬리가 인물을 가리킴) — 위 카드에 넣지 않음(목사님 결정 1)
   4 이름표 jPill*     인물 = 빨간 알약, 장소 = 흰 알약(+추정·자리 미상 꼬리말). 화면 크기와 상관없이 같은 글씨 크기
   5 겹침 정리 jDeclutter  이름표가 겹치면 앞 순서(주인공 → 다른 인물 → 장소)만 남김
   6 안내 띠 jToast     짧은 안내는 지도 위가 아니라 아래 카드 바로 위 한 줄에, 차례로
   7 자리 맞춤 jFit     양피지 지도는 위 말씀 카드와 아래 카드 사이 빈 곳에만(목사님 결정 4)
*/
const JNS="http://www.w3.org/2000/svg";
/* 설명 3줄 접기(목사님 승인 대기 — false면 꺼짐). 켜면 아래 카드 설명이 3줄로 접히고 '더 보기'로 펼침, 펼친 동안 멈춤 */
const JCLAMP=3; /* 목사님 2026-11-12: 3줄 접기로 정함(설명창 안의 색 다른 '더 보기') */ /* 0 꺼짐 · 2 = 2줄로 접고 '더 보기'는 단추 줄에 · 3 = 3줄로 접고 '더 보기'는 설명 아래 */
function jClamp(el){ const n=el.querySelector(".bmtn"); if(!n) return; let b=el.querySelector(".jmore"); if(!JCLAMP){ n.classList.remove("jclamp","jc2"); if(b) b.hidden=true; return; } n.classList.add("jclamp"); n.classList.toggle("jc2",JCLAMP===2);
  if(!b){ b=document.createElement("button"); b.className="jmore"; b.dataset.t="more"; const g=el.querySelector(".bmtgo"); if(JCLAMP===2&&g){ b.classList.add("inrow"); g.appendChild(b); } else n.after(b); } b.textContent="더 보기 ▾"; b.hidden=true; requestAnimationFrame(()=>{ b.hidden=!(n.scrollHeight>n.clientHeight+2); }); }
function jMore(el){ const n=el.querySelector(".bmtn"), b=el.querySelector(".jmore"); const open=n.classList.toggle("jclamp")===false; if(b) b.textContent=open?"접기 ▴":"더 보기 ▾"; return open; }
function jKick(i,n,lab){ return `${i+1} / ${n}${lab?" · "+lab:""}`; }
/* 두 단추: 큰 여정과 같은 자리·같은 말 */
function jGoHTML(){ return `<div class="bmtgo" hidden><button data-t="verse">📖 본문 펼치기</button><button data-t="day" hidden></button></div>`; }
function jGoSet(root,r){ const g=root.querySelector(".bmtgo"); if(!g) return; g.hidden=!r; if(!r) return; const db=g.querySelector('[data-t="day"]'); if(!db) return; let D=null; try{ D=dayOfRef(r); }catch(e){} db.hidden=!D; if(D) db.textContent=`${PLAN.abbr[r[0]-1]} ${r[1]}${r[0]===19?"편":"장"} 읽는 날 · ${fmt(dateOf(D[0],D[1]),{month:"long",day:"numeric"})} ›`; }
function jGoDay(r,close){ let D=null; try{ D=r&&dayOfRef(r); }catch(e){} if(!D) return; close(); try{ bmLeave(); }catch(e){} go(D[0],D[1]); }

/* 말풍선: 큰 여정의 .tvb.say 그대로 */
function jBubEl(fr,who,text,ref){ const d=document.createElement("div"); d.className="tvb say"; d.innerHTML=`${who?`<span class="mvtag">${esc(who)}</span>`:""}${esc(text)}${ref?`<small>${esc(vLab(ref))}</small>`:""}<i class="mvtail"></i>`; fr.appendChild(d); return d; }
/* 말풍선 자리: 인물 머리 위 → 옆 → 아래 가운데서 인물·다른 것을 가장 덜 가리는 곳(큰 여정 vbPlace에서 꺼냄)
   p: 인물 화면 좌표 {x,y} 또는 null(말한 이가 지도에 없으면 위 가운데) · o: {W,top0,bot,avoid:[{x0,x1,y0,y1}]} */
function jPlaceBub(d,p,o){ const w=d.offsetWidth, h=d.offsetHeight, W=o.W, top0=o.top0, bot=o.bot, avoid=o.avoid||[];
  if(!p){ d.style.transform=`translate(${Math.round((W-w)/2)}px,${Math.round(top0)}px)`; d.classList.remove("tup","tdn"); return; }
  const area=(a,b)=>Math.max(0,Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0))*Math.max(0,Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0));
  let best=null, bs=1e18; for(const [dx,dy] of [[-w/2,-h-66],[-w+26,-h-66],[-26,-h-66],[-w/2,16],[-w+26,16],[-26,16]]){ const x=Math.max(10,Math.min(W-w-10,p.x+dx)), y=Math.max(top0,Math.min(bot-h,p.y+dy)), r={x0:x,x1:x+w,y0:y,y1:y+h}; const sc=avoid.reduce((t,a)=>t+area(r,a),0)*10+Math.hypot(x+w/2-p.x,y+h/2-p.y); if(sc<bs){ bs=sc; best=r; } }
  d.style.transform=`translate(${Math.round(best.x0)}px,${Math.round(best.y0)}px)`; mvTail(d,best.x0,best.y0,w,h,p.x,p.y); }

/* 이름표(SVG 안): 화면에서 늘 같은 글씨 크기가 되도록 지도 배율로 나눔 */
function jPx(svg){ try{ const m=svg.getScreenCTM(); return (m&&m.a)||1; }catch(e){ return 1; } }
const JPILL_FS={who:12.5,place:11.5};
/* 글자(text)를 알약으로 감쌈. 글자는 g 안의 (0,0)으로 옮기고 g가 자리를 가짐(움직일 때 jPillAt) */
function jPillWrap(svg,t,kind){ if(!t||t.closest("g.jp")) return t&&t.closest("g.jp"); const s=1/jPx(svg); const x=+(t.getAttribute("x")||0), y=+(t.getAttribute("y")||0), tr=t.getAttribute("transform")||"";
  let est=t.classList.contains("pk-i"), unk=t.classList.contains("pk-u"), vis=t.classList.contains("pk-v"); let txt=t.textContent.trim(); if(/\?$/.test(txt)){ est=true; txt=txt.replace(/\?$/,""); }
  const g=document.createElementNS(JNS,"g"); g.setAttribute("class",`jp ${kind}${est?" est":""}${unk?" unk":""}${vis?" vis":""}`); if(t.id){ g.id="jp_"+t.id; }
  const rot=tr.match(/rotate\(\s*([-\d.]+)(?:[\s,]+([-\d.]+)[\s,]+([-\d.]+))?\s*\)/); g.setAttribute("transform",`translate(${x} ${y})${rot?` rotate(${rot[1]})`:""}`);
  if(t.hasAttribute("data-off")){ g.setAttribute("data-off",t.getAttribute("data-off")); t.removeAttribute("data-off"); }
  t.parentNode.insertBefore(g,t); g.appendChild(t); const an=t.getAttribute("text-anchor")||"start"; t.removeAttribute("transform"); t.removeAttribute("style"); t.setAttribute("x",0); t.setAttribute("y",0); t.setAttribute("text-anchor",an); t.setAttribute("class",""); t.setAttribute("dominant-baseline","central");
  const fs=(JPILL_FS[kind]||11.5)*s; t.style.fontSize=fs+"px"; t.textContent=txt;
  if(est||(unk&&!/미상/.test(txt))){ const sp=document.createElementNS(JNS,"tspan"); sp.textContent=est?" 추정":" 자리 미상"; sp.style.fontSize=(fs*.8)+"px"; t.appendChild(sp); }
  const b=t.getBBox(), px=5*s, py=1.6*s, r=document.createElementNS(JNS,"rect"); r.setAttribute("x",b.x-px); r.setAttribute("y",b.y-py); r.setAttribute("width",b.width+px*2); r.setAttribute("height",b.height+py*2); r.setAttribute("rx",(b.height+py*2)/2); g.insertBefore(r,t); return g; }
/* 새 알약 하나 */
function jPill(svg,par,x,y,text,o){ o=o||{}; const t=document.createElementNS(JNS,"text"); t.setAttribute("x",x); t.setAttribute("y",y); if(o.anchor) t.setAttribute("text-anchor",o.anchor); if(o.k==="i") t.classList.add("pk-i"); if(o.k==="u") t.classList.add("pk-u"); if(o.k==="v") t.classList.add("pk-v"); t.textContent=text; par.appendChild(t); return jPillWrap(svg,t,o.kind||"place"); }
function jPillAt(g,x,y){ if(!g) return; const tr=g.getAttribute("transform")||"", rot=tr.match(/rotate\([^)]*\)/); g.setAttribute("transform",`translate(${x} ${y})${rot?" "+rot[0]:""}`); }
/* 지도 안의 글자를 이름표로 바꿈: data-jn="who" → 인물 알약, class="pl"(흐린 글씨 m·큰 지역 이름 big이 아닌 것) → 장소 알약 */
function jPillify(svg,root){ root=root||svg; root.querySelectorAll('text[data-jn="who"]').forEach(t=>jPillWrap(svg,t,"who")); root.querySelectorAll("text.pl").forEach(t=>{ const c=t.classList; if(c.contains("m")||c.contains("big")||c.contains("v")||t.closest("g.jp")||t.closest("#pl_fx")||t.closest("#at_fx")) return; jPillWrap(svg,t,"place"); }); }
/* 겹침 정리: 보이는 알약을 순서대로(인물 먼저) 놓고, 앞의 것과 겹치면 숨김 */
function jVisible(e,stop){ for(let n=e.parentNode;n&&n!==stop;n=n.parentNode){ /* 알약 자신의 투명도(겹침 정리로 숨겼다 보이는 중)는 보지 않음 */ if(n.nodeType!==1) continue; const o=n.getAttribute("opacity"); if(o!=null&&+o===0) return false; const cs=getComputedStyle(n); if(cs.display==="none"||+cs.opacity===0) return false; } return true; }
function jDeclutter(svg){ const all=[...svg.querySelectorAll("g.jp")]; /* 목사님 2026-11-12: 지금 말하는 사람의 이름을 가장 먼저 남김 → 다른 인물 → 장소 */
  const root=svg.closest(".atn")||document, spk=new Set([...root.querySelectorAll(".tvb.say:not(.old)")].map(d=>d._spkG).filter(Boolean));
  const order=[...all.filter(g=>spk.has(g)),...all.filter(g=>g.classList.contains("who")&&!spk.has(g)),...all.filter(g=>!g.classList.contains("who"))]; const kept=[];
  order.forEach(g=>{ g.classList.remove("hid"); if(!jVisible(g,svg)) return; const r=g.getBoundingClientRect(); if(!r.width) return; const hit=kept.some(k=>r.left<k.right-1&&r.right>k.left+1&&r.top<k.bottom-1&&r.bottom>k.top+1); if(hit) g.classList.add("hid"); else kept.push(r); }); }

/* 안내 띠: 아래 카드 바로 위에 한 줄, 여러 개면 차례로 */
function jToast(el,text){ if(!el||!text) return; const q=el._jtq||(el._jtq=[]); q.push(String(text)); if(el._jtBusy) return;
  const next=()=>{ const t=q.shift(); if(t==null||!document.body.contains(el)){ el._jtBusy=false; return; } el._jtBusy=true; let d=el.querySelector(":scope>.jtoast"); if(!d){ d=document.createElement("div"); d.className="jtoast"; d.setAttribute("role","status"); el.appendChild(d); }
    const p=el.querySelector(".bmtp"), R=el.getBoundingClientRect(); const top=p?p.getBoundingClientRect().top-R.top+30:R.height*.6; d.style.bottom=Math.max(0,R.height-top+6)+"px"; d.textContent=t; d.classList.add("on");
    el._jtT=setTimeout(()=>{ d.classList.remove("on"); el._jtT=setTimeout(next,300); },Math.max(2400,Math.min(4600,1200+t.length*90))); };
  next(); }
function jToastClear(el){ if(!el) return; if(el._jtq) el._jtq.length=0; clearTimeout(el._jtT); el._jtBusy=false; el.querySelector(":scope>.jtoast")?.classList.remove("on"); }

/* 자리 맞춤: 모든 장면의 아래 카드 가운데 가장 높은 것을 재어, 지도가 그 위 빈 곳에만 그려지게 */
function jFit(el,rows){ const p=el.querySelector(".bmtp"); if(!p) return; const k=p.querySelector(".bmtk"), h=p.querySelector(".bmth"), n=p.querySelector(".bmtn"), g=p.querySelector(".bmtgo"), keep=[k.textContent,h.textContent,n.textContent,g&&g.hidden];
  if(JCLAMP){ n.classList.add("jclamp"); n.classList.toggle("jc2",JCLAMP===2); }
  let mx=0; if(g) g.hidden=false; rows.forEach(r=>{ k.textContent=r[0]||""; h.textContent=r[1]||""; n.textContent=r[2]||""; mx=Math.max(mx,p.offsetHeight); });
  k.textContent=keep[0]; h.textContent=keep[1]; n.textContent=keep[2]; if(g) g.hidden=keep[3];
  const H=el.clientHeight||innerHeight; el.style.setProperty("--jcard",Math.round(Math.min(mx-30,H*.5))+"px"); }
/* 길 모양 규칙(목사님 2026-11-12 확정): ① 빨간 실선 본문 ② 빨간 점선 추정 ③ 남색 긴 점선 배 ④ 짙은 빨강 굵은 선 군대 ⑤ 회색 점점선 포로 ⑥ 갈색 가는 선 따로 가는 무리 ⑦ 지나온 길은 흐리게 ⑧ 범례는 첫 화면에만 */
const JLINE={solid:["#c0392b",5,"","본문이 말하는 이동"],est:["#c0392b",5,"6 8","추정 이동"],sea:["#1f4f86",4,"12 6","배로 간 길"],army:["#7d1414",6,"","군대"],captive:["#55524a",4,"1 9","포로로 끌려감"],side:["#8a5a2b",3,"","따로 가는 무리"]};
function jLegHTML(kinds){ const K=["solid","est","sea","army","captive","side"].filter(k=>kinds.has(k)); if(!K.length) return ""; return `<div class="jleg" aria-label="길 모양">${K.map(k=>{ const [c,w,d,n]=JLINE[k]; return `<span><svg viewBox="0 0 30 10" width="30" height="10" aria-hidden="true"><path d="M2 5 H28" stroke="${c}" stroke-width="${Math.min(w,4)}" stroke-dasharray="${d}" stroke-linecap="${k==="captive"?"round":"butt"}" fill="none"/></svg>${n}</span>`; }).join("")}</div>`; }
function jUnclamp(el){ el.querySelector(".bmtn")?.classList.remove("jclamp"); const b=el.querySelector(".jmore"); if(b) b.hidden=true; }
try{ Object.assign(window,{jKick,jPill,jPillify,jDeclutter,jToast,jFit}); }catch(e){}
