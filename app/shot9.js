const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const html=fs.readFileSync('이야기통독노트.html','utf8');
const p=await b.newPage({viewport:{width:420,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>');await p.waitForTimeout(3000);
await p.click('.day:nth-child(6)');await p.waitForTimeout(500);
await (await p.$('.kw')).screenshot({path:'kw2.png'});
await p.click('.chip.inc');await p.waitForTimeout(200);await (await p.$('.sheet')).screenshot({path:'inc.png'});
console.log(errs);await b.close();})();
