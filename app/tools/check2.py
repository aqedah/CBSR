# 사용법: python3 tools/check2.py 파일.json  → 형식·구절·인용 점검
import json,base64,gzip,sys,re
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
RJ='--rj' in sys.argv; args=[a for a in sys.argv[1:] if a!='--rj']
if RJ:
    _P=json.load(open('/home/claude/rj/plan.json'))['plan']
    def getday(k): w,d=map(int,k.split('-')); return _P[w-1][d-1]
else:
    _P=json.load(open('/home/claude/rj/plan365.json'))
    def getday(k): return _P[int(k)-1]
D=json.load(open(args[0])); bad=[]
def strs(x):
    if isinstance(x,str): yield x
    elif isinstance(x,dict):
        for v in x.values(): yield from strs(v)
    elif isinstance(x,list):
        for v in x: yield from strs(v)
for k,v in D.items():
    p=getday(k); chs={tuple(c) for c in p['ch']}; books={c[0] for c in p['ch']}
    text=" ".join(B[b-1][c-1][i] for b,c in p['ch'] for i in range(len(B[b-1][c-1])))
    def ref_ok(r,where):
        try:
            b,c,vv=r; B[b-1][c-1][vv-1]
            if (b,c) not in chs: bad.append(f"{k} {where}: {r} 그날 범위 밖")
        except Exception: bad.append(f"{k} {where}: {r} 없는 구절")
    g=v.get('g',{})
    for f in ('prev','today','find'):
        if not isinstance(g.get(f),str) or not g.get(f).strip(): bad.append(f"{k} g.{f} 없음")
    e=v.get('e',{})
    if not e.get('q'): bad.append(f"{k} e.q 없음")
    L=e.get('look',[])
    if not 2<=len(L)<=3: bad.append(f"{k} e.look 개수 {len(L)}")
    for i,l in enumerate(L):
        if not l.get('t') or not l.get('n'): bad.append(f"{k} look{i} t/n 없음")
        ref_ok(l.get('r'),f"look{i}")
    Q=v.get('qz',[])
    if len(Q)!=2 and not (RJ and k.startswith('33-') and len(Q)==0): bad.append(f"{k} qz 개수 {len(Q)}")
    for i,q in enumerate(Q):
        o=q.get('o',[]); h=q.get('h',[]); a=q.get('a')
        if q.get('t')=='ox':
            if o!=["O","X"]: bad.append(f"{k} qz{i} ox 보기")
        elif q.get('t')!='mc' or len(o)!=4: bad.append(f"{k} qz{i} mc 보기 4개 아님")
        if not isinstance(a,int) or not 0<=a<len(o): bad.append(f"{k} qz{i} 정답 번호")
        elif len(h)!=len(o) or h[a] is not None or any(not x for j,x in enumerate(h) if j!=a): bad.append(f"{k} qz{i} 힌트(정답 자리는 null, 나머지는 글)")
        if q.get('kind') not in ('이야기 흐름','눈여겨보기','뜻 생각하기'): bad.append(f"{k} qz{i} kind")
        ref_ok(q.get('ref'),f"qz{i}")
    for s in strs(v):
        for m in re.finditer(r'(?<![\d:])(\d{1,3}):(\d{1,3})(?![\d])',s):
            c,vv=int(m.group(1)),int(m.group(2))
            okc=[(b,c) for b in books if (b,c) in chs]
            if not okc: bad.append(f"{k} 글 속 {m.group(0)} 그날 장 아님 :: {s[:40]}")
            elif not any(vv<=len(B[b-1][c-1]) for b,_ in okc): bad.append(f"{k} 글 속 {m.group(0)} 없는 절")
        for m in re.finditer(r'[“"]([^”"]{4,})[”"]',s):
            if m.group(1) not in text: bad.append(f"{k} 인용 불일치: {m.group(1)[:40]}")
print(len(D),"일 점검"); print("\n".join(bad) if bad else "문제 없음")
