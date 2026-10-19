const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const html=fs.readFileSync('이야기통독노트.html','utf8');
const p=await b.newPage({viewport:{width:420,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>');await p.waitForTimeout(3000);
const kw=await p.$('.kw'); await kw.screenshot({path:'kw.png'});
await p.click('.chip.lw'); await p.waitForTimeout(200); console.log(await p.$eval('.sheet',e=>e.textContent)); await p.click('#sheetClose');
async function mapShot(nav,day,name){ for(const n of nav) await p.click(n); await p.click(`.day:nth-child(${day})`); await p.waitForTimeout(900); const m=await p.$('.mapbox'); await m.screenshot({path:name}); }
await mapShot([],1,'route33.png');
await mapShot(['#nextW','#nextW','#nextW','#nextW'],1,'route37.png');
console.log(errs.slice(0,5));await b.close();})();
