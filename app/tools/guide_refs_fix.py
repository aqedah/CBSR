# 가이드북 원고 "성경 전체로"의 책 약칭 맞추기(2026-11-12, 태블릿 검수 R01).
# 책 이름 없는 주소는 앞에 나온 책으로 읽히므로, 책이 바뀌는 자리마다 약칭을 붙인다.
# 확인만: python3 tools/guide_refs_fix.py   고치기: python3 tools/guide_refs_fix.py --write
import json,re,sys
import os
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site_src','guide_qt.json'); raw=open(P).read(); D=json.loads(raw)
BK='창 출 레 민 신 수 삿 룻 삼상 삼하 왕상 왕하 대상 대하 스 느 에 욥 시 잠 전 아 사 렘 애 겔 단 호 욜 암 옵 욘 미 나 합 습 학 슥 말 마 막 눅 요 행 롬 고전 고후 갈 엡 빌 골 살전 살후 딤전 딤후 딛 몬 히 약 벧전 벧후 요일 요이 요삼 유 계'.split()
pat=re.compile(r'(^|[^가-힣])(?:('+'|'.join(sorted(BK,key=len,reverse=True))+r')\s?)?(\d{1,3}):(\d{1,3})')
INT="""2 5:17 롬|5 15:6 창|5 4:9 롬|7 21:10 창|9 25:23 창|9 9:11 롬|10 28:12 창|11 12:6 호|15 7:35 행|16 7:48 행|19 3:6 출|19 12:27 막|20 9:16 출|20 9:18 롬|21 5:8 고전|22 10:5 고전|23 6:35 요|24 19:6 출|25 24:8 출|25 9:12 히|26 25:40 출|26 8:1 히|27 31:17 출|28 34:33 출|28 3:14 고후|29 35:5 출|30 40:35 출|31 2:13 레|33 10:2 레|34 12:8 레|37 22:40 마|38 22:19 레|40 25:10 레|42 3:12 민|43 6:25 민|43 67:2 시|44 8:2 민|44 1:20 계|45 9:17 민|45 10:5 고전|46 11:34 민|46 10:11 고전|47 4:2 히|49 21:8 민|51 27:17 민|52 30:2 민|52 5:37 마|55 35:11 민|57 10:21 막|58 6:16 신|58 6:13 신|60 14:29 신|62 3:23 행|63 9:9 고전|64 3:13 갈|66 32:21 신|67 1:5 수|70 13:1 수|71 2:3 삿|75 2:16 삿|75 13:22 행|77 9:6 사|79 5:2 전|80 13:3 삿|85 78:70 시|87 12:23 삼상|89 13:23 행|90 59:9 시|91 12:7 마|92 24:12 삼상|93 28:6 삼상"""
want={}
for it in INT.split('|'):
    n,r,b=it.split(); want[(n,r)]=b
used=set(); changed=[]
for n,v in D['qt'].items():
    x=(v.get('obs') or {}).get('christ')
    if not x: continue
    out=[]; i=0; last=None
    for m in pat.finditer(x):
        r=m.group(3)+':'+m.group(4)
        if m.group(2): last=m.group(2); continue
        if not last: continue
        w=want.get((n,r))
        if w is None: print('UNLISTED',n,r,last); continue
        used.add((n,r))
        if w!=last:
            s=m.start(3); out.append((s,w+' ')); changed.append((n,r,last,'→',w)); last=w
    for s,ins in sorted(out,reverse=True): x=x[:s]+ins+x[s:]
    v['obs']['christ']=x
pass
for c in changed: print(*c)
print(len(changed))
if '--write' in sys.argv:
    open(P,'w').write(json.dumps(D,ensure_ascii=False,indent=1)+('\n' if raw.endswith('\n') else ''))
