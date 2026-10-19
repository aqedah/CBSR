const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const html=fs.readFileSync('이야기통독노트.html','utf8');
const p=await b.newPage({viewport:{width:400,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>');await p.waitForTimeout(3000);
await p.click('[data-tab="qt"]');await p.waitForTimeout(300);
for(let i=0;i<5;i++){const kv=await p.$eval('.keyv',e=>e.textContent.slice(0,70));const q=await p.$$eval('.qcard',e=>e.find(x=>x.textContent.includes('이 구절과'))?.textContent);const pr=await p.$eval('.prayer',e=>e.textContent);
 console.log('V:',kv,'\nQ:',q,'\nP:',pr.slice(0,90),'\n');await p.click('#qtNextV');await p.waitForTimeout(200);}
await p.click('#qtNextP');await p.waitForTimeout(200);console.log('P2:',(await p.$eval('.prayer',e=>e.textContent)).slice(0,90));
for(const d of [1,2,4]){await p.click(`.day:nth-child(${d})`);await p.waitForTimeout(300);console.log(d,(await p.$eval('.prayer',e=>e.textContent)).slice(0,60));}
await p.screenshot({path:'qt2.png',fullPage:true});
console.log(errs);await b.close();})();
