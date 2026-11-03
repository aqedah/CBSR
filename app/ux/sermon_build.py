#!/usr/bin/env python3
"""주일 설교 본문(ux/sermons.json) → 앱 자료 SERMON. 주소는 숫자로 풀어 넣음."""
import json, os, re, sys
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
from gb_build import AB
def segs(ref):
    """'행 11:27–12:5; 마 1:1–6' → [[b,c1,v1,c2,v2],…] ('행 11'은 장 전체 → v1=1,v2=999)"""
    out=[]; b=None
    for tok in re.split(r'(?=[;,])', ref.strip()):
        sep=tok[:1]; tok=tok.lstrip(';,').strip()
        if sep==',' and out and re.match(r'^\d+(?:[–-]\d+)?$', tok):  # '11:19–20, 23' → 같은 장의 절
            a=tok.replace('-','–').split('–'); c=out[-1][3]; out.append([b,c,int(a[0]),c,int(a[-1])]); continue
        m=re.match(r'\s*([가-힣]+)\s*', tok)
        if m and m.group(1) in AB: b=AB.index(m.group(1))+1; tok=tok[m.end():]
        tok=tok.strip().replace('-', '–')
        m=re.match(r'^(\d+)(?::(\d+))?(?:–(\d+)(?::(\d+))?)?$', tok)
        if not m or not b: raise ValueError('주소를 못 읽음: '+ref)
        c1=int(m.group(1)); v1=int(m.group(2) or 1)
        if m.group(4): c2=int(m.group(3)); v2=int(m.group(4))
        elif m.group(3) and m.group(2): c2=c1; v2=int(m.group(3))
        elif m.group(3): c2=int(m.group(3)); v2=999
        else: c2=c1; v2=int(m.group(2) or 999)
        out.append([b,c1,v1,c2,v2])
    return out
def chapters(sg):
    L=[]
    for b,c1,v1,c2,v2 in sg:
        for c in range(c1,c2+1):
            if [b,c] not in L: L.append([b,c])
    return L
def build():
    S=json.load(open(os.path.join(D,'sermons.json')))['list']; out={}
    for s in S:
        r=segs(s['r']); ch=chapters(segs(s['show'])) if s.get('show') else chapters(r)
        for x in chapters(r):
            if x not in ch: ch.append(x)
        q=dict(s.get('qt') or {})
        def fix(v): return [segs(x)[0] for x in v] if isinstance(v,list) else segs(v)[0]
        for k in ('frame','obs','gap'):
            if k in q: q[k]=dict(q[k], v=fix(q[k]['v']), vs=q[k]['v'])
        if 'god' in q: q['god']=[dict(g, v=fix(g['v']), vs=g['v']) for g in q['god']]
        if 'hold' in q: q['hold']={'v':fix(q['hold']),'vs':q['hold']}
        out[s['d']]={'r':s['r'],'rs':r,'ch':ch,'t':s.get('t',''),'sample':bool(s.get('sample')),'qt':q}
    return out
if __name__=='__main__': print(json.dumps(build(),ensure_ascii=False)[:400])
