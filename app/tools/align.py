# 사용법: python3 tools/align.py snb|shg 낱말 [개수]  → 개역개정에 그 낱말이 나오는 절과, 같은 절의 새번역(snb)/새한글(shg) 본문을 나란히
import json,base64,gzip,sys,re
k=sys.argv[1]; n=sys.argv[2]; lim=int(sys.argv[3]) if len(sys.argv)>3 else 5
B=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
T=json.loads(gzip.decompress(base64.b64decode(open(f'/home/claude/rj/bible_{k}.b64').read())))
A=json.load(open('/home/claude/rj/plan.json'))['abbr']
P="(이여|이라는|이라고|이란|이라|이요|이며|이니|이나|으로|에서|에게|께서|까지|부터|과|와|이|가|은|는|을|를|로|여|아|야|라|요|며|니|나|에|의|도|만|인)?"
r=re.compile("(?<![가-힣])"+re.escape(n)+P+"(?![가-힣])"); c=0
for b,bk in enumerate(B):
    for ci,ch in enumerate(bk):
        for v,t in enumerate(ch):
            if r.search(t):
                c+=1
                if c<=lim: print(f"[{A[b]} {ci+1}:{v+1}]\n  개역개정: {t}\n  {'새번역' if k=='snb' else '새한글'}: {T[b][ci][v]}")
print("개역개정에 모두",c,"절")
