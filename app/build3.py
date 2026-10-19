import json,base64
t=open('template3.html').read()
plan=json.load(open('plan.json'))
t=t.replace('/*LEAFLETCSS*/',open('npm/node_modules/leaflet/dist/leaflet.css').read())
data="\n".join(open(f).read() for f in ['engine.js','glossary.js','summaries.js','weeks.js','curated.js','qt_base.js','qt_extra.js','routes.js','incl.js','clues.js'])
data=data.replace('if(typeof module!=="undefined") module.exports={buildEntityIndex,buildGlossIndex,inScope,analyzeDay,makeQuiz,rng};','')
tj=json.load(open('terrain.json'))
terr={k:{"bounds":v["bounds"],"url":"data:image/jpeg;base64,"+base64.b64encode(open(f'terrain_{k}.jpg','rb').read()).decode()} for k,v in tj.items()}
data+="\nconst NAME_SET=new Set(NAME_MEAN.map(x=>x[0])); for(const n of NAME_MEAN){ if(!GLOSSARY.some(g=>g[0]===n[0])) GLOSSARY.push(n); }\nconst LEITWORT="+open('leitwort.json').read()+";\nconst EMPH="+open('emph.json').read()+";\nconst GAZ="+open('gaz.json').read()+";\nconst PLAN="+json.dumps(plan,ensure_ascii=False,separators=(',',':'))+";\nconst TERRAIN="+json.dumps(terr)+";\nconst BIBLE_B64=\""+open('bible.b64').read()+"\";\n"
out=t.replace('/*DATA*/',data)
open('이야기통독노트.html','w').write(out)
print(len(out.encode())/1e6)
