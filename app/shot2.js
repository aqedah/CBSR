const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 const html=require('fs').readFileSync('이야기통독노트.html','utf8');
 const page='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>';
 const p=await b.newPage({viewport:{width:400,height:900},colorScheme:'light'});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
 await p.setContent(page); await p.waitForTimeout(3000);
 await p.screenshot({path:'m1.png',fullPage:true});
 // start quiz
 await p.click('[data-qstart="day"]'); await p.waitForTimeout(300);
 for(let k=0;k<6;k++){
   const opts=await p.$$('[data-ans]:not([disabled])'); await opts[opts.length-1].click(); await p.waitForTimeout(150);
   if(k===0) await p.screenshot({path:'q1.png'});
   let nx=await p.$('[data-next]'); 
   while(!nx){ const o=await p.$$('[data-ans]:not([disabled])'); await o[0].click(); await p.waitForTimeout(100); nx=await p.$('[data-next]'); }
   await nx.click(); await p.waitForTimeout(150);
 }
 await p.screenshot({path:'q_end.png'});
 await p.click('.day:nth-child(7)'); await p.waitForTimeout(400); await p.screenshot({path:'sun2.png',fullPage:true});
 const pd=await b.newPage({viewport:{width:1000,height:900},colorScheme:'dark'});
 pd.on('pageerror',e=>errs.push(e.message));
 await pd.setContent(page); await pd.waitForTimeout(3000);
 // go to week 37 day1 via evaluate: click next 4 times
 for(let i=0;i<4;i++) await pd.click('#nextW');
 await pd.click('.day:nth-child(1)'); await pd.waitForTimeout(500);
 await pd.screenshot({path:'d37.png',fullPage:true});
 console.log('errors',errs, await p.evaluate(()=>document.body.scrollWidth));
 await b.close();
})();
