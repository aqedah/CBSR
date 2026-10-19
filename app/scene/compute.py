import json
R='/home/claude/rj/'
T=json.load(open(R+'traits/all.json')); P=json.load(open(R+'para/all.json'))
plan=json.load(open(R+'plan.json')); P365=json.load(open(R+'plan365.json'))
def days():
    for w,wk in enumerate(plan['plan'],1):
        for d,dd in enumerate(wk): yield 'rj',f"{w}-{d}",dd['ch'],dd['label']
    for i,dd in enumerate(P365): yield 'y365',f"{i//7+1}-{i%7}",dd['ch'],dd['label']
EYE={}
for k,v in json.load(open(R+'srj/all.json')).items():
    w,d=map(int,k.split('-')); EYE[('rj',f"{w}-{d-1}")]=v['e']
A=json.load(open(R+'s365b/all.json'))
for i,dd in enumerate(P365):
    v=A.get(str(dd['n']))
    if v: EYE[('y365',f"{i//7+1}-{i%7}")]=v['e']
def scene(e,chs):
    out=[]
    for l in e['look']:
        b,c,v=l['r']
        if [b,c] not in chs: continue
        st=P.get(f"{b}-{c}",[1]); s=max([x for x in st if x<=v] or [1]); nx=[x for x in st if x>v]; t=nx[0]-1 if nx else 999
        m=[r for r in out if r[0]==b and r[1]==c and not(t<r[2]-1 or s>r[3]+1)]
        if m: m[0][2]=min(m[0][2],s); m[0][3]=max(m[0][3],t)
        else: out.append([b,c,s,t])
    return out
need=[]; stat={'rj':[0,0],'y365':[0,0]}
for m,k,chs,lab in days():
    e=EYE.get((m,k))
    if not e: continue
    R_=scene(e,chs)
    if not R_: continue
    tr=[];seen=set()
    for b,c in chs:
        for x in T.get(f"{b}-{c}",[]):
            if x['n'] in seen: continue
            seen.add(x['n']); tr.append((b,c,x['v'],x['n']))
    inside=[t for t in tr if any(r[0]==t[0] and r[1]==t[1] and r[2]<=t[2]<=r[3] for r in R_)]
    stat[m][0]+=1
    if inside or not tr: continue
    stat[m][1]+=1
    need.append({'m':m,'k':k,'label':lab,'q':e['q'],'scene':R_,'look':e['look'],'trait':{'b':tr[0][0],'c':tr[0][1],'v':tr[0][2],'n':tr[0][3]}})
json.dump(need,open(R+'scene/need.json','w'),ensure_ascii=False,indent=0)
print(stat,len(need))
