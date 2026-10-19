s=open('template2.html').read()
def rep(a,b,cnt=1):
    global s
    assert a in s, a[:80]; s=s.replace(a,b,cnt)
css_new=open('css3.txt').read()
i=s.index('/* map */'); j=s.index('/* bible */')
s=s[:i]+css_new+'\n'+s[j:]
rep('<script>\n/*DATA*/','<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>\n<script>\n/*DATA*/')
rep('''<button class="tab" role="tab" data-tab="read" aria-selected="true">오늘 통독</button>''','''<button class="tab" role="tab" data-tab="read" aria-selected="true">오늘 통독</button>
      <button class="tab" role="tab" data-tab="qt" aria-selected="false">QT</button>''')
i=s.index('/* 지도 */'); j=s.index('/* 머리 */')
s=s[:i]+open('mapcode.js').read()+'\n'+s[j:]
i=s.index('/* 오늘 통독 */'); j=s.index('/* 퀴즈 카드')
s=s[:i]+open('readcode.js').read()+'\n'+s[j:]
rep('let mem={start:DEFAULT_START,q:{},wq:{},size:17};','let mem={start:DEFAULT_START,q:{},wq:{},done:{},qt:{},size:17};')
rep('try{const s=localStorage.getItem(KEY);if(s)mem=Object.assign(mem,JSON.parse(s));}catch(e){}','try{const s=localStorage.getItem(KEY);if(s)mem=Object.assign(mem,JSON.parse(s));}catch(e){}\nmem.done ||= {}; mem.qt ||= {};')
rep('store[qz.key]=rec; save();','store[qz.key]=rec; if(mode==="day"&&!mem.done[qz.key]){mem.done[qz.key]=new Date().toISOString().slice(0,10); view.justDone=true;} save();')
rep('''let h=`<section class="sec"><span class="label">나의 기록</span><h2>45주 통독 여정</h2>''','''let h=`<section class="sec"><span class="label">나의 기록</span><h2>45주 통독 여정</h2>${progressCard()}''')
rep('<b>${days}</b><span>퀴즈 푼 날 / 270</span>','<b>${Object.keys(mem.done).length}</b><span>통독 마친 날 / 270</span>')
rep('<b>${streak}</b><span>연속으로 푼 날</span>','<b>${Object.values(mem.qt).filter(x=>x.done).length}</b><span>QT 마친 날</span>')
rep('m.innerHTML=view.tab==="read"?renderRead():view.tab==="record"?renderRecord():renderGuide();\n  bind();',
    'm.innerHTML=view.tab==="read"?renderRead():view.tab==="qt"?renderQT():view.tab==="record"?renderRecord():renderGuide();\n  bind();\n  if(view.tab==="read"&&view.d<6&&BIBLE) initMap(dayA(view.w,view.d)); else destroyMap();')
rep('''  const tq=document.getElementById("toQuiz"); if(tq) tq.onclick=()=>document.getElementById("quizSec").scrollIntoView({block:"start"});''','''  m.querySelectorAll("[data-close]").forEach(b=>b.onclick=()=>{view.open=false;render();document.getElementById("textSec")?.scrollIntoView({block:"start"});});
  const dn=document.getElementById("doneBtn"); if(dn) dn.onclick=()=>{const k=keyOf(view.w,view.d); if(mem.done[k]) delete mem.done[k]; else {mem.done[k]=new Date().toISOString().slice(0,10); view.justDone=true;} save(); render(); document.getElementById("doneSec")?.scrollIntoView({block:"center"});};
  const tqt=document.getElementById("toQT"); if(tqt) tqt.onclick=()=>{view.tab="qt";render();window.scrollTo({top:0});};
  bindQT(m);''')
rep('''  const ct=document.getElementById("closeText"); if(ct) ct.onclick=()=>{view.open=false;render();};''','')
i=s.index('<ol><li><b>요약</b>'); j=s.index('</ol></section>',i)
s=s[:i]+'''<ol><li><b>오늘 통독</b> 탭: 본문을 펼쳐 읽고, 요약·단어 설명·지도로 이해를 돕고, 퀴즈로 확인합니다. 퀴즈를 끝까지 풀거나 '오늘 통독 완료'를 누르면 진행률이 올라갑니다.</li>
  <li><b>QT</b> 탭: 이야기로 읽기, 본문에 나오는 하나님의 성품, 묵상, 기도 순서로 말씀을 깊이 붙잡습니다. 적은 내용은 이 기기에 저장됩니다.</li>
  <li><b>지도</b>는 두 손가락으로 벌리거나 +/− 버튼으로 확대·축소하고, 끌어서 옮길 수 있습니다. '위성'은 웹에 따로 올린 버전에서 보입니다.</li>
  <li><b>주일</b>에는 한 주 점수를 보고 주간 도전 문제를 풉니다.</li>'''+s[j:]
rep('''<section class="sec"><span class="label">시험판 안내</span><p class="lead">33주차(마태복음 19장–마가복음 16장)에는 직접 만든 '생각해 보기' 문제가 함께 나옵니다.''','''<section class="sec"><span class="label">시험판 안내</span><p class="lead">33주차(마태복음 19장–마가복음 16장)에는 직접 만든 '생각해 보기' 문제와 QT 질문이 함께 나옵니다.''')
# when switching tabs/day, reset open
open('template3.html','w').write(s)
print('ok')
s=open('template3.html').read()
rep('<div id="resetBox">','<span class="label" style="margin-top:10px">이미 읽어 오신 분</span><p class="lead">이 프로그램을 중간부터 쓰기 시작했다면, 오늘 이전 날을 모두 읽은 것으로 표시해 진행률을 맞출 수 있습니다.</p><div class="row"><button class="btn ghost small" id="markPast">오늘 이전 날 모두 완료로 표시</button></div><div id="resetBox">')
rep('    document.getElementById("resetAsk").onclick=()=>{','''    document.getElementById("markPast").onclick=()=>{ for(let w=1;w<=here.w;w++) for(let d=0;d<6;d++){ if(w===here.w&&d>=here.d) break; const k=keyOf(w,d); if(!mem.done[k]) mem.done[k]="past"; } save(); view.tab="record"; render(); window.scrollTo({top:0}); };
    document.getElementById("resetAsk").onclick=()=>{''')
rep('mem.q={};mem.wq={};save();render();','mem.q={};mem.wq={};mem.done={};mem.qt={};save();render();')
rep('<span>모든 퀴즈 기록을 지울까요? 되돌릴 수 없습니다.</span>','<span>퀴즈, 진행률, QT 기록을 모두 지울까요? 되돌릴 수 없습니다.</span>')
rep('.sheet-bg{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:flex-end;justify-content:center;z-index:20}','.sheet-bg{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:flex-end;justify-content:center;z-index:10000}')
rep('  bindQT(m);','  const pm=document.getElementById("pmini"); if(pm){const go2=()=>{view.tab="record";render();window.scrollTo({top:0});}; pm.onclick=go2; pm.onkeydown=e=>{if(e.key==="Enter")go2();};}\n  bindQT(m);')
open('template3.html','w').write(s)
print('ok2')
s=open('template3.html').read()
rep('b.onclick=()=>{view.d=d;view.tab="read";view.open=false;view.quiz=null;render();};','b.onclick=()=>{view.d=d;if(view.tab!=="qt")view.tab="read";view.open=false;view.quiz=null;view.wquiz=null;render();window.scrollTo({top:0});};')
rep('document.getElementById("todayBtn").onclick=()=>go(here.w,here.d);','document.getElementById("todayBtn").onclick=()=>{const t=view.tab==="qt"?"qt":"read"; go(here.w,here.d); if(t==="qt"){view.tab="qt";render();}};')
open('template3.html','w').write(s)
print('ok3')
s=open('template3.html').read()
rep('b.onclick=()=>{view.d=d;if(view.tab!=="qt")view.tab="read";','b.onclick=()=>{view.d=d;')
rep('document.getElementById("todayBtn").onclick=()=>{const t=view.tab==="qt"?"qt":"read"; go(here.w,here.d); if(t==="qt"){view.tab="qt";render();}};','document.getElementById("todayBtn").onclick=()=>{const t=view.tab; go(here.w,here.d); if(t!=="read"){view.tab=t;render();}};')
open('template3.html','w').write(s)
s=open('template3.html').read()
rep('  bindQT(m);','  m.querySelectorAll("[data-lw]").forEach(b=>b.onclick=()=>showLW(b.dataset.lw));\n  m.querySelectorAll("[data-em]").forEach(b=>b.onclick=()=>showEM(b.dataset.em));\n  bindQT(m);')
rep("'위성'은 웹에 따로 올린 버전에서 보입니다.","오늘 이야기에 이동이 있으면 점선과 화살표로 경로를 보여 줍니다.")
open('template3.html','w').write(s)
s=open('template3.html').read()
rep('  bindQT(m);','  m.querySelectorAll("[data-inc]").forEach(b=>b.onclick=()=>showINC(+b.dataset.inc));\n  bindQT(m);')
open('template3.html','w').write(s)
s=open('template3.html').read()
rep('  bindQT(m);','  m.querySelectorAll("[data-clue]").forEach(b=>b.onclick=()=>showClue(+b.dataset.clue));\n  bindQT(m);')
rep('  h+=`<section class="sec"><span class="label">이번 주 이야기 다시 보기</span>','  h+=renderArcs(w);\n  h+=`<section class="sec"><span class="label">이번 주 이야기 다시 보기</span>')
rep('''  document.getElementById("sheetClose").focus();''','''  root.querySelectorAll("[data-jump]").forEach(b=>b.onclick=()=>{const [w,d]=b.dataset.jump.split("-").map(Number); close(); go(w,d);});
  document.getElementById("sheetClose").focus();''')
rep('''out+=esc(text.slice(last,m.index))+`<span class="g" tabindex="0"''','''out+=esc(text.slice(last,m.index))+`<span class="g${NAME_SET.has(it.t)?" nm":""}" tabindex="0"''')
rep('''function showGloss(t){const it=GI.by.get(t); if(it) sheet(it.t,`<p>${esc(it.d)}</p>`);}''','''function showGloss(t){const it=GI.by.get(t); if(it) sheet(NAME_SET.has(it.t)?it.t+" · 이름의 뜻":it.t,`<p>${esc(it.d)}</p>`);}''')
open('template3.html','w').write(s)
s=open('template3.html').read()
rep('function save(){try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){}}','function save(){try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){} if(window.SYNC&&SYNC.loggedIn()) SYNC.push(mem);}')
rep('if(mode==="day"&&!mem.done[qz.key]){mem.done[qz.key]=new Date().toISOString().slice(0,10); view.justDone=true;}','if(mode==="day"&&!mem.done[qz.key]){mem.done[qz.key]=new Date().toISOString().slice(0,10); view.justDone=true; if(window.SYNC&&SYNC.available) SYNC.markDone(qz.key,todayStr());}')
rep('else {mem.done[k]=new Date().toISOString().slice(0,10); view.justDone=true;}','else {mem.done[k]=new Date().toISOString().slice(0,10); view.justDone=true; if(window.SYNC&&SYNC.available) SYNC.markDone(k,todayStr());}')
rep('let h=`<section class="sec"><span class="label">나의 기록</span><h2>45주 통독 여정</h2>${progressCard()}','let h=renderAccount()+`<section class="sec"><span class="label">나의 기록</span><h2>45주 통독 여정</h2>${progressCard()}')
rep('  bindQT(m);','  bindAccount(m); if(view.tab==="read") churchCounts();\n  bindQT(m);')
rep('applySize(); render(); loadBible();','''applySize(); render(); loadBible();
if(window.SYNC&&SYNC.loggedIn()) SYNC.pull().then(remote=>{ if(remote){ mem=mergeMem(mem,remote); try{localStorage.setItem(KEY,JSON.stringify(mem));}catch(e){} Object.assign(here,posOfToday()); render(); } }).catch(()=>{});
if(window.SYNC) SYNC.onChange(()=>{ if(view.tab==="record"){ const a=document.activeElement; if(!(a&&a.tagName==="INPUT")) render(); } });''')
open('template3.html','w').write(s)
print('ok8')
