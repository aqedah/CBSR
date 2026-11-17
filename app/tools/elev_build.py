"""여정 높낮이(2026-11-17 목사님: 성경지도 아이디어) — routes/all.json의 경로마다 길을 따라 고도를 재서 elev.json으로.
고도: AWS Terrain Tiles(terrarium, 공개 자료). 바다 위(0m 이하, 요단 골짜기 밖)는 null.
쓰는 법: cd app && python3 tools/elev_build.py  → elev.json (빌드가 site/로 복사)"""
import json, math, os, io, urllib.request, concurrent.futures as cf
from PIL import Image
R=json.load(open('routes/all.json'))
CACHE='/tmp/elevtiles'; os.makedirs(CACHE,exist_ok=True)
def hav(a,b):
    la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 6371*2*math.asin(math.sqrt(h))
def txy(lat,lon,z):
    n=2**z; x=(lon+180)/360*n; r=math.radians(lat); y=(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*n; return x,y
IM={}
def tile(z,x,y):
    k=(z,x,y)
    if k in IM: return IM[k]
    p=f"{CACHE}/{z}_{x}_{y}.png"
    if not os.path.exists(p):
        urllib.request.urlretrieve(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",p)
    IM[k]=Image.open(p).convert('RGB'); return IM[k]
def elev(lat,lon,z):
    x,y=txy(lat,lon,z); im=tile(z,int(x),int(y)); px=min(255,int((x%1)*256)); py=min(255,int((y%1)*256))
    r,g,b=im.getpixel((px,py)); return r*256+g+b/256-32768
def low_ok(lat,lon): return 29.5<=lat<=33.3 and 35.2<=lon<=35.75   # 요단 골짜기·사해·갈릴리 바다: 해수면 아래가 땅
out=[]; jobs=set(); plan=[]
for r in R:
    P=[(q[1],q[2],q[0]) for q in r['p']]
    if len(P)<2: plan.append(None); continue
    cum=[0]
    for i in range(1,len(P)): cum.append(cum[-1]+hav(P[i-1],P[i]))
    tot=cum[-1]
    if tot<1: plan.append(None); continue
    N=max(24,min(120,int(tot/1.5)))
    z=11 if tot<60 else 10 if tot<250 else 9 if tot<900 else 8
    S=[]
    for k in range(N+1):
        d=tot*k/N; i=1
        while i<len(cum)-1 and cum[i]<d: i+=1
        seg=cum[i]-cum[i-1]; t=0 if seg==0 else (d-cum[i-1])/seg
        la=P[i-1][0]+(P[i][0]-P[i-1][0])*t; lo=P[i-1][1]+(P[i][1]-P[i-1][1])*t; S.append((la,lo))
        x,y=txy(la,lo,z); jobs.add((z,int(x),int(y)))
    # 이름 있는 곳의 거리 위치(같은 이름 연속은 하나로)
    marks=[]
    for i,(la,lo,n) in enumerate(P):
        if n and (not marks or marks[-1][0]!=n): marks.append([n,round(cum[i]/tot,4)])
    plan.append((r,S,z,tot,marks))
print('tiles',len(jobs))
with cf.ThreadPoolExecutor(16) as ex: list(ex.map(lambda a:tile(*a),sorted(jobs)))
for it in plan:
    if not it: out.append(0); continue
    r,S,z,tot,marks=it; E=[]
    for la,lo in S:
        e=elev(la,lo,z)
        E.append(None if (e<=0 and not low_ok(la,lo)) or e<-440 else int(round(e)))
    out.append({"km":round(tot),"e":E,"m":marks})
json.dump(out,open('elev.json','w'),ensure_ascii=False,separators=(',',':'))
print('routes',sum(1 for x in out if x),'bytes',os.path.getsize('elev.json'))
