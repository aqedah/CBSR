# 지형 그림 4장(levant·sinai·israel·israelhi)을 지도 타일(z7–9, 256px, WebP)로 잘라 둡니다.
# 큰 그림 한 장을 겹쳐 올리면 휴대폰에서 확대할 때 다시 그리는 동안 흰 바탕이 비칩니다(목사님 2026-10-31). 타일은 지도 바탕과 같은 방식으로 다뤄져 그런 일이 없습니다.
import json,math,os,sys
import numpy as np,cv2
R=os.path.dirname(os.path.abspath(__file__)); DEST=sys.argv[1] if len(sys.argv)>1 else R+'/site/terrain/t'; OUT=R+'/terrain_tiles_cache'
T=json.load(open(R+'/terrain.json')); KEYS=['levant','sinai','israel','israelhi']
stamp=max(os.path.getmtime(f'{R}/terrain_{k}.jpg') for k in KEYS)
mark=OUT+'/.stamp'
import shutil
def ship():
  if os.path.abspath(DEST)!=os.path.abspath(OUT): shutil.rmtree(DEST,ignore_errors=True); shutil.copytree(OUT,DEST)
if os.path.exists(mark) and float(open(mark).read() or 0)>=stamp and os.path.exists(OUT+'/9'): ship(); sys.exit(0)
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
Z=9; W=256*2**Z
def mx(lng): return (lng+180)/360*W
def my(lat): s=math.sin(math.radians(lat)); return (0.5-math.log((1+s)/(1-s))/(4*math.pi))*W
def inv_my(y): n=math.pi-2*math.pi*y/W; return math.degrees(math.atan(math.sinh(n)))
lat0=min(T[k]['bounds'][0][0] for k in KEYS); lat1=max(T[k]['bounds'][1][0] for k in KEYS)
lng0=min(T[k]['bounds'][0][1] for k in KEYS); lng1=max(T[k]['bounds'][1][1] for k in KEYS)
x0,x1=int(mx(lng0))//256*256,(int(mx(lng1))//256+1)*256; y0,y1=int(my(lat1))//256*256,(int(my(lat0))//256+1)*256
H,Wd=y1-y0,x1-x0; acc=np.zeros((H,Wd,3),np.float32); wsum=np.zeros((H,Wd),np.float32)
ys=np.array([inv_my(y0+i+.5) for i in range(H)]); xs=(np.arange(Wd)+x0+.5)/W*360-180
for k in KEYS:
  im=cv2.imread(f'{R}/terrain_{k}.jpg'); h,w=im.shape[:2]; (a0,o0),(a1,o1)=T[k]['bounds']
  col=(xs-o0)/(o1-o0)*w-.5; row=(a1-ys)/(a1-a0)*h-.5
  mapx=np.tile(col.astype(np.float32),(H,1)); mapy=np.tile(row.astype(np.float32)[:,None],(1,Wd))
  warped=cv2.remap(im,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0)).astype(np.float32)
  fx=np.clip(np.minimum((col+.5)/(w*.08),(w-.5-col)/(w*.08)),0,1); fy=np.clip(np.minimum((row+.5)/(h*.08),(h-.5-row)/(h*.08)),0,1)
  wgt=(fy[:,None]*fx[None,:]).astype(np.float32); wgt*={'israelhi':1.6,'israel':1.0,'levant':1.0,'sinai':1.0}[k]
  acc+=warped*wgt[:,:,None]; wsum+=wgt
rgb=np.where(wsum[:,:,None]>0,acc/np.maximum(wsum,1e-6)[:,:,None],0).astype(np.uint8)
alpha=(np.clip(wsum,0,1)*0.92*255).astype(np.uint8)
mosaic=np.dstack([rgb,alpha]); n=0
for z in (9,8,7):
  s=2**(9-z); m=mosaic if s==1 else cv2.resize(mosaic,(Wd//s,H//s),interpolation=cv2.INTER_AREA); X0,Y0=x0//s,y0//s
  for ty in range(m.shape[0]//256):
    for tx in range(m.shape[1]//256):
      t=m[ty*256:(ty+1)*256,tx*256:(tx+1)*256]
      if t[:,:,3].max()<8: continue
      d=f'{OUT}/{z}/{X0//256+tx}'; os.makedirs(d,exist_ok=True); cv2.imwrite(f'{d}/{Y0//256+ty}.webp',t,[cv2.IMWRITE_WEBP_QUALITY,80]); n+=1
json.dump({"minZoom":7,"maxZoom":9,"bounds":[[lat0,lng0],[lat1,lng1]]},open(OUT+'/meta.json','w'))
open(mark,'w').write(str(stamp)); ship(); print('terrain tiles',n)
