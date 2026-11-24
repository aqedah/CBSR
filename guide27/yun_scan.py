# 윤문 후보 자동 검색 (2026-11-24). 쓰는 법: python3 guide27/yun_scan.py 결과.json  — 저장소 맨 위에서 돌립니다. 성경 인용(큰따옴표 안)은 보지 않습니다.
import json,re,collections,sys
SRC={'2027가이드북':'app/site_src/guide_qt.json','체험판':'app/site_src/trial26_qt.json','세라핌·절기':'app/site_src/season.json','주일공과':'app/site_src/sunday_qt.json','성경책장':'app/site_src/shelf_66.json','스토리카드':'app/ux/story_cards.json'}
SKIP_KEYS={'u','img','pic','map','color','light','ymd','key','id','kind','date','vv','youth','churchn','no','n','ch'}
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in SKIP_KEYS: continue
            yield from walk(v,path+[str(k)])
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,path+[str(i)])
    elif isinstance(o,str) and len(o)>=8 and re.search('[가-힣]',o): yield path,o
def strip_quotes(s): return re.sub(r'"[^"]*"|“[^”]*”','"…"',s)  # 성경 인용 안은 보지 않음
P=[
 ('견주다','고유어 약한 말 → 비교하다',r'견주'),
 ('재다','"쓸모를 재다"류: 무엇을 하는 말인지 흐림',r'(?<![가-힣])재(는|어|고|며|다|면|던|ㄴ)\b|을 재|를 재'),
 ('서술자','"본문은"으로',r'서술자'),
 ('되풀이','"반복"으로(책머리 f0 제외)',r'되풀이'),
 ('줄 비유','흐린 "줄" 비유',r'의 줄(?:[이을은도에과로]|$)|줄을 (?:긋|잇|따라|타)|한 줄로 꿰'),
 ('맞서다','대조 뜻의 "맞서다"',r'맞서'),
 ('흐린 비유','가리키는 것이 바로 안 보이는 비유',r'내려옵니다|꿰뚫|매듭|눈이 옮겨|무게가 실|결이 |자리를 맞바꾸|선을 넘'),
 ('안심 문구','과잉 친절·방어 문구',r'괜찮습니다|하지 않아도 됩니다|선택입니다|부담 갖지|부담 없이'),
 ('번역투','~을 통해 / ~에 대해 / ~라는 점 / 가지다',r'을 통해|를 통해|에 대해|에 대한|라는 점|을 가지|를 가지|가지고 있'),
 ('AI 말투','바로 ~입니다 / 단순히 ~이 아니라 / 오롯이 / 고스란히 / 셈입니다',r'단순히|오롯이|고스란히|셈입니다|셈이지요|다름 아닌|그야말로'),
 ('문장 안 줄표','줄표로 압축',r'[가-힣)\]"’”] ?[—–] ?[가-힣"“‘(]'),
 ('가운뎃점 나열','문장 안 가운뎃점 나열',r'[가-힣]·[가-힣]+·[가-힣]'),
 ('견줌 낱말','비교 뜻 고유어 후보',r'빗대|맞대|나란히 놓'),
 ('쓸모','"쓸모" — 무엇을 위한 것인지 바로 쓰기',r'쓸모'),
]
out=[]; cnt=collections.Counter()
for name,f in SRC.items():
    try: D=json.load(open(f))
    except Exception as e: print('skip',f,e); continue
    for path,s in walk(D,[]):
        body=strip_quotes(s)
        for lab,why,rx in P:
            if lab=='되풀이' and 'f0' in path: continue
            for m in re.finditer(rx,body):
                a=max(0,m.start()-60); b=min(len(body),m.end()+60)
                out.append(dict(src=name,path='/'.join(path[:4]),lab=lab,why=why,ctx=body[a:b].replace('\n',' '))); cnt[(name,lab)]+=1
                break
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
srcs=list(SRC); labs=[p[0] for p in P]
print('갈래'.ljust(10),' '.join(s[:5].rjust(6) for s in srcs))
for l in labs: print(l.ljust(10),' '.join(str(cnt[(s,l)]).rjust(6) for s in srcs))
