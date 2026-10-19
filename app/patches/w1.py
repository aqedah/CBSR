p='/home/claude/rj/template3.html'; s=open(p).read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)>=1, a[:80]; s=s.replace(a,b,cnt)

# 1) 표시 주(일~토) 계산
rep('''const dateOf=(w,d)=>{const s=parseD(mem.start);s.setDate(s.getDate()+(w-1)*7+d);return s;};''','''const dateOf=(w,d)=>{const s=parseD(mem.start);s.setDate(s.getDate()+(w-1)*7+d);return s;};
/* 화면의 한 주는 늘 주일~토요일. 통독표 날짜(w,d)는 그대로 두고 보여 주는 묶음만 달력 주로 맞춥니다. */
const S0=()=>{const s=parseD(mem.start); s.setDate(s.getDate()-s.getDay()); return s;};
function NDW(){ const last=parseD(mem.start); last.setDate(last.getDate()+TOTAL_DAYS-1); return Math.floor(dayDiff(S0(),last)/7)+1; }
function cellOf(W,i){ const dt=S0(); dt.setDate(dt.getDate()+(W-1)*7+i); const n=dayDiff(parseD(mem.start),dt);
  if(n<0) return {dt,pre:true}; if(n>=TOTAL_DAYS) return {dt,after:true}; return {dt,w:Math.floor(n/7)+1,d:n%7}; }
const weekOfDay=(w,d)=>Math.floor(dayDiff(S0(),dateOf(w,d))/7)+1;
function dispW(){ if(view.pre) return 1; if(view.revW) return view.revW; return weekOfDay(view.w,view.d); }
const hasPre=()=>MODE==="rj"&&cellOf(1,0).pre&&dayDiff(parseD(mem.start),cellOf(1,0).dt)===-1;
function weekDays(W){ const L=[]; for(let i=0;i<7;i++){ const c=cellOf(W,i); if(c.w&&!isRev(c.d)) L.push([c.w,c.d]); } return L; }
function dispTitle(W){
  if(MODE==="rj") return W<=NW?`${W}주차 · ${WEEKS[W-1].t}`:`${NW}주차 돌아보기`;
  const L=weekDays(W); if(!L.length) return `${W}주차`;
  const a=dayPlan(...L[0]).ch[0], z=dayPlan(...L[L.length-1]).ch.slice(-1)[0];
  return `${W}주차 · `+(a[0]===z[0]?`${PLAN.abbr[a[0]-1]} ${a[1]}–${z[1]}`:`${PLAN.abbr[a[0]-1]} ${a[1]} – ${PLAN.abbr[z[0]-1]} ${z[1]}`);
}''')

# 2) 머리 부분(날짜줄, 주 제목, 날짜 칸)
i=s.index('function renderHead(){'); j=s.index('\n}\n',i)+3
s=s[:i]+r'''function renderHead(){
  const W=dispW(), NDWv=NDW();
  const dt=view.pre?cellOf(1,0).dt:view.revW?(()=>{let c; for(let i=6;i>=0;i--){ c=cellOf(W,i); if(c.w) break; } return c.dt;})():dateOf(view.w,view.d);
  document.getElementById("dateLine").textContent=fmt(dt,{month:"long",day:"numeric",weekday:"long"});
  document.getElementById("whereLine").innerHTML=view.pre?`<b>시작 주일</b> · 45주 여정 미리 보기`:view.revW?`<b>${W}주차</b> · 한 주 돌아보기`:isRev(view.d)?`<b>${view.w}주차</b> · 주일 · 한 주 돌아보기`:MODE==="y365"?`<b>${dayNo(view.w,view.d)}일째</b> · ${esc(dayPlan(view.w,view.d).label)}`:`<b>${view.w}주차</b> · ${view.d+1}일째 · ${esc(dayPlan(view.w,view.d).label)}`;
  const nb=document.getElementById("noticeBox"), isToday=!view.pre&&!view.revW&&view.w===here.w&&view.d===here.d;
  if(here.state==="before"&&isToday) nb.innerHTML=`<div class="notice">통독 시작일까지 ${-here.diff}일 남았습니다. 1주차를 미리 볼 수 있습니다.</div>`;
  else if(here.state==="after"&&isToday) nb.innerHTML=`<div class="notice">${esc(PI.name)} 일정이 끝났습니다. '나의 기록'에서 한 해를 돌아보세요.</div>`;
  else if(!isToday&&!view.pre&&!view.revW&&view.tab==="read") nb.innerHTML=`<div class="notice">오늘이 아닌 날을 보고 있습니다. '오늘'을 누르면 돌아갑니다.</div>`;
  else nb.innerHTML="";
  const a=cellOf(W,0).dt, z=cellOf(W,6).dt;
  document.getElementById("wkTitle").innerHTML=`<span class="wkt">${esc(dispTitle(W))}<i class="caret" aria-hidden="true">▾</i></span><small>${fmt(a,{month:"numeric",day:"numeric"})} – ${fmt(z,{month:"numeric",day:"numeric"})}</small>`;
  const st=document.getElementById("strip"); st.innerHTML="";
  const todayDt=today0();
  for(let i=0;i<7;i++){
    const c=cellOf(W,i), b=document.createElement("button"), dt2=c.dt;
    const isTodayCell=dayDiff(dt2,todayDt)===0;
    if(c.after||(c.pre&&!(hasPre()&&W===1&&i===0))){ b.className="day"; b.disabled=true; b.style.visibility="hidden"; st.appendChild(b); continue; }
    if(c.pre){
      b.className="day pre"+(view.pre?" sel":"")+(isTodayCell?" today":"");
      b.innerHTML=`<span class="dn">${DAYN[dt2.getDay()]}</span><span class="dd">${dt2.getDate()}</span><span class="ds">시작</span><span class="dc">미리 보기</span>`;
      b.setAttribute("aria-label",fmt(dt2,{month:"long",day:"numeric"})+" 시작 주일 미리 보기");
      b.onclick=()=>{view.pre=true;view.revW=null;view.open=false;view.quiz=null;view.wquiz=null;render();window.scrollTo({top:0});};
      st.appendChild(b); continue;
    }
    const w=c.w,d=c.d, rev=isRev(d);
    const sc=!rev?dayScore(w,d):mem.wq[w]?.first;
    const dn=!rev&&mem.done[keyOf(w,d)];
    const sel=!view.pre&&!view.revW&&view.w===w&&view.d===d;
    b.className="day"+(sel?" sel":"")+(w===here.w&&d===here.d&&here.state==="in"?" today":"")+(sc||dn?" done":"");
    b.innerHTML=`<span class="dn">${DAYN[dt2.getDay()]}</span><span class="dd">${dt2.getDate()}</span>${!rev?(()=>{const [bk,ch]=stripRef(dayPlan(w,d)); return `<span class="ds">${esc(bk)}</span><span class="dc${ch.length>=7?" long":""}">${esc(ch)||"&nbsp;"}</span>`;})():`<span class="ds">복습</span><span class="dc">${sc?sc.s+"/"+sc.t:`${w}주차`}</span>`}${dn||(!rev&&sc)?`<i class="dchk" aria-hidden="true">✓</i>`:""}`;
    b.setAttribute("aria-label",fmt(dt2,{month:"long",day:"numeric"})+" "+(!rev?dayPlan(w,d).label:`${w}주차 돌아보기`));
    b.onclick=()=>{view.pre=false;view.revW=null;view.w=w;view.d=d;view.open=false;view.quiz=null;view.wquiz=null;render();window.scrollTo({top:0});};
    st.appendChild(b);
  }
  const rr=document.getElementById("revRow");
  if(rr){ if(MODE==="y365"&&weekDays(W).length){ const T=weekTotalsList(weekDays(W)); const wf=mem.wq["c"+W]?.first;
      rr.innerHTML=`<button class="revchip${view.revW===W?" on":""}" id="revBtn"><span>이번 주 돌아보기</span><small>${T.n?`퀴즈 ${T.s}/${T.t}`:""}${wf?` · 도전 ${wf.s}/${wf.t}`:""}</small><b aria-hidden="true">›</b></button>`;
      document.getElementById("revBtn").onclick=()=>{view.revW=W;view.pre=false;view.open=false;view.quiz=null;view.wquiz=null;render();window.scrollTo({top:0});}; }
    else rr.innerHTML=""; }
  document.getElementById("prevW").disabled=W<=1;
  document.getElementById("nextW").disabled=W>=NDWv;
  document.getElementById("planName").textContent=PI.name; document.getElementById("planSrc").textContent=PI.src;
  document.querySelectorAll(".bnav .tab").forEach(t=>t.setAttribute("aria-selected",t.dataset.tab===view.tab));
}
'''+s[j:]
rep('<div class="strip" id="strip"></div>','<div class="strip" id="strip"></div>\n    <div id="revRow"></div>')

# 3) 주 이동·주차 고르기
i=s.index('function openWeekPicker(){'); j=s.index('document.getElementById("wkTitle").onclick=openWeekPicker;')
s=s[:i]+r'''function gotoW(W,col){
  const N=NDW(); W=Math.max(1,Math.min(N,W));
  const valid=i=>{ const c=cellOf(W,i); return c.w||(c.pre&&hasPre()&&W===1&&i===0); };
  const td=today0(); let pick=-1;
  for(let i=0;i<7;i++) if(dayDiff(cellOf(W,i).dt,td)===0&&valid(i)) pick=i;
  if(pick<0&&col!=null&&valid(col)) pick=col;
  if(pick<0){ for(let i=0;i<7;i++){ const c=cellOf(W,i); if(c.w&&!isRev(c.d)){ pick=i; break; } } }
  if(pick<0){ for(let i=0;i<7;i++) if(valid(i)){ pick=i; break; } }
  const c=cellOf(W,pick); const keepRev=!!view.revW&&MODE==="y365";
  view.pre=!!c.pre; view.revW=keepRev?W:null; if(c.w){ view.w=c.w; view.d=c.d; }
  view.quiz=null; view.wquiz=null; view.open=false; render(); window.scrollTo({top:0});
}
function curCol(){ return view.pre?0:view.revW?6:dateOf(view.w,view.d).getDay(); }
function openWeekPicker(){
  const N=NDW(), cur=dispW(), td=today0(); let h=`<div class="wklist" id="wkList">`;
  for(let W=1;W<=N;W++){
    const L=weekDays(W); let dn=0; L.forEach(([w,d])=>{ if(mem.done[keyOf(w,d)]) dn++; });
    const a=cellOf(W,0).dt, z=cellOf(W,6).dt, now=dayDiff(a,td)>=0&&dayDiff(td,z)>=0;
    h+=`<button class="wkrow${W===cur?" sel":""}" data-pickw="${W}"><span class="n">${W}주차</span><span class="t">${esc(dispTitle(W).replace(/^\d+주차 · /,""))}<small>${fmt(a,{month:"numeric",day:"numeric"})} – ${fmt(z,{month:"numeric",day:"numeric"})}${now?" · 이번 주":""}</small></span><span class="c${L.length&&dn>=L.length?" full":""}">${dn?`${dn}/${L.length}`:""}</span></button>`;
  }
  h+=`</div>`;
  sheet("주차 고르기",h);
  const root=document.getElementById("sheetRoot");
  root.querySelectorAll("[data-pickw]").forEach(b=>b.onclick=()=>{ root.innerHTML=""; view.revW=null; gotoW(+b.dataset.pickw,null); });
  const sel=root.querySelector(".wkrow.sel"); if(sel) sel.scrollIntoView({block:"center"});
}
'''+s[j:]
rep('''document.getElementById("prevW").onclick=()=>{if(view.w>1){view.w--;fixD();view.quiz=null;view.wquiz=null;view.open=false;render();}};''','''document.getElementById("prevW").onclick=()=>gotoW(dispW()-1,curCol());''')
rep('''document.getElementById("nextW").onclick=()=>{if(view.w<NW){view.w++;fixD();view.quiz=null;view.wquiz=null;view.open=false;render();}};''','''document.getElementById("nextW").onclick=()=>gotoW(dispW()+1,curCol());''')
rep('''function go(w,d){view.w=w;view.d=d;''','''function go(w,d){view.pre=false;view.revW=null;view.w=w;view.d=d;''')
open(p,'w').write(s)
print("ok")
