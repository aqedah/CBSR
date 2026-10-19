import json,base64,gzip,sys,re
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
P="(이여|이라는|이라고|이란|이라|이요|이며|이니|이나|으로|에서|에게|께서|에게서|까지|부터|과|와|이|가|은|는|을|를|과|와|로|여|아|야|라|요|며|니|나|에|의|도|만)?"
D=json.load(open(sys.argv[1])); bad=[]
K=None
for n,v in D.items():
    if len(n)<2: bad.append(f"{n}: 한 글자")
    d=v.get("d","")
    if not 25<=len(d)<=160: bad.append(f"{n}: 설명 길이 {len(d)}")

    r=re.compile("(?<![가-힣])"+re.escape(n)+P+"(?![가-힣])")
    try:
        b,c,vv=v["r"]; t=B[b-1][c-1][vv-1]
        if not r.search(t): bad.append(f"{n}: 대표 구절 {v['r']}에 이름이 없음")
    except Exception: bad.append(f"{n}: 대표 구절 잘못 {v.get('r')}")
    for b in v.get("b",[]):
        if not any(r.search(t) for ch in B[b-1] for t in ch): bad.append(f"{n}: {b}번 책에 이름이 없음")
    if not v.get("b"): bad.append(f"{n}: b 없음")
print(len(D),"명 점검"); print("\n".join(bad) if bad else "문제 없음")
