# 합친 원고(data/*.md) → 앱이 읽는 shelf_66.json, shelf.src.js → shelf.js
import re,glob,json,sys,os
SITE='/home/claude/cbsr/app/site_src'
K={'한줄':'line','구절':'verse','저자':'author','수신자':'audience','시기':'time','갈래':'genre','배경':'bg','각주':'footnote','목적':'purpose','흐름':'flow','구조':'parts','하나님':'god','주제':'themes','연결':'connection','읽기':'reading'}
M100=set(x['r'] for x in json.load(open(SITE+'/mem100.json',encoding='utf-8'))['list'])
def in100(v):
    m=re.match(r'^(\S+) (\d+):(\d+)(?:[–-](\d+))?$',v or '')
    return bool(m) and any('%s %s:%d'%(m.group(1),m.group(2),i) in M100 for i in range(int(m.group(3)),int(m.group(4) or m.group(3))+1))
books=[];g='';cur=None
for f in sorted(glob.glob('/home/claude/shelf-desk/data/*.md')):
    for l in open(f,encoding='utf-8').read().split('\n'):
        l=l.strip(); m=re.match(r'^# (.+)$',l)
        if m: g=m.group(1).strip(); continue
        m=re.match(r'^## (.+?) \| (\w+) \| (\d+)$',l)
        if m: cur=dict(id=m.group(2),name=m.group(1),group=g,chapters=int(m.group(3)),line='',verse='',author='',audience='',time='',genre='',background=[],footnote='',purpose='',flow='',structure=[],god='',themes=[],connection='',reading=''); books.append(cur); continue
        m=re.match(r'^- ([^:]+): (.*)$',l)
        if not (m and cur) or m.group(1) not in K: continue
        k,v=K[m.group(1)],m.group(2)
        if k=='bg':
            r=re.match(r'^(.*?)\s*\(([^()]*\d[^()]*)\)\s*$',v); cur['background'].append({'text':r.group(1),'ref':r.group(2)} if r else {'text':v,'ref':''})
        elif k=='parts': p=v.split('|'); cur['structure'].append({'range':p[0].strip(),'title':'|'.join(p[1:]).strip()})
        elif k=='themes': cur['themes']=[x.strip() for x in v.split('·') if x.strip()]
        else: cur[k]=v
for b in books: b['mem100']=in100(b['verse'])
assert len(books)==66
out={'name':'CBSR 성경책장 개론','version':1,'books':books}
json.dump(out,open(SITE+'/shelf_66.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
art=open('/home/claude/shelf-desk/shelf_art.json',encoding='utf-8').read()
js=open('/home/claude/shelf-desk/shelf.src.js',encoding='utf-8').read(); assert js.count('__ART__')==1
open(SITE+'/shelf.js','w',encoding='utf-8').write(js.replace('__ART__',art))
print('shelf_66.json',os.path.getsize(SITE+'/shelf_66.json'),'| shelf.js',os.path.getsize(SITE+'/shelf.js'),'| groups',sorted(set(b['group'] for b in books)))
