import json,base64,gzip,sys,re
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
N=json.load(open('/home/claude/rj/ux/names.json')); PE,PL,GL=set(N['pe']),set(N['pl']),set(N['gl'])
D=json.load(open(sys.argv[1])); b0,b1=int(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)>3 else int(sys.argv[2]); bad=[]
c0,c1=(int(sys.argv[4]),int(sys.argv[5])) if len(sys.argv)>5 else (1,999)
need={f"{b}-{c}" for b in range(b0,b1+1) for c in range(1,len(B[b-1])+1) if b0!=b1 or c0<=c<=c1}
for k in sorted(need-set(D)): bad.append(f"{k} 빠짐")
for k,v in D.items():
    b,c=map(int,k.split('-'));
    try: txt=" ".join(B[b-1][c-1])
    except Exception: bad.append(f"{k} 없는 장"); continue
    t=v.get('t','')
    if not (6<=len(t)<=30): bad.append(f"{k} t 길이 {len(t)}")
    for f,S,mx in (('pe',PE,3),('pl',PL,3),('w',GL,2)):
        L=v.get(f,[])
        if not isinstance(L,list) or len(L)>mx: bad.append(f"{k} {f} 개수"); continue
        for n in L:
            if n not in S: bad.append(f"{k} {f} 목록에 없음: {n}")
            elif n not in txt: bad.append(f"{k} {f} 본문에 없음: {n}")
    q=v.get('qz')
    if not q: bad.append(f"{k} qz 없음"); continue
    o=q.get('o',[]); a=q.get('a'); h=q.get('h',[])
    if len(o)!=4 or not isinstance(a,int) or not 0<=a<4: bad.append(f"{k} 보기/정답")
    if len(h)!=4 or h[a] is not None or any((x is None) for i,x in enumerate(h) if i!=a): bad.append(f"{k} 힌트 형식")
    if len(q.get('q',''))>110: bad.append(f"{k} 질문 김")
    r=q.get('ref')
    try:
        assert r[0]==b and r[1]==c; B[b-1][c-1][r[2]-1]
    except Exception: bad.append(f"{k} ref {r}")
    for s in [q.get('q','')]+o:
        for m in re.findall(r'"([^"]{4,})"',s):
            if m not in txt: bad.append(f"{k} 인용 불일치: {m[:30]}")
    if len(set(o))<4: bad.append(f"{k} 보기 중복")
print("\n".join(bad[:80]) if bad else "문제 없음", f"({len(D)}장)")
