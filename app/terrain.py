import math, os, io, json, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image, ImageDraw
frames={
 "israel":dict(lon=(33.9,36.9),lat=(29.4,33.8),z=9),
 "israelhi":dict(lon=(34.2,35.95),lat=(30.9,33.45),z=10),
 "asia":dict(lon=(21.3,31.0),lat=(36.2,41.6),z=7),
 "med":dict(lon=(11,37.8),lat=(30.3,42.6),z=6),
 "neareast":dict(lon=(24,50),lat=(21.5,40.5),z=6),
 "levant":dict(lon=(34.0,39.0),lat=(33.0,37.6),z=9),
 "sinai":dict(lon=(32.0,35.6),lat=(27.4,31.2),z=9),
}
ONLY=[x for x in os.environ.get("ONLY","").split(",") if x]
if ONLY: frames={k:v for k,v in frames.items() if k in ONLY}
def lon2x(lon,z): return (lon+180)/360*256*2**z
def lat2y(lat,z):
    r=math.radians(lat); return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*256*2**z
def tile(z,x,y):
    p=f"tiles/{z}_{x}_{y}.png"
    if not os.path.exists(p):
        urllib.request.urlretrieve(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",p)
    return p
# land polygons from world-atlas via node-converted geojson
land=json.load(open('land50.json')); land10=json.load(open('land10.json'))
out={}
for fid,f in frames.items():
    z=f['z']; x0,x1=lon2x(f['lon'][0],z),lon2x(f['lon'][1],z); y0,y1=lat2y(f['lat'][1],z),lat2y(f['lat'][0],z)
    tx0,tx1,ty0,ty1=int(x0//256),int(x1//256),int(y0//256),int(y1//256)
    jobs=[(z,x,y) for x in range(tx0,tx1+1) for y in range(ty0,ty1+1)]
    with cf.ThreadPoolExecutor(16) as ex: list(ex.map(lambda a:tile(*a),jobs))
    W=(tx1-tx0+1)*256; H=(ty1-ty0+1)*256
    mosaic=np.zeros((H,W),dtype=np.float32)
    for (zz,x,y) in jobs:
        a=np.asarray(Image.open(f"tiles/{zz}_{x}_{y}.png").convert('RGB')).astype(np.float32)
        e=a[...,0]*256+a[...,1]+a[...,2]/256-32768
        mosaic[(y-ty0)*256:(y-ty0+1)*256,(x-tx0)*256:(x-tx0+1)*256]=e
    ox,oy=int(x0-tx0*256),int(y0-ty0*256); cw,ch=int(x1-x0),int(y1-y0)
    E=mosaic[oy:oy+ch,ox:ox+cw]
    # land mask
    mask=Image.new('L',(cw,ch),0); d=ImageDraw.Draw(mask)
    src=land10 if fid in('israel','asia','israelhi','levant','sinai') else land
    for poly in src:
        for ring in poly:
            pts=[(lon2x(lo,z)-x0,lat2y(la,z)-y0) for lo,la in ring]
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            if max(xs)<0 or min(xs)>cw or max(ys)<0 or min(ys)>ch: continue
            d.polygon(pts,fill=255 if ring is poly[0] else 0)
    M=np.asarray(mask)>0
    # hillshade
    cell=40075016*math.cos(math.radians(sum(f['lat'])/2))/(256*2**z)
    gy,gx=np.gradient(E,cell)
    ex=3.0 if fid in('israel','israelhi','levant','sinai') else 6.0
    slope=np.arctan(ex*np.hypot(gx,gy)); asp=np.arctan2(-gx,gy)
    az,alt=math.radians(315),math.radians(45)
    hs=np.sin(alt)*np.cos(slope)+np.cos(alt)*np.sin(slope)*np.cos(az-asp)
    hs=np.clip(hs,0,1)
    # hypsometric colors
    stops=[(-450,(176,196,150)),(0,(196,210,166)),(200,(214,218,170)),(500,(226,214,166)),(900,(214,190,146)),(1500,(190,160,120)),(2500,(170,140,110)),(4000,(235,232,226))]
    el=np.clip(E,-450,4000); rgb=np.zeros(E.shape+(3,),np.float32)
    for i in range(len(stops)-1):
        a,ca=stops[i]; b,cb=stops[i+1]
        m=(el>=a)&(el<=b); t=((el-a)/(b-a))[m][:,None]
        rgb[m]=np.array(ca)*(1-t)+np.array(cb)*t
    shade=(0.55+0.6*hs)[...,None]
    rgb=np.clip(rgb*shade,0,255)
    sea=np.array((168,198,214),np.float32)
    rgb[~M]=sea
    img=Image.fromarray(rgb.astype(np.uint8))
    maxw={'israel':1100,'israelhi':1500,'levant':1500,'sinai':1100}.get(fid,1600)
    if img.width>maxw: img=img.resize((maxw,round(img.height*maxw/img.width)),Image.LANCZOS)
    buf=io.BytesIO(); img.save(buf,'JPEG',quality=72,optimize=True,progressive=True)
    open(f'terrain_{fid}.jpg','wb').write(buf.getvalue())
    out[fid]=dict(bounds=[[f['lat'][0],f['lon'][0]],[f['lat'][1],f['lon'][1]]],size=len(buf.getvalue()),wh=img.size)
    print(fid,img.size,len(buf.getvalue())//1024,'KB')
old=json.load(open('terrain.json')) if os.path.exists('terrain.json') else {}
old.update(out); json.dump(old,open('terrain.json','w'))
