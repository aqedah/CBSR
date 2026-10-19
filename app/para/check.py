import json,base64,gzip,sys
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
D=json.load(open(sys.argv[1])); b0=int(sys.argv[2]); b1=int(sys.argv[3]) if len(sys.argv)>3 else b0
c0,c1=(int(sys.argv[4]),int(sys.argv[5])) if len(sys.argv)>5 else (1,999)
need={f"{b}-{c}" for b in range(b0,b1+1) for c in range(1,len(B[b-1])+1) if b0!=b1 or c0<=c<=c1}
bad=[f"{k} 빠짐" for k in sorted(need-set(D))]; tot=0
for k,L in D.items():
    b,c=map(int,k.split('-')); n=len(B[b-1][c-1])
    if not isinstance(L,list) or any(not isinstance(x,int) for x in L): bad.append(f"{k} 형식"); continue
    if L!=sorted(set(L)): bad.append(f"{k} 순서/중복")
    if any(x<2 or x>n for x in L): bad.append(f"{k} 범위 밖 절")
    if n>=8 and len(L)>n/2: bad.append(f"{k} 너무 잘게 나눔 ({len(L)}곳/{n}절)")
    tot+=len(L)
print("\n".join(bad[:60]) if bad else "문제 없음", f"({len(D)}장, 문단 시작 {tot}곳)")
