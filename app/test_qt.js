const fs=require('fs');const E=require('./engine.js');
global.DETAIL={};eval(fs.readFileSync('qt_base.js','utf8').replace(/const (\w+)/g,'global.$1'));
eval(fs.readFileSync('qt_extra.js','utf8').replace(/^const (DIVINE|ATTRS)/gm,'global.$1').replace('function godTraits','global.godTraits=function').replace('function near','global.near=function'));
const plan=JSON.parse(fs.readFileSync('plan.json'));
const bible=JSON.parse(require('zlib').gunzipSync(Buffer.from(fs.readFileSync('bible.b64','utf8'),'base64')));
const gz=JSON.parse(fs.readFileSync('gaz.json'));const EI=E.buildEntityIndex(gz.places,gz.people);
let none=0;
for(let w=0;w<45;w++)for(let d=0;d<6;d++){const A=E.analyzeDay(plan.plan[w][d].ch,bible,EI);const t=godTraits(A);if(!t.length)none++;
 if(['33-2','4-3','21-1','17-1','40-6'].includes(`${w+1}-${d+1}`)) console.log(w+1,d+1,t.map(x=>x.at.n+'('+x.vs.length+') '+x.verse.c+':'+x.verse.v+' '+x.verse.t.slice(0,50)).join('\n   '));}
console.log('none',none, Object.keys(DETAIL).length);
