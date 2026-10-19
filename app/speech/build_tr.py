# 새번역·새한글: “ ” 따옴표로 대화 구간 찾기. 여러 절·장에 걸친 대화도 이어서 처리.
import json,base64,gzip
def load(k): return json.loads(gzip.decompress(base64.b64decode(open(f'/home/claude/rj/{k}.b64').read())))
def build(k):
    B=load(k); out={}; dropped=0
    for bi,book in enumerate(B):
        depth=0
        for ci,chap in enumerate(book):
            nxt=book[ci+1] if ci+1<len(book) else []
            pend=[]   # 아직 닫히지 않은 대화가 지나간 절들
            for vi,t in enumerate(chap):
                key=f"{bi+1}-{ci+1}-{vi+1}"; segs=[]; start=0 if depth>0 else None
                for i,ch in enumerate(t):
                    if ch=='“':
                        if depth==0: start=i
                        depth+=1
                    elif ch=='”' and depth>0:
                        depth-=1
                        if depth==0: segs.append([start,i+1]); start=None; pend=[]
                if depth>0: segs.append([start,len(t)]); pend.append(key)
                if segs: out[key]=segs
            if depth>0:
                nt=" ".join(nxt); carry=nxt and nt.count('”')>nt.count('“')
                if not carry:
                    # 짝 없는 여는 따옴표: 열린 채로 지나간 절의 표시는 지웁니다(첫 절 제외)
                    for k2 in pend[1:]:
                        out[k2]=[s for s in out[k2] if not (s[0]==0 and s[1]==len(B[bi][ci][int(k2.split('-')[2])-1]))] or None
                        if out[k2] is None: del out[k2]
                        dropped+=1
                    depth=0
    return out,dropped
if __name__=='__main__':
    for k in ('bible_snb','bible_shg'):
        o,d=build(k); json.dump(o,open(f'{k}.json','w'),separators=(',',':')); print(k,len(o),'dropped',d)
