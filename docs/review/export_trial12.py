# 12월 체험판 원고(app/site_src/trial26_qt.json)를 검수용 CSV 세 묶음으로 뽑습니다.
# 저장소 맨 위에서: python docs/교정/export_trial_csv.py
import json,csv,re,os
R=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(R,'..','..','app','site_src','trial26_qt.json'),encoding='utf-8'))['qt']
PROT=['이야기 속의 하나님께서 오늘','점점 심화됩니다','속마음을 열어 독자에게','하나님, 선지자, 시인, 사도가 직접','두 줄이 서로 호응하거나','둘째 줄이 첫째 줄에서 무엇을 더하는지','상상력을 자극하고','평생의 반려 성경책']
NAME=[('sub','소제목'),('guide.today','① 오늘의 흐름'),('map.cap','지도 설명'),('guide.word','말뜻'),('v27.start','시작 안내'),('v27.scenes','장면 나눔'),('v27.marks','② 성경 읽기(읽으며 표시)'),('v27.find','② 찾을 것'),('obs.look','다시 읽을 곳'),('obs.pair','③ 눈여겨볼 것'),('v27.looks','③ 눈여겨볼 것'),('obs.q','④ 본문 관찰'),('v27.god','④ 하나님의 성품'),('god','성품 한 문장(해설 끝에 붙음)'),('apply','④ 적용'),('pray','④ 오늘의 기도'),('obs.christ','⑤ 성경 전체로'),('note','⑤ 해설'),('v27.link','다음 날로 잇는 말'),('hymn','찬송'),('ldr','주일 인도자 원고')]
SKIP=re.compile(r'(^u$|^attr$|hymn\.(no|t)$|\.tool$|\.rep$|\.ck$|^guide\.find$|^ref$|^title$|^map\.(show|route|routes|emph))')
def walk(o,p):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,p+[k])
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,p+[str(i)])
    elif isinstance(o,str): yield '.'.join(p),o
def cname(path):
    for k,n in NAME:
        if path==k or path.startswith(k+'.'): return n
    return path
order={n:i for i,(k,n) in enumerate(NAME)}
rows=[];no=0
days=[d for d in T if not d.isdigit()]+sorted([d for d in T if d.isdigit()],key=int)
for d in days:
    seen=set(); items=[]
    for path,s in walk(T[d],[]):
        if SKIP.search(path) or not s.strip() or re.fullmatch(r'[\d:–\-, ;]+',s): continue
        if path.startswith('obs.look') and path.endswith('.0'): continue
        if s in seen: continue
        seen.add(s); items.append((path,s))
    if d.isdigit(): items.sort(key=lambda x:order.get(cname(x[0]),99))
    for path,s in items:
        no+=1
        mark='목사님 문장(고치지 말고 의견만)' if any(p in s for p in PROT) else ('책머리' if not d.isdigit() else '')
        rows.append({'번호':no,'날':d if not d.isdigit() else f'{d}일','칸':cname(path) if d.isdigit() else '책머리','칸 경로':path,'원문':s,'표시':mark})
def dn(r):
    x=str(r['날']).replace('일',''); return int(x) if x.isdigit() else 0
for k,f in {1:lambda d:d<=333,2:lambda d:334<=d<=350,3:lambda d:d>=351}.items():
    with open(os.path.join(R,f'12월체험판_원고_{k}.csv'),'w',encoding='utf-8-sig',newline='') as o:
        w=csv.DictWriter(o,fieldnames=['번호','날','칸','칸 경로','원문','표시']); w.writeheader(); w.writerows([r for r in rows if f(dn(r))])
print(len(rows))
