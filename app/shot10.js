const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const html=fs.readFileSync('이야기통독노트.html','utf8');
const p=await b.newPage({viewport:{width:420,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>');await p.waitForTimeout(3000);
await (await p.$('.kw')).screenshot({path:'k1.png'});
const chips=await p.$$eval('[data-clue]',e=>e.map(x=>x.textContent));console.log('33-3 clues',chips);
await p.click('[data-clue]');await p.waitForTimeout(200);console.log(await p.$eval('.sheet',e=>e.textContent.slice(0,200)));await p.click('#sheetClose');
const names=await p.$$eval('.chip.nm',e=>e.map(x=>x.textContent));console.log('names',names);
await p.click('[data-tab="qt"]');await p.waitForTimeout(200);console.log('gap',await p.$eval('.gapq',e=>e.textContent.slice(0,80)).catch(()=>null));
await p.click('.day:nth-child(7)');await p.waitForTimeout(300);await p.click('[data-tab="read"]');await p.waitForTimeout(300);
const arc=await p.$('.arc');if(arc)await arc.screenshot({path:'arc.png'});
// go to week 35 day1 for echo/scene
await p.click('#nextW');await p.click('#nextW');await p.click('.day:nth-child(1)');await p.waitForTimeout(600);
console.log('35-1',await p.$$eval('[data-clue]',e=>e.map(x=>x.textContent)));
const sc=await p.$('.cl-scene'); if(sc){await sc.click();await p.waitForTimeout(200);await (await p.$('.sheet')).screenshot({path:'scene.png'});
 await p.click('.sheet [data-jump]');await p.waitForTimeout(500);console.log('jumped to',await p.$eval('#whereLine',e=>e.textContent));}
console.log(errs);await b.close();})();
