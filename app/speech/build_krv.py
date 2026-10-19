# 개역개정: 따옴표가 없으므로 새번역(없으면 새한글)의 대화 위치를 길잡이로, 개역개정의 '이르되 … 하니라' 꼴에서 경계를 찾습니다.
import json,base64,gzip,re
def load(k): return json.loads(gzip.decompress(base64.b64decode(open(f'/home/claude/rj/{k}.b64').read())))
K=load('bible'); SN=load('bible_snb'); SH=load('bible_shg')
QS=json.load(open('bible_snb.json')); QH=json.load(open('bible_shg.json'))
START=re.compile(r'(?:이르시되|이르되|가라사대|가로되|가로대|말하되|말씀하시되|말씀하여 이르시되|대답하되|대답하시되|대답하여 이르시되|대답하여 이르되|여짜오되|여쭈되|외치되|외쳐 이르되|부르짖되|부르짖어 이르되|기도하여 이르되|기도하되|물으시되|묻되|물어 이르되|물어 가로되|명령하여 이르되|명하여 이르되|이르기를|일렀으되|하였으되|하셨으되|기록하였으되|기록된 바|쓰였으되|맹세하여 이르되|축복하여 이르되|노래하되|선포하되|하시되|하되|이르니라 ?|고하되|아뢰되|아뢰어 이르되|전하되|소리 질러 이르되|소리 질러|부르며|탄식하며 이르되|이르되)\s')
END=re.compile(r'\s(?:하시니라|하니라|하시고|하고|하매|하시매|하니|하시니|하더라|하였더라|하셨더라|하였느니라|하셨느니라|하므로|하시므로|하며|하시며|하였고|하셨고|하였으니|하셨으니|하신대|한대|하거늘|하시거늘|하는지라|하시는지라|함이라|하였음이라|하였나이다|하나이다|하였도다|하는도다|하였으므로|하였는지라|하셨는지라|한즉|하신즉|하였은즉|하였으나|하셨으나|하나|하시나|하자|하시자|함이요|함이니|하더니|하시더니|할 때에|하실 때에|하였을 때에|라 하였더라|하였더니|하셨더니|하던|하는|하신|한|하였다|하셨다|하여|하사)(?=[\s.,]|$)')
def ratio(seg,L): return seg[0]/max(1,L), seg[1]/max(1,L)
FIN=re.compile(r'(?:냐|라|다|요|까|소서|이다|니라|도다|리라|노라|하라|이까|느냐|구나|지라|로다|니이다|나이다)(?=[\s,.!?]|$)')
def pick_start(t,pos,rs,s,ref,n):
    cont=(s==0 and not ref.lstrip().startswith('“'))
    if cont: return 0
    cands=[m.end() for m in START.finditer(t,pos)]
    near=[x for x in cands if abs(x/n-rs)<0.45]
    if near: return min(near,key=lambda x:abs(x/n-rs))
    return 0 if s==0 else None
def krv_segs(t,segs,L,ref):
    out=[]; pos=0; n=len(t)
    for i,(s,e) in enumerate(segs):
        a=pick_start(t,pos,s/L,s,ref,n)
        if a is None: continue
        nxt=None
        if i+1<len(segs):
            s2=segs[i+1][0]; cands=[m for m in START.finditer(t,a+2)]
            near=[m for m in cands if abs(m.end()/n-s2/L)<0.45]
            if near: nxt=min(near,key=lambda m:abs(m.end()/n-s2/L))
        if nxt is not None:
            lim=nxt.start(); ends=[m.start() for m in END.finditer(t,a+2,lim+1)]
            if ends: b=ends[-1]
            else:
                f=[m.end() for m in FIN.finditer(t,a+1,lim)]
                b=f[-1] if f else lim
        elif e>=L-1 or e/L>0.97:
            b=n
            m=list(END.finditer(t,a+2))
            if m and m[-1].end()>=n-1: b=m[-1].start()
        else:
            ends=[m.start() for m in END.finditer(t,a+2)]
            b=min(ends,key=lambda x:abs(x/n-e/L)) if ends else n
        while b>a and t[b-1]==' ': b-=1
        if b-a<2: continue
        out.append([a,b]); pos=b
    return out
res={}; stat={'none':0,'seg':0,'miss':0}
for bi,book in enumerate(K):
    for ci,chap in enumerate(book):
        for vi,t in enumerate(chap):
            k=f"{bi+1}-{ci+1}-{vi+1}"
            if k in QS: segs,ref=QS[k],SN[bi][ci][vi]
            elif k in QH: segs,ref=QH[k],SH[bi][ci][vi]
            else: stat['none']+=1; continue
            L=len(ref)
            # 끝의 문장부호 무시: 따옴표가 절 끝 근처에서 닫히면 끝까지로
            tail=ref.rstrip(' .,!?”’')
            segs=[[s, L if e>=len(tail) else e] for s,e in segs]
            o=krv_segs(t,segs,L,ref)
            if o: res[k]=o; stat['seg']+=1
            else: stat['miss']+=1
json.dump(res,open('bible.json','w'),separators=(',',':'))
print(stat)
