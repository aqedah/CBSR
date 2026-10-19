# 사용법: python3 tools/readrj.py 주-일 [주-일 ...]   예: 33-3  → 리딩지저스 그날 본문(개역개정)
import json,base64,gzip,sys
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
P=json.load(open('/home/claude/rj/plan.json')); full=P['full']
for a in sys.argv[1:]:
    w,d=map(int,a.split('-')); day=P['plan'][w-1][d-1]; print(f"### {w}주차 {d}일째 · {day['label']}")
    for b,c in day['ch']:
        print(f"[{full[b-1]} {c}{'편' if b==19 else '장'}]")
        for i,v in enumerate(B[b-1][c-1]): print(f"{c}:{i+1} {v}")
