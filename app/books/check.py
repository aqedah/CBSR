import json,base64,gzip,sys,re
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
D=json.load(open(sys.argv[1])); bad=[]
L={"what":(60,220),"why":(30,150),"look":(20,110),"christ":(20,130)}
for k,v in D.items():
    b=int(k)
    for f,(a,z) in L.items():
        t=v.get(f,"")
        if not isinstance(t,str) or not (a<=len(t)<=z): bad.append(f"{k} {f} 길이 {len(t) if isinstance(t,str) else t}")
    kv=v.get("key")
    try:
        assert kv[0]==b; B[kv[0]-1][kv[1]-1][kv[2]-1]
    except Exception: bad.append(f"{k} key 잘못됨 {kv}")
    txt=" ".join(" ".join(c) for c in B[b-1])
    for f in L:
        for m in re.finditer(r'[“"]([^”"]{4,})[”"]',v.get(f,"")):
            if m.group(1) not in " ".join(" ".join(" ".join(c) for c in bk) for bk in B): bad.append(f"{k} {f} 인용 불일치: {m.group(1)[:30]}")
        for m in re.finditer(r'(\d+)\s*[–-]\s*(\d+)장|(\d+)장',v.get(f,"")):
            n=int(m.group(2) or m.group(3)); 
            if f!="christ" and n>len(B[b-1]): bad.append(f"{k} {f} 장 번호 {n} > {len(B[b-1])}")
print(len(D),"권 점검"); print("\n".join(bad) if bad else "문제 없음")
