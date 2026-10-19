import json,base64,gzip,sys,re
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
G=json.load(open('/home/claude/rj/routes/gaz_coords.json'))
R=json.load(open(sys.argv[1])); bad=[]
P="(이여|이라는|이라고|이란|이라|이요|이며|이니|이나|으로부터|에서부터|에서는|으로|에서|에게|께서|까지|부터|에도|에는|보다|과|와|이|가|은|는|을|를|로|여|아|야|라|요|며|니|나|에|의|도|만|인)*"
for i,r in enumerate(R):
    try:
        b=r["b"]; c1,c2=r["c"]; assert 1<=c1<=c2<=len(B[b-1]); assert isinstance(r["n"],str) and r["n"]
    except Exception as e: bad.append(f"{i}: b/c/n 잘못 {r.get('n')}"); continue
    if len(r.get("p",[]))<2: bad.append(f"{i} {r['n']}: 지점 2곳 미만")
    text=" ".join(t for c in range(c1,c2+1) for t in B[b-1][c-1])
    text0=" ".join(t for c in range(max(1,c1-2),c2+1) for t in B[b-1][c-1])
    for qi,q in enumerate(r.get("p",[])):
        n=q[0]
        if not (24<=q[1]<=43 and 10<=q[2]<=53): bad.append(f"{i} {r['n']}: {n} 좌표가 이상함 {q[1:3]}")
        if n in G and (abs(G[n][0]-q[1])>0.05 or abs(G[n][1]-q[2])>0.05): bad.append(f"{i} {r['n']}: {n} 좌표가 지도 값 {G[n]}과 다름")
        if n not in G and (len(q)<4 or q[3]!=1): bad.append(f"{i} {r['n']}: {n} 지도에 없는 곳인데 대략 표시(4번째 값 1)가 없음")
        if not re.search("(?<![가-힣])"+re.escape(n)+P+"(?![가-힣])",text0 if qi==0 else text): bad.append(f"{i} {r['n']}: '{n}'이 {b}번 책 {c1}–{c2}장 본문에 없음")
print(len(R),"개 점검"); print("\n".join(bad) if bad else "문제 없음")
