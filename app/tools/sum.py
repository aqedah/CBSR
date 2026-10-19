# 사용법: python3 tools/sum.py 날번호 ...  → 365 통독표 그날 범위·주제·요약(이미 검수됨)
import json,glob
P=json.load(open('/home/claude/rj/plan365.json')); S={}
for f in glob.glob('/home/claude/rj/s365/part*.json'): S.update(json.load(open(f)))
import sys
for n in sys.argv[1:]:
    d=P[int(n)-1]; print(f"{n}일 · {d['label']} · 주제: {d['topic']}\n  요약: {S.get(str(n),{}).get('s','')}")
