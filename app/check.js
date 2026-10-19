const fs=require('fs');eval(fs.readFileSync('days.js','utf8')+';global.D=D');
const P=JSON.parse(fs.readFileSync('plan.json','utf8'));
const zlib=require('zlib');const B=JSON.parse(zlib.gunzipSync(Buffer.from(fs.readFileSync('bible.b64','utf8'),'base64')));
const ab=P.abbr;
function parseRef(r,day){let bk=null;const m=r.match(/^(\S+) (.+)$/);if(m&&ab.includes(m[1])){bk=ab.indexOf(m[1])+1;r=m[2];}
 if(!bk)bk=day.ch[0][0];const [a,b]=r.split('-');const [c,v]=a.split(':').map(Number);let c2=c,v2=v;
 if(b){if(b.includes(':')){[c2,v2]=b.split(':').map(Number)}else v2=+b;} return {bk,c,v,c2,v2};}
let bad=0,n=0;
for(const k in D){const [w,d]=k.split('-').map(Number);const day=P.plan[w-1][d-1];
 for(const e of D[k].ev){n++;const R=parseRef(e[0],day);
  const inDay=day.ch.some(([b,c])=>b===R.bk&&c===R.c);
  if(!inDay){console.log('OUT',k,e[0]);bad++;continue;}
  let txt='';for(let c=R.c;c<=R.c2;c++){const vs=B[R.bk-1][c-1];const s=(c===R.c?R.v:1)-3,t=(c===R.c2?R.v2:vs.length)+2;txt+=vs.slice(Math.max(0,s-1),t).join(' ');}
  const T=txt.replace(/\s/g,'');
  for(const q of (e[2].match(/'([^']+)'/g)||[])){const qq=q.slice(1,-1).replace(/\s/g,'');if(!T.includes(qq)){console.log('Q',k,e[0],q);bad++;}}
 }
 for(const q of ((D[k].p+D[k].s).match(/'([^']+)'(\(\d+:\d+)/g)||[])){}
}
console.log('events',n,'problems',bad);
