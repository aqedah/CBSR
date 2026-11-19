const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const qt=JSON.parse(fs.readFileSync('../guide/all_qt.json','utf8')).qt;
  const b = await chromium.launch(); const ctx=await b.newContext({viewport:{width:1500,height:950}});
  await ctx.addInitScript(d=>{localStorage.setItem('cbsr_guide_qt',JSON.stringify(d))}, qt);
  const p = await ctx.newPage(); await p.goto('file:///home/claude/통독가이드북_작업실.html'); await p.waitForTimeout(800);
  const days=process.argv.slice(2).map(Number); const out={};
  for(const n of days){
    const i=await p.evaluate(n=>PLAN.findIndex(x=>x.no===n),n);
    await p.evaluate(i=>gotoDay(i), i); await p.waitForTimeout(500);
    const r=await p.evaluate(()=>{const pg=document.querySelector('#prev .pg');const c2=pg.querySelector('.c2');return c2?{cls:[...c2.querySelectorAll('*')].slice(0,6).map(e=>e.tagName+'.'+e.className).join(' '),html:c2.innerHTML,w:c2.getBoundingClientRect().width,h:c2.getBoundingClientRect().height}:null});
    out[n]=r; console.log(n, r&&r.cls, r&&r.html.length, r&&[r.w,r.h]);
  }
  fs.writeFileSync('maps.json',JSON.stringify(out));
  await b.close();
})();
