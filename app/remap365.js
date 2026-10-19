const fs=require('fs');
const ld=(f,n)=>{const s=fs.readFileSync(f,'utf8');return new Function(s+';return '+n)();};
const INCL=ld('incl.js','INCL'), ROUTES=ld('routes.js','ROUTES');
const RJ=JSON.parse(fs.readFileSync('plan.json')).plan, P=JSON.parse(fs.readFileSync('plan365.json'));
const key365=i=>`${Math.floor(i/7)+1}-${i%7+1}`;
const dayOf=(b,c)=>P.findIndex(d=>d.ch.some(x=>x[0]===b&&x[1]===c));
const I2={};let lost=0;
for(const k in INCL) for(const x of INCL[k]){const a=dayOf(x.a[0],x.a[1]), z=dayOf(x.z[0],x.z[1]); if(a===z&&a>=0)(I2[key365(a)] ||= []).push(x); else lost++;}
const R2={};
for(const k in ROUTES){ const [w,d]=k.split('-').map(Number); const day=RJ[w-1][d-1];
  for(const r of ROUTES[k]){
    let chs=[]; const m=r.n.match(/\((\d+)(?:[–-](\d+))?(?:장|편)/);
    if(m){ const c1=+m[1], c2=+(m[2]||m[1]); chs=day.ch.filter(([b,c])=>c>=c1&&c<=c2); }
    if(!chs.length) chs=day.ch;
    const cnt={}; for(const [b,c] of chs){const i=dayOf(b,c); cnt[i]=(cnt[i]||0)+1;}
    const best=Object.entries(cnt).sort((a,b)=>b[1]-a[1]||b[0]-a[0])[0][0];
    (R2[key365(+best)] ||= []).push(r);
  }}
fs.writeFileSync('incl365.json',JSON.stringify(I2)); fs.writeFileSync('routes365.json',JSON.stringify(R2));
console.log('incl',Object.values(INCL).flat().length,'->',Object.values(I2).flat().length,'lost',lost,'routes',Object.values(ROUTES).flat().length,'->',Object.values(R2).flat().length);
for(const k of Object.keys(R2).slice(0,6)) console.log(k,P[(+k.split('-')[0]-1)*7+(+k.split('-')[1]-1)].label,R2[k].map(r=>r.n));
