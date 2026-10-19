import json,base64,gzip,sys
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
N=set(json.load(open('/home/claude/rj/traits/names.json')))
D=json.load(open(sys.argv[1])); b0=int(sys.argv[2]); b1=int(sys.argv[3]) if len(sys.argv)>3 else b0
c0,c1=(int(sys.argv[4]),int(sys.argv[5])) if len(sys.argv)>5 else (1,999)
need={f"{b}-{c}" for b in range(b0,b1+1) for c in range(1,len(B[b-1])+1) if b0!=b1 or c0<=c<=c1}
bad=[f"{k} 빠짐" for k in sorted(need-set(D))]
for k,L in D.items():
    b,c=map(int,k.split('-'))
    if not isinstance(L,list) or len(L)>2: bad.append(f"{k} 목록 형식"); continue
    ns=[x.get('n') for x in L]
    if len(set(ns))<len(ns): bad.append(f"{k} 같은 성품 둘")
    for x in L:
        if x.get('n') not in N: bad.append(f"{k} 목록에 없는 성품: {x.get('n')}")
        try: B[b-1][c-1][x['v']-1]
        except Exception: bad.append(f"{k} 없는 절 {x.get('v')}")
print("\n".join(bad[:60]) if bad else "문제 없음", f"({len(D)}장, 성품 있는 장 {sum(1 for L in D.values() if L)})")
