const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 for(const [name,w,scheme] of [['desk',1100,'light'],['phone',400,'dark']]){
  const p=await b.newPage({viewport:{width:w,height:1400},colorScheme:scheme});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
  const html=require('fs').readFileSync('이야기통독노트.html','utf8');
  await p.setContent('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>');
  await p.waitForTimeout(2500);
  await p.screenshot({path:name+'.png',fullPage:false});
  console.log(name,errs, await p.evaluate(()=>document.body.scrollWidth));
  if(name==='desk'){ // click verse, sunday, map
    await p.click('.v[data-i="2"]'); await p.fill('#f-title','기쁜 소식, 넉넉한 연보');
    await p.waitForTimeout(600);
    await p.click('.day:nth-child(7)'); await p.waitForTimeout(300); await p.screenshot({path:'sun.png'});
    await p.click('[data-tab=map]'); await p.screenshot({path:'map.png'});
    await p.click('.mrow'); await p.waitForTimeout(300); await p.screenshot({path:'back.png',fullPage:true});
    console.log(errs);
  }
 }
 await b.close();
})();
