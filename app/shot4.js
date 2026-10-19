const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const html=fs.readFileSync('이야기통독노트.html','utf8');
const p=await b.newPage({viewport:{width:400,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>');
await p.waitForTimeout(3500);await p.screenshot({path:'t1.png'});
await (await p.$('#lmap')).scrollIntoViewIfNeeded(); await p.click('.chip.term'); await p.waitForTimeout(300); await p.screenshot({path:'t2.png'});
const top=await p.evaluate(()=>{const r=document.querySelector('.sheet').getBoundingClientRect();const e=document.elementFromPoint(r.left+20,r.top+20);return !!e.closest('.sheet');});
console.log(errs,'sheetOnTop',top);await b.close();})();
