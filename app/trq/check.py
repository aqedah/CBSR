import json,base64,gzip,sys,re
T={k:json.loads(gzip.decompress(base64.b64decode(open(f'/home/claude/rj/bible_{k}.b64').read()))) for k in ('snb','shg')}
ALL={k:" ".join(t for bk in v for ch in bk for t in ch) for k,v in T.items()}
strip=lambda s:re.sub(r'[“”‘’"]','',s)
ALL2={k:strip(v) for k,v in ALL.items()}
D=json.load(open(sys.argv[1])); bad=[]
for q,o in D.items():
    for k in ('snb','shg'):
        s=(o or {}).get(k)
        if s is None: continue
        for part in re.split(r'\s*…\s*',strip(s)):
            part=part.strip(' .')
            if part and part not in ALL2[k]: bad.append(f"[{k}] {q[:20]} → '{part[:40]}' 본문에 없음")
print(len(D),"개"); print("\n".join(bad) if bad else "문제 없음")
