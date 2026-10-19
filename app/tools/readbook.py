# 사용법: python3 tools/readbook.py 책번호 [시작장 끝장]  → 개역개정 본문 출력
import json,base64,gzip,sys
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
F=json.load(open('/home/claude/rj/plan.json'))['full']
b=int(sys.argv[1]); a=int(sys.argv[2]) if len(sys.argv)>2 else 1; z=int(sys.argv[3]) if len(sys.argv)>3 else len(B[b-1])
for c in range(a,z+1):
    print(f"[{F[b-1]} {c}{'편' if b==19 else '장'}]")
    for i,v in enumerate(B[b-1][c-1]): print(f"{c}:{i+1} {v}")
