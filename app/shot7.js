const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const html=fs.readFileSync('이야기통독노트.html','utf8');
const p=await b.newPage({viewport:{width:400,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/leaflet.js',r=>r.fulfill({body:'',contentType:'application/javascript'}));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>');await p.waitForTimeout(3000);
await p.click('[data-tab="qt"]');
for(const d of [1,2,3,4,5,6]){await p.click(`.day:nth-child(${d})`);await p.waitForTimeout(250);
 const tr=await p.$$eval('.trait',e=>e.map(x=>x.querySelector('b').textContent+' / '+x.querySelector('q').textContent.slice(0,40)));
 console.log('DAY',d,tr);
 for(let i=0;i<3;i++){const kv=await p.$eval('.keyv',e=>e.textContent.slice(14,60));const q=await p.$$eval('.qcard',e=>e.find(x=>x.textContent.includes('이 구절과'))?.querySelector('p').textContent);console.log('  ',kv,'→',q.slice(0,60));await p.click('#qtNextV');await p.waitForTimeout(150);}
 const a=await p.$eval('.prayer',e=>e.textContent);console.log('  P:',a.slice(-30),await p.$('#qtNextP'),(await p.content()).includes('전체 적용'));}
console.log(errs);await b.close();})();
