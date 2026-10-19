import json,gzip,base64,re
K=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
PARA=json.load(open('/home/claude/rj/para/all.json'))
PE=set(json.load(open('/home/claude/rj/people/all.json')).keys())
PL=set(json.load(open('/home/claude/rj/places/all.json')).keys()) if __import__('os').path.exists('/home/claude/rj/places/all.json') else set()
NAMES=sorted([n for n in PE|PL if len(n)>=2],key=len,reverse=True)
ABBR="창 출 레 민 신 수 삿 룻 삼상 삼하 왕상 왕하 대상 대하 스 느 에 욥 시 잠 전 아 사 렘 애 겔 단 호 욜 암 옵 욘 미 나 합 습 학 슥 말 마 막 눅 요 행 롬 고전 고후 갈 엡 빌 골 살전 살후 딤전 딤후 딛 몬 히 약 벧전 벧후 요일 요이 요삼 유 계".split()
def scope(e,chs):
    if e.get('sc'): return e['sc']
    R=[]
    for l in e.get('look',[]):
        b,c,v=l['r']
        if [b,c] not in chs: continue
        st=PARA.get(f"{b}-{c}",[1]); s0=1
        for x in st:
            if x<=v: s0=x
        nx=[x for x in st if x>v]; t=nx[0]-1 if nx else len(K[b-1][c-1])
        m=[r for r in R if r[0]==b and r[1]==c and not (t<r[2]-1 or s0>r[3]+1)]
        if m: m[0][2]=min(m[0][2],s0); m[0][3]=max(m[0][3],t)
        else: R.append([b,c,s0,t])
    return R
def text(R): return " ".join(K[b-1][c-1][v-1] for b,c,s,t in R for v in range(s,t+1) if v-1<len(K[b-1][c-1]))
def names_in(q):
    out=[]; qq=q
    for n in NAMES:
        if re.search(r'(?<![가-힣])'+re.escape(n),qq): out.append(n); qq=qq.replace(n,' ')
    return out
def lab(R): return ", ".join(f"{ABBR[b-1]} {c}:{s}–{t}" for b,c,s,t in R)
rows=[]
P365=json.load(open('/home/claude/rj/plan365.json')); E365=json.load(open('/home/claude/rj/s365b/all.json'))
for i,day in enumerate(P365):
    e=E365.get(str(i+1),{}).get('e')
    if not e or not e.get('q'): continue
    R=scope(e,day['ch']); 
    if not R: continue
    T=text(R); dayT=" ".join(" ".join(K[b-1][c-1]) for b,c in day['ch'])
    miss=[n for n in names_in(e['q']) if n not in T]
    if miss: rows.append(("365",i+1,day['label'],e['q'],lab(R),miss,[n for n in miss if n not in dayT]))
print(len(rows))
json.dump(rows,open('/home/claude/rj/ux/scope_rows.json','w'),ensure_ascii=False,indent=0)
for r in rows[:15]: print(r)
