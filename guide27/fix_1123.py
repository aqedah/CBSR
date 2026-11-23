# 11-23 목사님: ① '줄'(죽음의 줄 등) 표현이 어색함 ② '되풀이' → '반복' ③ 성경 읽기 표시가 5장 → 3장처럼 거꾸로 놓여 헷갈림.
# 하루 원고 칸만 고칩니다. 책머리(f0)와 front.py의 목사님 문장(↗ 점층 설명 등)은 건드리지 않습니다.
# 표시 차례(③)는 trial_review7.py(체험판)와 이 파일(2027 1–21일)에서 본문 차례대로 놓습니다. 다시 돌려도 결과가 같습니다.
import json,os,re,glob
R=os.path.dirname(os.path.abspath(__file__)); SS=os.path.join(R,'..','app','site_src')
D2=[('죽음이 되풀이되는 줄 가운데서도','죽음이 반복되는 가운데서도'),('죽음이 되풀이되는 줄 가운데','죽음이 반복되는 가운데'),
    ('죽음의 줄 가운데서도','죽음이 이어지는 가운데서도'),('죽음의 줄 가운데서','죽음이 이어지는 가운데서'),
    ('그런데 그 줄 가운데 에녹은','그런데 그 가운데 에녹은'),('에녹 — 죽었더라가 끊기는 한 줄',"에녹에게서 끊기는 '죽었더라'"),
    ('그 줄이 에녹에게서는','그 반복이 에녹에게서는')]
PT=[('되풀이는','반복은'),('되풀이가','반복이'),('되풀이와','반복과'),('되풀이로','반복으로'),('되풀이를','반복을'),('되풀이','반복')]
def fix(s):
    for a,b in D2+PT: s=s.replace(a,b)
    return s
def walk(x):
    if isinstance(x,str): return fix(x)
    if isinstance(x,list): return [walk(v) for v in x]
    if isinstance(x,dict): return {k:walk(v) for k,v in x.items()}
    return x
REF=re.compile(r'(\d+):(\d+)')
def key(t):
    m=REF.search(re.sub(r'<[^>]+>','',t)); return (int(m.group(1)),int(m.group(2))) if m else None
def order(marks,looks):
    """표시는 본문 차례대로. 눈여겨볼 것은 표시를 확인하는 것(ck) 먼저, 그 안에서 본문 차례대로, 나머지도 본문 차례대로."""
    out=[marks,looks]
    if marks and all(key(m['text']) for m in marks): out[0]=sorted(marks,key=lambda m:key(m['text']))
    if looks and all(key(l['text']) for l in looks):
        out[1]=sorted([l for l in looks if l.get('ck')],key=lambda l:key(l['text']))+sorted([l for l in looks if not l.get('ck')],key=lambda l:key(l['text']))
    return out
if __name__=='__main__':
    n=0
    # 원고 원본(.py): 다시 만들어도 '반복'이 되게
    for f in glob.glob(os.path.join(R,'week*.py'))+glob.glob(os.path.join(R,'trial_w[0-9].py'))+glob.glob(os.path.join(R,'trial_review[0-9].py'))+[os.path.join(R,'book1_review_q.py')]:
        s=open(f).read(); t=fix(s)
        if t!=s: open(f,'w').write(t); n+=1
    # 주 원고(.json)
    for f in glob.glob(os.path.join(R,'week*.json'))+glob.glob(os.path.join(R,'trial_w[0-9].json'))+[os.path.join(R,'book1.json')]:
        L=json.load(open(f)); L2=walk(L)
        if f.endswith('book1.json'):
            for D in L2:
                if 'marks' in D and 'looks' in D: D['marks'],D['looks']=order(D['marks'],D['looks'])
        if L2!=L: json.dump(L2,open(f,'w'),ensure_ascii=False,indent=1); n+=1
    # 작업대 원고: 하루 칸만(f0 제외)
    for f in ['guide_qt.json','trial26_qt.json']:
        p=os.path.join(SS,f); J=json.load(open(p))
        for k in list(J['qt']):
            if k=='f0': continue
            J['qt'][k]=walk(J['qt'][k])
            v=J['qt'][k].get('v27')
            if f=='guide_qt.json' and v and k.isdigit() and int(k)<=21 and 'marks' in v and 'looks' in v: v['marks'],v['looks']=order(v['marks'],v['looks'])
        json.dump(J,open(p,'w'),ensure_ascii=False,indent=1); n+=1
    print('고친 파일',n)
