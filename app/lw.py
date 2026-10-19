import json,gzip,base64,re,math,collections
B=json.loads(gzip.decompress(base64.b64decode(open('bible.b64').read())))
plan=json.load(open('plan.json'))['plan']
P=['께서','에게서','으로부터','에게','에서','으로','까지','부터','이니라','이라','이요','이며','이니','이나','이여','이','가','을','를','은','는','의','에','로','과','와','도','만','아','야','여','라','요']
P.sort(key=len,reverse=True)
STOP=set('그 이 저 것 자 때 날 사람 말 일 곳 가운데 우리 너희 그들 내 네 나 너 그가 그의 모든 모두 또 및 위 앞 뒤 속 안 밖 중 줄 수 이제 거기 여기 그러나 그런즉 이에 또한 곧 다 한 두 세 그러므로 그리고 하나 둘 셋 무리 자기 그녀 아들 이스라엘 여호와 하나님 예수 주 왕 백성 땅 집 손 이름 마음 소리 눈 날에 그날 오늘 이것 저것 무엇 누구 어찌 어떤 그것 이러므로 그때 자손 사람들 하늘 아버지'.split())
def stems(t):
    out=[]
    for w in re.findall(r'[가-힣]+',t):
        for p in P:
            if len(w)>len(p)+1 and w.endswith(p):
                out.append(w[:-len(p)]); break
        else:
            pass
    return out
df=collections.Counter(); tf_days=[]
for w in plan:
    for d in w:
        txt=' '.join(' '.join(B[b-1][c-1]) for b,c in d['ch'])
        c=collections.Counter(s for s in stems(txt) if len(s)>=2 and s not in STOP)
        tf_days.append(c); df.update(set(c))
N=len(tf_days)
def top(i,k=6):
    c=tf_days[i]; sc=[(n*math.log(N/df[s]),s,n) for s,n in c.items() if n>=3]
    return sorted(sc,reverse=True)[:k]
for key in [(0,0),(2,1),(3,3),(16,1),(32,1),(37,1),(39,5),(22,0),(41,4)]:
    i=key[0]*6+key[1]; print(plan[key[0]][key[1]]['spec'],[(s,n) for _,s,n in top(i)])
