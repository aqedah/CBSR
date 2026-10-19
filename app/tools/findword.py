# 사용법: python3 tools/findword.py 낱말 [책번호…]  → 그 낱말이 (앞뒤가 다른 글자에 붙지 않고, 뒤에 조사만 붙은 채) 나오는 절 목록
import json,base64,gzip,sys,re
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
A=json.load(open('/home/claude/rj/plan.json'))['abbr']
w=sys.argv[1]; books=[int(x) for x in sys.argv[2:]] or range(1,67)
P="(이여|이라는|이라고|이란|이라|이요|이며|이니|이나|으로|에서|에게|께서|에게서|까지|부터|과|와|이|가|은|는|을|를|과|와|로|여|아|야|라|요|며|니|나|에|의|도|만)?"
r=re.compile("(?<![가-힣])"+re.escape(w)+P+"(?![가-힣])"); n=0
for b in books:
    for c,ch in enumerate(B[b-1]):
        for v,t in enumerate(ch):
            if r.search(t): n+=1; print(f"{A[b-1]} {c+1}:{v+1} {t[:90]}") if n<=15 else None
print("모두",n,"절")
