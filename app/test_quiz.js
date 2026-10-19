const fs=require('fs');const E=require('./engine.js');
const plan=JSON.parse(fs.readFileSync('plan.json'));
const bible=JSON.parse(require('zlib').gunzipSync(Buffer.from(fs.readFileSync('bible.b64','utf8'),'base64')));
const gz=JSON.parse(fs.readFileSync('gaz.json'));
const EI=E.buildEntityIndex(gz.places,gz.people);
const bookCache={};
function bookA(b){ if(!bookCache[b]) bookCache[b]=E.analyzeDay(bible[b-1].map((_,i)=>[b,i+1]),bible,EI); return bookCache[b];}
const ctx={abbr:plan.abbr,bookPeople:b=>[...bookA(b).people.values()].sort((x,y)=>y.n-x.n).slice(0,30).map(x=>x.name),bookPlaces:b=>[...bookA(b).places.values()].sort((x,y)=>y.n-x.n).slice(0,30).map(x=>x.name)};
let short=0, kinds={};
const show=process.argv[2];
for(let w=0;w<45;w++)for(let d=0;d<6;d++){
  const day=E.analyzeDay(plan.plan[w][d].ch,bible,EI);
  for(let s=1;s<=3;s++){
    const q=E.makeQuiz(day,ctx,w*1000+d*10+s);
    if(q.length<6){short++; if(s===1) console.log('short',w+1,d+1,plan.plan[w][d].spec,q.length,q.map(x=>x.kind).join(','));}
    q.forEach(x=>kinds[x.kind]=(kinds[x.kind]||0)+1);
    if(show && show===`${w+1}-${d+1}` && s===1) q.forEach(x=>console.log(JSON.stringify({k:x.kind,q:x.quote,o:x.o,a:x.a,ref:[x.vs.c,x.vs.v]},null,0)));
  }
}
console.log('short',short,kinds);
