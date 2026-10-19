const fs=require('fs');
eval(fs.readFileSync('clues.js','utf8').replace(/^const (\w+)=/gm,'global.$1='));
const plan=JSON.parse(fs.readFileSync('plan.json')).plan;
const B=JSON.parse(require('zlib').gunzipSync(Buffer.from(fs.readFileSync('bible.b64','utf8'),'base64')));
const t=r=>{try{return B[r[0]-1][r[1]-1][r[2]-1]}catch(e){return undefined}};
const dayOf=r=>{for(let w=0;w<45;w++)for(let d=0;d<6;d++)if(plan[w][d].ch.some(([b,c])=>b===r[0]&&c===r[1]))return `${w+1}-${d+1}`;return null;};
let bad=0;
const chk=(r,k,label)=>{const v=t(r);if(v===undefined){console.log('NOVERSE',label,r);bad++;return;} if(k&&!v.includes(k)){console.log('MISS',label,r,'['+k+']',v.slice(0,80));bad++;} if(!dayOf(r)){console.log('NODAY',label,r);bad++;}};
for(const c of CLUE_LIST){ if(c.t==='pair'){chk(c.ra,c.ka,c.t+' '+c.a);chk(c.rb,c.kb,c.t+' '+c.b);} else chk(c.r,c.k,c.t); if(c.o) chk(c.o,c.ok,'echo-o'); }
for(const g of GAP_LIST) chk(g.r,g.k,'gap');
for(const a of ARC_LIST){chk(a.a,a.ka,'arc '+a.n);chk(a.z,a.kz,'arc '+a.n); const da=dayOf(a.a),dz=dayOf(a.z); if(!dz||+dz.split('-')[0]!==a.w) console.log('ARCWEEK',a.n,da,dz,a.w);}
// count per day
const per={};for(const c of CLUE_LIST){const d=dayOf(c.t==='pair'?c.ra:c.r);per[d]=(per[d]||0)+1;}
console.log('bad',bad,'days with clues',Object.keys(per).length);
