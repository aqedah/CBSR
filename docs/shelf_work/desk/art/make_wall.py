from PIL import Image, ImageFilter
import numpy as np, random, os
D='/home/claude/cbsr/app/site_src/img/shelf/'
ROWS=[(194,612),(636,1080),(1104,1548)]
sprites=[]; meta=[]
for k in ['tor','his','poe','pro','gos','pau','gen']:
    im=Image.open(D+'press_%s.webp'%k).convert('RGB'); a=np.asarray(im).astype(float).sum(2)
    for y0,y1 in ROWS:
        band=a[y1-200:y1-40, :]
        col=band.mean(0)
        isb=col>300
        x=94; segs=[]
        while x<692:
            if isb[x]:
                s=x
                while x<692 and isb[x]: x+=1
                if x-s>60: segs.append((s,x))
            x+=1
        for s,e in segs:
            c=a[y0:y1, s+8:e-8].mean(1)
            top=None
            for i in range(len(c)-25):
                if (c[i:i+25]>330).all(): top=y0+i; break
            if top is None: continue
            # 둥근 윗머리까지: 위로 조금 더
            top=max(y0,top-14)
            if e-s>=150 or e>=690: continue
            body=a[top+20:y1-10, s+6:e-6]
            if body.size==0 or (body.mean(1)>290).mean()<.92 or body.mean()<330: continue
            if y1-top<260: continue
            meta.append((k,y0,s,e,y1-top)); sprites.append(im.crop((s-3,top-2,e+3,y1)))
print('sprites',len(sprites),[sp.size for sp in sprites[:6]])
base=Image.open(D+'press_tor.webp').convert('RGB')
tex=base.crop((94,640,480,1076)); texm=tex.transpose(Image.FLIP_LEFT_RIGHT)
board=base.crop((78,606,706,642))
def wall(rows,seed,name):
    random.seed(seed)
    im=base.copy()
    top,bot=194,1548; n=len(rows); bh=36
    rh=(bot-top+bh)//n  # row pitch incl board
    y=top
    for i,row in enumerate(rows):
        y1=top+rh*(i+1)-bh if i<n-1 else bot
        # back panel
        x=94; t=0
        while x<690:
            tt=tex if t%2==0 else texm
            w=min(tt.width,690-x); im.paste(tt.crop((0,0,w,y1-y)),(x,y)); x+=w; t+=1
        # books, groups separated by gap
        total=sum(row); gaps=len(row)-1
        avail=690-94-24-gaps*18
        hmax=(y1-y)-26; bw=min(avail/total, hmax*0.34)
        x=94+12+ (avail-bw*total)/2
        for gi,cnt in enumerate(row):
            for j in range(cnt):
                sp=random.choice(sprites)
                h=(y1-y)-random.randint(22,46)
                w=int(bw-3)
                spr=sp.resize((w,min(h,int(sp.height*w/sp.width*1.0))),Image.LANCZOS)
                im.paste(spr,(int(x+(bw-spr.width)/2),y1-spr.height))
                x+=bw
            x+=18
        if i<n-1: im.paste(board,(78,y1)); y=y1+bh
    im.save('/tmp/wall/%s.png'%name); im.save(D+'%s.webp'%name,quality=86)
wall([[8],[8],[8],[8],[7]],7,'wall_ot')
wall([[7],[7],[7],[6]],11,'wall_nt')
sh=Image.new('RGB',(60*len(sprites),220),'white')
for i,sp in enumerate(sprites):
    t=sp.resize((56,int(sp.height*56/sp.width))); sh.paste(t,(i*60,0))
sh.save('/tmp/wall/sprites.png')
