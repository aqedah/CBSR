# 사용법: python3 tools/sumrj.py 주-일 ...  → 리딩지저스 그날 범위·요약(이미 검수됨). 주의 6일째 다음은 다음 주 1일째.
import json,sys
P=json.load(open('/home/claude/rj/plan.json')); S=json.load(open('/home/claude/rj/srj/summ.json'))
for a in sys.argv[1:]:
    w,d=map(int,a.split('-')); print(f"{w}-{d} · {P['plan'][w-1][d-1]['label']}\n  요약: {S[w-1][d-1]}")
