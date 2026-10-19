const {chromium}=require('playwright');const fs=require('fs');
const FB='/home/claude/fbemu/node_modules/firebase/';
(async()=>{const b=await chromium.launch();const errs=[];
async function dev(){const ctx=await b.newContext({viewport:{width:400,height:850}});const p=await ctx.newPage();
 p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
 await p.route('**/leaflet.js',r=>r.fulfill({body:fs.readFileSync('npm/node_modules/leaflet/dist/leaflet.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/firebasejs/10.14.1/*',r=>{const f=r.request().url().split('/').pop();r.fulfill({body:fs.readFileSync(FB+f,'utf8'),contentType:'application/javascript'});});
 await p.route('**/config.js*',r=>r.fulfill({contentType:'application/javascript',body:'window.CBSR_FIREBASE_CONFIG={apiKey:"demo",authDomain:"demo-cbsr.firebaseapp.com",projectId:"demo-cbsr",appId:"1:1:web:1",emulator:true};'}));
 await p.goto('http://localhost:8765/');await p.waitForTimeout(3500);return p;}
const A=await dev();
await A.click('[data-tab="record"]');await A.waitForTimeout(300);
await A.fill('#acctName','홍길동');await A.fill('#acctPin','4821');await A.click('#acctIn');await A.waitForTimeout(2500);
console.log('A msg:',await A.$eval('.acct',e=>e.textContent.slice(0,60)));
await A.click('[data-tab="read"]');await A.waitForTimeout(800);await A.click('#doneBtn');await A.waitForTimeout(1500);
console.log('A done card:',await A.$eval('.done-card',e=>e.textContent.slice(0,120)));
await A.click('[data-tab="qt"]');await A.waitForTimeout(400);await A.fill('#qt-med','오늘은 베드로처럼 다시 일어나겠습니다');await A.waitForTimeout(3500);
const B=await dev();
console.log('B before:',await B.$eval('.pmini b',e=>e.textContent));
await B.click('[data-tab="record"]');await B.waitForTimeout(300);
await B.fill('#acctName','홍길동');await B.fill('#acctPin','4821');await B.click('#acctIn');await B.waitForTimeout(2500);
console.log('B msg:',await B.$eval('#acctMsg',e=>e.textContent).catch(()=>'(rerendered)'), await B.$eval('.acct',e=>e.textContent.slice(0,40)));
await B.waitForTimeout(1500);console.log('B church:',await B.$eval('#churchBox',e=>e.textContent));
await B.click('[data-tab="read"]');await B.waitForTimeout(500);console.log('B after:',await B.$eval('.pmini b',e=>e.textContent));
await B.click('[data-tab="qt"]');await B.waitForTimeout(400);console.log('B qt:',await B.$eval('#qt-med',e=>e.value));
// rule tests from page
const rt=await B.evaluate(async()=>{const db=firebase.firestore();const out={};
 try{await db.collection('readers').get();out.list='ALLOWED';}catch(e){out.list='denied';}
 try{await db.doc('days/33-3').set({done:99});out.bump='ALLOWED';}catch(e){out.bump='denied';}
 try{await db.doc('readers/abc').set({name:'x',data:'{}'});out.shortkey='ALLOWED';}catch(e){out.shortkey='denied';}
 return out;});
console.log('rules',rt);
console.log('errs',errs.filter(e=>!/permission|PERMISSION/.test(e)).slice(0,5));await b.close();})();
