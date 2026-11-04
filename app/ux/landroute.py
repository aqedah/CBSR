# 큰 여정의 육지 이동이 물 위를 지나면 물을 돌아가는 경유점을 찾음(11/4). 쓰는 법: NO_LANDPATH=1 python3 ux/big_tours.py && python3 ux/landroute.py && python3 ux/big_tours.py
import json, math, os, heapq, sys
sys.path.insert(0,'.')
from PIL import Image
R='/home/claude/rj'; T=json.load(open(f'{R}/ux/big_tours.json')); C={}
def tile(k,z,x,y):
    f=f'{R}/site/{k}/{z}/{x}/{y}.webp'
    if f not in C: C[f]=Image.open(f).convert('RGB') if os.path.exists(f) else None
    return C[f]
WC={}
def water(lat,lng):
    key=(round(lat,4),round(lng,4))
    if key in WC: return WC[key]
    v=False
    for k,z in [('terrhi',12),('terrhi',11),('terrm',10),('terrw',9)]:
        n=2**z; x=(lng+180)/360*n; r=math.radians(lat); y=(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*n
        im=tile(k,z,int(x),int(y))
        if im is None: continue
        p=im.getpixel((min(im.width-1,int((x%1)*im.width)),min(im.height-1,int((y%1)*im.height))))
        v=p[2]>p[0]+35 and p[2]>p[1]-5; break
    WC[key]=v; return v
def run_len(a,b,st=0.002,ea=True,eb=True):
    d=math.hypot(a[0]-b[0],a[1]-b[1]); n=max(2,int(d/st)); best=cur=0; m=int(0.013/st)
    for i in range(1,n):
        if (ea and i<=m) or (eb and i>=n-m): cur=0; continue
        if water(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n): cur+=1; best=max(best,cur)
        else: cur=0
    return best*st*111  # km
def clear(a,b,ea,eb): return run_len(a,b,0.0015,ea,eb)<0.6
def route(a,b):
    g=0.008; la0=min(a[0],b[0])-0.6; lo0=min(a[1],b[1])-0.6; la1=max(a[0],b[0])+0.6; lo1=max(a[1],b[1])+0.6
    H=int((la1-la0)/g)+1; W=int((lo1-lo0)/g)+1
    cell=lambda p:(int(round((p[0]-la0)/g)),int(round((p[1]-lo0)/g)))
    pos=lambda c:(la0+c[0]*g,lo0+c[1]*g)
    s=cell(a); t=cell(b); D={s:0}; P={}; Q=[(0,0,s)]
    while Q:
        f0,d,c=heapq.heappop(Q)
        if c==t: break
        if d>D.get(c,1e9): continue
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if not di and not dj: continue
                n=(c[0]+di,c[1]+dj)
                if not(0<=n[0]<H and 0<=n[1]<W): continue
                nd=d+math.hypot(di,dj*math.cos(math.radians(a[0])))*(60 if water(*pos(n)) else 1)
                if nd<D.get(n,1e9): D[n]=nd; P[n]=c; heapq.heappush(Q,(nd+math.hypot(n[0]-t[0],(n[1]-t[1])*math.cos(math.radians(a[0]))),nd,n))
    if t not in P: return None
    path=[t]
    while path[-1]!=s: path.append(P[path[-1]])
    path=[a]+[pos(c) for c in reversed(path[1:-1])]+[b]
    out=[a]; i=0
    while i<len(path)-1:
        j=len(path)-1
        while j>i+1 and not clear(path[i],path[j],i==0,j==len(path)-1): j-=1
        out.append(path[j]); i=j
    i=1
    while i<len(out)-1:
        if run_len(out[i-1],out[i+1],0.0015,i-1==0,i+1==len(out)-1)<0.6: out.pop(i)
        else: i+=1
    return [(round(p[0],3),round(p[1],3)) for p in out[1:-1]]
def pt(q): return (q[1],q[2]) if isinstance(q,list) and len(q)==3 else (q[0],q[1]) if isinstance(q,list) else None
SKIP={('exodus','바다 가운데 마른 땅'),('paul3','걸어서 앗소까지'),('paul1','마가 요한이 돌아가다'),('paul2','고린도에서 1년 6개월'),('paul3','말씀이 흥왕하다')}
res={}; rep=[]
for t in T:
    cur=pt(t['start'])
    for s in t['steps']:
        if s.get('from'): cur=pt(s['from'])
        def run(pts,land,field,sk):
            global cur
            for i,q in enumerate(pts):
                q=pt(q)
                if q is None: continue
                if land and cur and not sk and run_len(cur,q)>=1.0:
                    w=route(cur,q); key=f"{cur[0]},{cur[1]}>{q[0]},{q[1]}"
                    rep.append(f"{t['id']} '{s['t']}' {field}: {cur}->{q} 물 {run_len(cur,q):.1f}km → {w}")
                    if w: res[key]=w
                cur=q
        sk=(t['id'],s['t']) in SKIP
        if s.get('land0'): run(s['land0'],True,'land0',sk)
        run(s.get('p',[]),not s.get('sea'),'p',sk)
        if s.get('then'): run(s['then'],True,'then',sk)
        SD=s.get('side'); SD=SD if isinstance(SD,list) else [SD] if SD else []
        for sd in SD:
            if not sd.get('p'): continue
            save=cur; cur=pt(sd['from']) if sd.get('from') else cur; run(sd['p'],not sd.get('sea'),'side',sk); cur=save
print('\n'.join(rep)); json.dump(res,open(f'{R}/ux/landpath.json','w'),ensure_ascii=False,indent=0); print(len(res))
