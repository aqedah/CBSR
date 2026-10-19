# 사용법: python3 tools/read.py 날번호   → 365 통독표 그날 본문(개역개정) 출력
import json,base64,gzip,sys
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
P=json.load(open('/home/claude/rj/plan365.json')); full=json.load(open('/home/claude/rj/plan.json'))['full']
for n in sys.argv[1:]:
    d=P[int(n)-1]; print(f"### {d['n']}일 · {d['label']} · 주제: {d['topic']}")
    for b,c in d['ch']:
        print(f"[{full[b-1]} {c}장]")
        for i,v in enumerate(B[b-1][c-1]): print(f"{c}:{i+1} {v}")
