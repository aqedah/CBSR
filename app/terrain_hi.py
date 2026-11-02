# 자세한 지형 조각(목사님 2026-11-02 승인, GPT 지도 제안 검토): 고도 원자료(AWS Terrarium)에서 배율마다 직접 만든 조각.
# 바탕색(낮은 채도 흙색) + 산 음영 + 물(성경 시대 보정: 사해는 물이 줄기 전 해발 -393m 아래, 갈릴리 바다는 -208m 아래).
# 강은 조각에 그리지 않고 앱에서 벡터로(ux/rivers.json) — 배율이 바뀌어도 같은 굵기.
# 가장자리는 48화소에 걸쳐 투명하게 → 바깥의 Esri 바탕과 이어짐. 출력: terrhi/{z}/{x}/{y}.webp, terrhi.json(범위)
import math, os, json, urllib.request, concurrent.futures as cf, numpy as np, sys
from PIL import Image
from scipy import ndimage
REG=dict(lon=(34.85,35.85),lat=(30.80,33.35)); ZS=range(8,14)
os.makedirs('tiles',exist_ok=True)
def lon2x(lon,z): return (lon+180)/360*256*2**z
def lat2y(lat,z): r=math.radians(lat); return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*256*2**z
def y2lat(y,z): n=math.pi-2*math.pi*y/(256*2**z); return math.degrees(math.atan(math.sinh(n)))
def get(z,x,y):
    p=f"tiles/{z}_{x}_{y}.png"
    if not os.path.exists(p):
        for k in range(3):
            try: urllib.request.urlretrieve(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",p); break
            except Exception as e: err=e
    a=np.asarray(Image.open(p).convert("RGB"),np.float32); return a[...,0]*256+a[...,1]+a[...,2]/256-32768
def fetch(z,xs,ys):
    J=[(z,x,y) for x in xs for y in ys]
    with cf.ThreadPoolExecutor(24) as ex: list(ex.map(lambda a:get(*a),J))
def dem_px(z,X0,Y0,X1,Y1):
    tx0,tx1,ty0,ty1=X0//256,(X1-1)//256,Y0//256,(Y1-1)//256
    B=np.zeros(((ty1-ty0+1)*256,(tx1-tx0+1)*256),np.float32)
    for x in range(tx0,tx1+1):
        for y in range(ty0,ty1+1): B[(y-ty0)*256:(y-ty0+1)*256,(x-tx0)*256:(x-tx0+1)*256]=get(z,x,y)
    return B[Y0-ty0*256:Y1-ty0*256,X0-tx0*256:X1-tx0*256]
# 물 마스크(12배율, 성분 연결로)
MZ=12; mx0,mx1=int(lon2x(REG['lon'][0],MZ)),int(lon2x(REG['lon'][1],MZ)); my0,my1=int(lat2y(REG['lat'][1],MZ)),int(lat2y(REG['lat'][0],MZ))
fetch(MZ,range(mx0//256,(mx1-1)//256+1),range(my0//256,(my1-1)//256+1))
EM=dem_px(MZ,mx0,my0,mx1,my1)
def comp(th,lat,lon):
    low=EM<=th; lab,_=ndimage.label(low); sy,sx=int(lat2y(lat,MZ))-my0,int(lon2x(lon,MZ))-mx0
    w=lab==lab[sy,sx]; w=ndimage.binary_opening(w,iterations=3); w=ndimage.binary_fill_holes(w); l2,_=ndimage.label(w); return l2==l2[sy,sx]
# 사해 남쪽 분지: 지금은 증발 염전(둑으로 막아 -385~-391m)이라 북쪽 기준으로는 빠짐 → 남쪽은 -384m 아래를 따로(위도 30.98–31.24 안에서만)
def comp_box(th,lat,lon,la0,la1,lo0,lo1):
    G=np.zeros_like(EM,bool); Y=lambda la:int(lat2y(la,MZ))-my0; X=lambda lo:int(lon2x(lo,MZ))-mx0
    G[Y(la1):Y(la0),X(lo0):X(lo1)]=True; low=(EM<=th)&G; lab,_=ndimage.label(low); sy,sx=Y(lat),X(lon)
    w=lab==lab[sy,sx]; w=ndimage.binary_opening(w,iterations=3); w=ndimage.binary_fill_holes(w); l2,_=ndimage.label(w); return l2==l2[sy,sx]
WM=(comp(-393,31.5,35.48)|comp_box(-384,31.12,35.46,30.98,31.24,35.33,35.6)|comp(-208,32.82,35.59)).astype(np.float32)
WM=ndimage.binary_closing(WM>0,iterations=4).astype(np.float32)
# 지중해: 해발 0m 아래이면서 바다 쪽 점과 이어진 곳(요단 골짜기는 0m 아래여도 이어지지 않음). 색은 바깥 Esri 바다와 같게
SEA=comp(0.5,32.6,34.86).astype(np.float32); SEA=ndimage.gaussian_filter(SEA,1.0)
# 훌레 호수(1950년대에 말려 없어짐): 옛 지도의 호수 자리(남북 약 5km, 동서 약 4km)를 타원으로 되살림 — 자리는 추정
HY,HX=np.mgrid[0:EM.shape[0],0:EM.shape[1]]
hy,hx=lat2y(33.078,MZ)-my0,lon2x(35.615,MZ)-mx0; ry=(lat2y(33.054,MZ)-lat2y(33.102,MZ))/2; rx=(lon2x(35.636,MZ)-lon2x(35.594,MZ))/2
WM=np.maximum(WM,(((HY-hy)/ry)**2+((HX-hx)/rx)**2<=1).astype(np.float32))
WM=ndimage.gaussian_filter(WM,1.0)
st=[(-430,(203,196,160)),(-300,(214,205,163)),(-100,(222,212,170)),(200,(226,214,175)),(500,(214,198,160)),(800,(198,182,148)),(1100,(184,170,142)),(2000,(176,166,146))]
xs=[s[0] for s in st]
def render(z,x,y):
    P=40; X0,Y0=x*256-P,y*256-P; E=dem_px(z,X0,Y0,X0+256+2*P,Y0+256+2*P)
    if z<=9: E=ndimage.gaussian_filter(E,.6)
    lat=y2lat(y*256+128,z); px=156543.03*math.cos(math.radians(lat))/2**z
    gy,gx=np.gradient(E,px); ex=1.6 if z>=11 else 2.0 if z==10 else 2.6
    def sh(az,alt):
        az,alt=math.radians(az),math.radians(alt); sl=np.arctan(np.hypot(gx,gy)*ex); asp=np.arctan2(-gx,gy)
        return np.clip(np.sin(alt)*np.cos(sl)+np.cos(alt)*np.sin(sl)*np.cos(az-asp),0,1)
    hs=.6*sh(315,40)+.25*sh(270,45)+.15*sh(0,50); hs=(hs-.62)*1.1+.9
    C=np.stack([np.interp(E,xs,[s[1][k] for s in st]) for k in range(3)],-1)*hs[...,None]
    C=C[P:-P,P:-P]
    # 물: 12배율 마스크를 이 배율 화소 자리에서 읽음
    gx_,gy_=np.meshgrid(np.arange(256)+.5+x*256,np.arange(256)+.5+y*256); f=2.0**(MZ-z)
    w=ndimage.map_coordinates(WM,[gy_*f-my0,gx_*f-mx0],order=1,mode='constant',cval=0)
    if z<MZ: w=ndimage.zoom(ndimage.zoom(w,1),1)
    wa=np.clip((w-.35)/.3,0,1)[...,None]; edge=np.clip(1-abs(w-.5)/.12,0,1)[...,None]*.0
    C=C*(1-wa)+np.array([143,183,207])*wa
    sw=ndimage.map_coordinates(SEA,[gy_*f-my0,gx_*f-mx0],order=1,mode='constant',cval=0); sa=np.clip((sw-.35)/.3,0,1)[...,None]
    C=C*(1-sa)+np.array([122,180,218])*sa
    # 물가 선(살짝 짙게)
    e2=np.clip(1-abs(w-.5)/.15,0,1)[...,None]; C=C*(1-e2*.45)+np.array([95,143,174])*e2*.45
    # 가장자리 투명
    ax0,ax1=lon2x(REG['lon'][0],z),lon2x(REG['lon'][1],z); ay0,ay1=lat2y(REG['lat'][1],z),lat2y(REG['lat'][0],z)
    d=np.minimum(np.minimum(gx_-ax0,ax1-gx_),np.minimum(gy_-ay0,ay1-gy_)); A=np.clip(d/48,0,1)*255
    if A.max()<=0: return None
    im=Image.fromarray(np.dstack([np.clip(C,0,255),A]).astype(np.uint8),"RGBA")
    os.makedirs(f"terrhi/{z}/{x}",exist_ok=True); im.save(f"terrhi/{z}/{x}/{y}.webp",quality=82,method=5); return 1
n=0
for z in ZS:
    tx0,tx1=int(lon2x(REG['lon'][0],z)//256),int(lon2x(REG['lon'][1],z)//256); ty0,ty1=int(lat2y(REG['lat'][1],z)//256),int(lat2y(REG['lat'][0],z)//256)
    fetch(z,range(tx0-1,tx1+2),range(ty0-1,ty1+2))
    J=[(z,x,y) for x in range(tx0,tx1+1) for y in range(ty0,ty1+1)]
    with cf.ThreadPoolExecutor(8) as ex: r=list(ex.map(lambda a:render(*a),J))
    n+=sum(1 for v in r if v); print(z,len(J),flush=True)
json.dump({"bounds":[[REG['lat'][0],REG['lon'][0]],[REG['lat'][1],REG['lon'][1]]],"minZoom":min(ZS),"maxZoom":max(ZS)},open('terrhi.json','w'))
print("tiles",n)
