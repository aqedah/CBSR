// 체험판 12월·부록 책(A5) 본문 찍기 — 작업대(trial26.html)의 책 차례 그대로: 앞표지 → 책머리 → 11/29–12/31 → 부록 머리. (11-25)
// 쓰는 법: app/site_src에서 python3 -m http.server 8765를 띄우고, 빈 폴더에서 node trial_dec_body.js → python3 trial_dec_merge.py
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:1000}});
await p.goto('http://localhost:8765/trial26.html');await p.waitForTimeout(3000);
const r=await p.evaluate(()=>{
  cur=PLAN.findIndex(x=>x.no===ED.from); buildViews();
  const parts=[]; let back=''; const bad=[];
  const probe=document.createElement('div'); probe.style.cssText='position:absolute;left:-9999px;top:0'; document.body.appendChild(probe);
  VIEWS.forEach((v,i)=>{
    if(v.t==='d'){ const x=PLAN[v.i], qt=get(x.no)||blank(); probe.innerHTML=pageL(x,qt)+pageR(x,qt); tighten(probe); matchMedia(probe,1); post27(probe,1); parts.push(probe.innerHTML); if(!get(x.no)) bad.push('원고없음 '+x.m+'/'+x.d); return }
    const d=document.createElement('div'); d.innerHTML=v.h; const pgs=[...d.querySelectorAll('.spread > .pg')];
    pgs.forEach(pg=>{ if(pg.classList.contains('back')){ back=pg.outerHTML; return } if(pg.classList.contains('axim')) return; parts.push(pg.outerHTML) });
  });
  probe.remove();
  document.getElementById('printroot').innerHTML=parts.join(''); window.__back=back;
  return {n:document.querySelectorAll('#printroot > .pg').length,bad,ax:ED.ax26.n};
});
console.log(JSON.stringify(r));
await p.emulateMedia({media:'print'}); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(1500);
await p.pdf({path:'body.pdf',format:'A5',printBackground:true,preferCSSPageSize:true});
await p.evaluate(()=>{document.getElementById('printroot').innerHTML=window.__back}); await p.waitForTimeout(500);
await p.pdf({path:'back.pdf',format:'A5',printBackground:true,preferCSSPageSize:true});
await p.evaluate(()=>{document.getElementById('printroot').innerHTML=blankPage(4)});
await p.pdf({path:'blank.pdf',format:'A5',printBackground:true,preferCSSPageSize:true});
await b.close();})();
