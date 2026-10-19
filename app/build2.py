import json
t=open('template2.html').read()
plan=json.load(open('plan.json'))
data="\n".join(open(f).read() for f in ['engine.js','glossary.js','summaries.js','weeks.js','curated.js'])
data=data.replace('if(typeof module!=="undefined") module.exports={buildEntityIndex,buildGlossIndex,inScope,analyzeDay,makeQuiz,rng};','')
data+="\nconst GAZ="+open('gaz.json').read()+";\nconst PLAN="+json.dumps(plan,ensure_ascii=False,separators=(',',':'))+";\nconst MAPS="+open('maps.json').read()+";\nconst BIBLE_B64=\""+open('bible.b64').read()+"\";\n"
out=t.replace('/*DATA*/',data)
open('이야기통독노트.html','w').write(out)
print(len(out.encode())/1e6)
