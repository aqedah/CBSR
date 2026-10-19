const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const b=await chromium.launch();
 const html=fs.readFileSync('이야기통독노트.html','utf8');
 const page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>';
 const errs=[];
 async function mk(w,scheme){const p=await b.newPage({viewport:{width:w,height:900},colorScheme:scheme});
  await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
  p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
  await p.setContent(page); await p.waitForTimeout(3500); return p;}
 const p=await mk(400,'light');
 await p.screenshot({path:'r1.png',fullPage:true});
 await p.click('#openText'); await p.waitForTimeout(400); await p.screenshot({path:'r2.png'});
 await p.click('[data-close]'); await p.waitForTimeout(300);
 await p.click('#doneBtn'); await p.waitForTimeout(500); await p.screenshot({path:'r3.png'});
 await p.click('[data-tab="qt"]'); await p.waitForTimeout(500); await p.screenshot({path:'qt.png',fullPage:true});
 const d=await mk(1000,'dark');
 for(let i=0;i<4;i++) await d.click('#nextW'); await d.click('.day:nth-child(1)'); await d.waitForTimeout(1200);
 const m=await d.$('#lmap'); await m.screenshot({path:'map37.png'});
 await d.click('#mSat'); await d.waitForTimeout(1500); await d.screenshot({path:'sat.png'});
 console.log(errs.slice(0,8), await p.evaluate(()=>document.body.scrollWidth));
 await b.close();
})();
