# 지형 조각 목록(2026-11-02): 만들지 않은 조각(바다만 있는 곳·범위 밖)을 앱이 요청하지 않도록 층·배율·x마다 y 구간을 적음
import os, json
out={}
for d in ['terrw','terrm','terrhi']:
    if not os.path.isdir(d): continue
    L={}
    for z in os.listdir(d):
        Z={}
        for x in os.listdir(f'{d}/{z}'):
            ys=sorted(int(f.split('.')[0]) for f in os.listdir(f'{d}/{z}/{x}'))
            R=[]
            for y in ys:
                if R and y==R[-1]+1: R[-1]=y
                else: R+= [y,y]
            Z[x]=R
        L[z]=Z
    out[d]=L
json.dump(out,open('terrindex.json','w'),separators=(',',':'))
print(os.path.getsize('terrindex.json'))
