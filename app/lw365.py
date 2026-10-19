import json,gzip,base64,re,math,collections
B=json.loads(gzip.decompress(base64.b64decode(open('bible.b64').read())))
P=json.load(open('plan365.json')); plan=[P[i:i+7] for i in range(0,len(P),7)]
# 표시형: 정규식(어절 시작)
V="""믿음:믿음|믿으|믿는|믿고|믿었|믿지
은혜:은혜
사랑:사랑
복음:복음
율법:율법
의:의롭|의로|의를|의가|의의|의와
죄:죄
언약:언약
성전:성전
포도원:포도원
광야:광야
피:피를|피가|피로|피의|피는|피와
어린 양:어린 양
빛:빛
어둠:어둠|흑암
생명:생명
영광:영광
기쁨:기쁨|기뻐|즐거워|즐거움
고난:고난|환난
평강:평강|평안
소망:소망
지혜:지혜|지혜로
미련한 자:미련한|어리석
악인:악인|악한 자|악을
의인:의인
목자:목자
양:양을|양이|양의|양들|양 떼|양떼
떡:떡
물:물을|물이|물로|물에|물과
열매:열매
씨:씨를|씨가|씨는|씨의|씨앗
나라:나라
심판:심판
진노:진노|노하|분노
긍휼:긍휼|불쌍히|자비
거룩:거룩
복:복을|복이|복된|복 있|복의
저주:저주
우상:우상
제단:제단
제사:제사|번제|제물
기도:기도
찬양:찬양|찬송|송축
금식:금식
회개:회개|돌이키|돌아오
용서:용서|사하
구원:구원|건지|구속|속량
부활:부활|살아나|다시 살
십자가:십자가
종:종이|종을|종의|종들|종으로|종과
자유:자유
육체:육체|육신
성령:성령|영이|영을|영으로
세상:세상
진리:진리
길:길을|길이|길로|길에|길은
문:문을|문이|문에|문으로
반석:반석
눈물:눈물|울며|울었|통곡
두려움:두려워|두려움|무서워
아들:아들
아버지:아버지
형제:형제
이방:이방
왕:왕이|왕을|왕의|왕은|왕에게|왕께
전쟁:전쟁|싸우|싸움
칼:칼
불:불을|불이|불로|불에|불과|불 가운데
구름:구름
바다:바다
산:산에|산으로|산을|산이|산 위
땅:땅을|땅이|땅에|땅의
기업:기업
약속:약속
맹세:맹세
순종:순종|청종|듣지 아니|듣지 않
교만:교만|높이|높아
겸손:겸손|낮추|낮아
보라:보라
기억:기억
잊:잊
지키:지키|지켜
말씀:말씀
음성:음성|소리
이름:이름
마음:마음
눈:눈을|눈이|눈으로|눈에
손:손을|손이|손으로|손에
진실:진실(?!로)|성실|신실|미쁘
진실로:진실로
선:선을|선한|선하|선이
악:악하|악이|악한
의심:의심
시험:시험|유혹
깨어:깨어|깨라
잠:잠들|잠을|자고|자더라|졸
보:보았|보니|보고|보매|보이
듣:들으|듣고|들었|들은|듣는
화 있을진저:화 있을진저|화로다|화 있으리라|화가 있으리로다
보시기에 좋았더라:보시기에 (?:심히 )?좋았더라
죽었더라:죽었더라
헛되다:헛되
인자하심이 영원함:인자하심이 영원
이기는 그:이기는 그
곧:곧(?= )
때:때가|때에|때를
여호와의 말씀:여호와의 말씀
네 하나님 여호와:네 하나님 여호와|너희 하나님 여호와"""
items=[]
for line in V.split('\n'):
    k,v=line.split(':',1); items.append((k,re.compile(r'(?<![가-힣])(?:'+v+')')))
days=[]
for wi,w in enumerate(plan):
    for di,d in enumerate(w):
        vs=[(b,c,i+1,t) for b,c in d['ch'] for i,t in enumerate(B[b-1][c-1])]
        txt=' '.join(t for *_,t in vs)
        days.append((vs,len(txt)))
tot_len=sum(L for _,L in days)
cnt=[[0]*len(items) for _ in days]; tot=[0]*len(items)
for di,(vs,L) in enumerate(days):
    for ii,(k,rx) in enumerate(items):
        n=sum(len(rx.findall(t)) for *_,t in vs); cnt[di][ii]=n; tot[ii]+=n
GENERIC={'곧','때','여호와의 말씀','네 하나님 여호와','보','듣','마음','말씀','이름','손','눈','땅','왕','아들','아버지','산','음성','종','길','물','양','나라','악','선','이방','형제','세상','지키','복','불','칼','문','잠'}
out={}
for di,(vs,L) in enumerate(days):
    sc=[]
    for ii,(k,rx) in enumerate(items):
        n=cnt[di][ii]
        if n<4: continue
        exp=tot[ii]*L/tot_len; ratio=n/max(exp,0.3)
        need=3.5 if k in GENERIC else 2.2
        if ratio<need: continue
        refs=[(b,c,v) for b,c,v,t in vs if rx.search(t)][:8]
        sc.append((n*math.log(ratio),k,n,round(ratio,1),refs))
    sc.sort(reverse=True)
    out[f"{di//7+1}-{di%7+1}"]=[[k,n,r,refs] for _,k,n,r,refs in sc[:4]]
# 강조: 같은 어절 연달아 반복
emph={}
for di,(vs,L) in enumerate(days):
    found=[]
    for b,c,v,t in vs:
        ws=t.split()
        for i in range(len(ws)-1):
            a=re.sub(r'[,.!?]','',ws[i]); bb=re.sub(r'[,.!?]','',ws[i+1])
            if a==bb and len(a)>=2 and not a.endswith('씩') and a not in ('대대로','점점','각각','따로','서로','가끔','조금','차차','흔들흔들','거듭') and not any(f[0]==a for f in found):
                n=2
                while i+n<len(ws) and re.sub(r'[,.!?]','',ws[i+n])==a: n+=1
                found.append([a,n,[b,c,v]])
    emph[f"{di//7+1}-{di%7+1}"]=found[:3]
json.dump(emph,open('emph365.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(out,open('leitwort365.json','w'),ensure_ascii=False,separators=(',',':'))
print(sum(1 for v in out.values() if not v),'days empty')
