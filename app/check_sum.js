const fs=require('fs');
eval(fs.readFileSync('summaries.js','utf8').replace('const SUMMARY','global.SUMMARY'));
const plan=JSON.parse(fs.readFileSync('plan.json')).plan;
const {execSync}=require('child_process');
const bible=JSON.parse(require('zlib').gunzipSync(Buffer.from(fs.readFileSync('bible.b64','utf8'),'base64')));
const gz=fs.readFileSync('gaz.py','utf8');
const places=gz.match(/PLACES = """([\s\S]*?)"""/)[1].split('\n').map(l=>l.split(' ').slice(0,-3).join(' '));
const people=[...new Set(gz.match(/PEOPLE = """([\s\S]*?)"""/)[1].split(/\s+/).filter(Boolean))].filter(x=>x!=='유다');
const names=[...new Set([...places,...people])].sort((a,b)=>b.length-a.length);
const P="(?:께서|에게서|으로부터|에게|에서|으로|까지|부터|이여|이요|이라|이니|이며|이나|이다|이시|사람|족속|자손|지방|광야|이|가|은|는|을|를|의|에|로|과|와|도|만|아|야|여|라|땅|성|산|강|왕|온|들|께|인|요|며|니|나|고)";
const rx=n=>new RegExp('(?<![가-힣])'+n+'(?='+P+'?(?![가-힣]))','g');
let bad=0;
for(let w=0;w<45;w++)for(let d=0;d<6;d++){
  const s=SUMMARY[w][d]; if(!s){console.log('MISSING',w+1,d+1);bad++;continue;}
  const txt=plan[w][d].ch.map(([b,c])=>bible[b-1][c-1].join(' ')).join(' ');
  const norm=t=>t.replace(/[\s,.'"!?·:;]/g,'');
  const nt=norm(txt);
  const miss=[];
  let rest=s;
  for(const n of names){ if(rx(n).test(rest)){ rest=rest.replace(rx(n),'＿'); if(!rx(n).test(txt)) miss.push(n);} }
  const quotes=[...s.matchAll(/"([^"]+)"/g)].map(m=>m[1]).filter(q=>!nt.includes(norm(q)));
  if(miss.length||quotes.length){bad++;console.log(`${w+1}-${d+1}`,plan[w][d].spec,'| 이름:',miss.join(','),'| 인용:',quotes.join(' / '));}
}
console.log('bad',bad);
