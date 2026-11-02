# 넓은 지역 지형 조각(2026-11-02, terrain_hi.py의 확장): 성경 지도 전체를 고도 원자료로.
#  terrw: 5–9배율 — 이탈리아에서 메소보다미아까지(바울·포로·출애굽 길 전체)
#  terrm: 10–11배율 — 레반트·시내 반도·애굽 하류·요단 동편(사건이 많은 곳)
# 요단·갈릴리·사해 핵심 권역은 terrhi(8–13배율)가 위에 덮음.
# 물: 해발 0.5m 아래(바다·호수). 단 바다보다 낮은 땅(요단 골짜기, 까따라 분지, 파이윰)은 빼고 그 안의 호수만 따로.
# 바다로만 된 조각은 만들지 않음(바깥 Esri 바다가 그대로 보임 — 색을 같게 맞춤).
import math, os, json, urllib.request, concurrent.futures as cf, numpy as np, sys
from PIL import Image
from scipy import ndimage
os.makedirs('tiles',exist_ok=True)
def lon2x(lon,z): return (lon+180)/360*256*2**z
def lat2y(lat,z): r=math.radians(lat); return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*256*2**z
def x2lon(x,z): return x/(256*2**z)*360-180
def y2lat(y,z): n=math.pi-2*math.pi*y/(256*2**z); return math.degrees(math.atan(math.sinh(n)))
def get(z,x,y):
    p=f"tiles/{z}_{x}_{y}.png"
    if not os.path.exists(p):
        for k in range(4):
            try: urllib.request.urlretrieve(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",p); break
            except Exception: pass
    a=np.asarray(Image.open(p).convert("RGB"),np.float32); return a[...,0]*256+a[...,1]+a[...,2]/256-32768
def dem_px(z,X0,Y0,X1,Y1):
    tx0,tx1,ty0,ty1=X0//256,(X1-1)//256,Y0//256,(Y1-1)//256
    B=np.zeros(((ty1-ty0+1)*256,(tx1-tx0+1)*256),np.float32)
    for x in range(tx0,tx1+1):
        for y in range(ty0,ty1+1): B[(y-ty0)*256:(y-ty0+1)*256,(x-tx0)*256:(x-tx0+1)*256]=get(z,x%(2**z),y)
    return B[Y0-ty0*256:Y1-ty0*256,X0-tx0*256:X1-tx0*256]
st=[(-430,(203,196,160)),(-300,(214,205,163)),(-100,(222,212,170)),(0,(224,214,172)),(200,(226,214,175)),(500,(214,198,160)),(800,(198,182,148)),(1100,(184,170,142)),(1800,(172,160,140)),(3000,(196,190,180))]
XS=[s[0] for s in st]; SEA=np.array([122,180,218]); LAKE=np.array([143,183,207])
# 바다보다 낮은 땅(물이 아님): (위도0,위도1,경도0,경도1, 그 안에서 물로 칠할 기준 높이)
LOWLAND=[(29.4,33.45,35.15,35.8,None),(28.4,30.9,25.3,29.6,None),(29.0,29.75,30.15,31.1,-42)]
def lakes_rift(E,LA,LO):
    w=np.zeros(E.shape,bool)
    w|=(E<=-393)&(LA<31.8)&(LA>30.9)&(LO>35.3)&(LO<35.62)
    w|=(E<=-384)&(LA>30.98)&(LA<31.24)&(LO>35.33)&(LO<35.6)
    w|=(E<=-208)&(LA>32.69)&(LA<32.92)&(LO>35.5)&(LO<35.67)
    w|=(((LA-33.078)/.024)**2+((LO-35.615)/.021)**2)<=1
    return w
def render(out,z,x,y,regs):
    P=24; X0,Y0=x*256-P,y*256-P; E=dem_px(z,X0,Y0,X0+256+2*P,Y0+256+2*P)
    if z<=9: E=ndimage.gaussian_filter(E,.6)
    lat=y2lat(y*256+128,z); px=156543.03*math.cos(math.radians(lat))/2**z
    gy,gx=np.gradient(E,px); ex={5:7,6:5.5,7:4.2,8:3.2,9:2.6,10:2.0,11:1.6}.get(z,1.6)
    def sh(az,alt):
        az,alt=math.radians(az),math.radians(alt); sl=np.arctan(np.hypot(gx,gy)*ex); asp=np.arctan2(-gx,gy)
        return np.clip(np.sin(alt)*np.cos(sl)+np.cos(alt)*np.sin(sl)*np.cos(az-asp),0,1)
    hs=.6*sh(315,40)+.25*sh(270,45)+.15*sh(0,50); hs=(hs-.62)*1.1+.9
    C=(np.stack([np.interp(E,XS,[s[1][k] for s in st]) for k in range(3)],-1)*hs[...,None])[P:-P,P:-P]; E=E[P:-P,P:-P]
    gxp,gyp=np.meshgrid(np.arange(256)+.5+x*256,np.arange(256)+.5+y*256)
    LO=x2lon(gxp,z); LA=np.vectorize(lambda v:y2lat(v,z))(gyp[:,0])[:,None]*np.ones((1,256))
    low=np.zeros(E.shape,bool); lakeIn=np.zeros(E.shape,bool)
    for la0,la1,lo0,lo1,th in LOWLAND:
        m=(LA>=la0)&(LA<=la1)&(LO>=lo0)&(LO<=lo1); low|=m
        if th is not None: lakeIn|=m&(E<=th)
    sea=(E<=0.5)&~low
    lake=lakes_rift(E,LA,LO)|lakeIn
    if sea.all() and not lake.any(): return 0
    sea=ndimage.binary_opening(sea,iterations=1)|ndimage.binary_erosion(sea,iterations=2,border_value=1)
    def soft(m): return np.clip(ndimage.gaussian_filter(m.astype(np.float32),.8)*1.6-.3,0,1)[...,None]
    s_=soft(sea); l_=soft(lake)
    C=C*(1-s_)+SEA*s_; C=C*(1-l_)+LAKE*l_
    A=np.zeros(E.shape)
    for (lo0,lo1,la0,la1) in regs:
        ax0,ax1=lon2x(lo0,z),lon2x(lo1,z); ay0,ay1=lat2y(la1,z),lat2y(la0,z)
        d=np.minimum(np.minimum(gxp-ax0,ax1-gxp),np.minimum(gyp-ay0,ay1-gyp)); A=np.maximum(A,np.clip(d/40,0,1))
    if A.max()<=0: return 0
    im=Image.fromarray(np.dstack([np.clip(C,0,255),A*255]).astype(np.uint8),"RGBA")
    os.makedirs(f"{out}/{z}/{x}",exist_ok=True); im.save(f"{out}/{z}/{x}/{y}.webp",quality=80,method=5); return 1
def layer(out,regs,zs):
    n=0
    for z in zs:
        J=set()
        for (lo0,lo1,la0,la1) in regs:
            for tx in range(int(lon2x(lo0,z)//256),int(lon2x(lo1,z)//256)+1):
                for ty in range(int(lat2y(la1,z)//256),int(lat2y(la0,z)//256)+1): J.add((tx,ty))
        need=set((x+dx,y+dy) for x,y in J for dx in (-1,0,1) for dy in (-1,0,1))
        with cf.ThreadPoolExecutor(32) as ex: list(ex.map(lambda a:get(z,a[0]%(2**z),a[1]),need))
        with cf.ThreadPoolExecutor(8) as ex: r=list(ex.map(lambda a:render(out,z,a[0],a[1],regs),sorted(J)))
        n+=sum(r); print(out,z,len(J),sum(r),flush=True)
    return n
# 범위: (경도0,경도1,위도0,위도1)
WIDE=[(11.5,30.5,34.0,42.2),(29.5,48.8,27.0,42.2),(25.0,29.6,29.5,32.2)]
MID=[(29.8,38.6,27.3,37.4)]
which=sys.argv[1:] or ["w","m"]
info={}
if "w" in which: layer("terrw",WIDE,range(5,10)); info["terrw"]={"regs":WIDE,"minZoom":5,"maxZoom":9}
if "m" in which: layer("terrm",MID,range(10,12)); info["terrm"]={"regs":MID,"minZoom":10,"maxZoom":11}
old=json.load(open('terrwide.json')) if os.path.exists('terrwide.json') else {}
old.update(info); json.dump(old,open('terrwide.json','w'))
