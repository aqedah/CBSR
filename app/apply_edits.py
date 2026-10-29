# 목사님이 앱(관리자 고치기)에서 보낸 고칠 글을 원본 파일에 반영합니다.
# edits/inbox/*.json 하나가 고칠 글 하나: {"at":시각,"plan":"rj"|"y365","day":날번호,"keys":{파일:그날 키},"where":설명,"old":원래 글,"new":바꿀 글}
# 원래 글이 원본 전체에서 한 곳에만 있으면 그곳을 바꿉니다. 여러 곳이면 그날 항목 안에서만 바꿉니다.
# 못 찾으면 바꾸지 않고 기록(edits/log.json)에 '못 찾음'으로 남깁니다. 처리한 inbox 파일은 지웁니다.
import json,os,glob,time,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from edit_targets import FILES
R=os.path.dirname(os.path.abspath(__file__)); os.chdir(R)
IN=sorted(glob.glob('edits/inbox/*.json'))
if not IN: raise SystemExit(0)
FMT={'ux/story_rj.json':dict(indent=1),'ux/story_cards.json':dict(indent=1),'srj/all.json':{},'s365b/all.json':{}}
raw={f:open(f,encoding='utf-8').read() for f in FILES if os.path.exists(f)}
NL={f:r.endswith('\n') for f,r in raw.items()}
dirty=set()
def forms(s):
    # 값 전체가 같은 것만: 따옴표까지 붙여 찾음(긴 글 속 일부와 헷갈리지 않게)
    a=json.dumps(s,ensure_ascii=False); b=json.dumps(s)
    L=[a] if a==b else [a,b]
    if "'" not in s and '"' not in s and '\\' not in s and '\n' not in s: L.append("'"+s+"'")
    return L
def count(s):
    return {f:sum(r.count(x) for x in forms(s)) for f,r in raw.items()}
def repl_text(f,old,new):
    r=raw[f]
    for x,y in zip(forms(old),forms(new)):
        if x in r: raw[f]=r.replace(x,y,1); dirty.add(f); return True
    return False
def walk_replace(o,old,new):
    n=0
    if isinstance(o,dict):
        for k,v in o.items():
            if v==old: o[k]=new; n+=1
            else: n+=walk_replace(v,old,new)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            if v==old: o[i]=new; n+=1
            else: n+=walk_replace(v,old,new)
    return n
def apply(e):
    old,new=e.get('old',''),e.get('new','')
    if not old or old==new: return '바꿀 것 없음'
    c=count(old); tot=sum(c.values())
    if tot==0: return '못 찾음(원본에 없는 글, 자동으로 만든 글일 수 있음)'
    if tot==1:
        f=[f for f,n in c.items() if n][0]; repl_text(f,old,new); return '반영: '+f
    # 여러 곳: 그날 항목 안에서만
    done=[]
    for f,k in (e.get('keys') or {}).items():
        if f not in FMT or f not in raw or not c.get(f): continue
        o=json.loads(raw[f]); ent=o.get(str(k))
        if ent is None: continue
        if ent==old: o[str(k)]=new; n=1
        else: n=walk_replace(ent,old,new)
        if n:
            raw[f]=json.dumps(o,ensure_ascii=False,**FMT[f]); dirty.add(f); done.append(f'{f}({n}곳)')
    if done: return '반영(그날 안에서): '+', '.join(done)
    return '못 찾음(여러 곳에 있어 어디인지 모름: '+', '.join(f for f,n in c.items() if n)+')'
LOG='edits/log.json'
log=json.load(open(LOG,encoding='utf-8')) if os.path.exists(LOG) else []
for p in IN:
    try: e=json.load(open(p,encoding='utf-8'))
    except Exception as x: e={'old':'','new':''}; res='읽지 못함: '+str(x)
    else: res=apply(e)
    log.append({**{k:e.get(k) for k in ('at','plan','day','where','old','new')},'id':os.path.basename(p)[:-5],'res':res,'done':time.strftime('%Y-%m-%d %H:%M')})
    os.remove(p); print(os.path.basename(p),res)
for f in dirty:
    s=raw[f]
    if NL[f] and not s.endswith('\n'): s+='\n'
    open(f,'w',encoding='utf-8').write(s)
json.dump(log[-300:],open(LOG,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
