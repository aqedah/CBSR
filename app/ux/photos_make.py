import json,glob,os,re
from PIL import Image
import numpy as np
G='/home/claude/rj/site_src/img/g'
SRC={'g14':'s12','g15':'s13','g12':'s14','g13':'s15','g21':'s16','g16':'s17','g17':'s18','g18':'s19','g19':'s20'}
def parse_refs(s):
    out=[]
    for part in filter(None,s.split(';')):
        b,cs=part.split(':'); a,_,z=cs.partition('-'); out.append([int(b),int(a),int(z or a)])
    return out
rows=[]
for ln in open('master.txt',encoding='utf8'):
    if ln.startswith('#') or not ln.strip(): continue
    f=ln.rstrip('\n').split('|'); assert len(f)==13,(len(f),ln)
    id_,sc,refs,kw,tags,pl,sets,mood,fx,memo,out,deny,role=f
    rows.append(dict(id=id_,scope=sc,refs=parse_refs(refs),kw=[k for k in kw.split('/') if k],tags=tags.split(','),pl=[pl] if pl else [],sets=[int(x) for x in sets.split(',')],mood=mood,fx=f'{fx}% 50%',memo=memo,out=out.replace('뺌: ',''),deny=[x for x in deny.split('/') if x],role=role))
def crop(im):
    a=np.asarray(im.convert('L'),float); H,W=a.shape; rm=a.mean(1)
    t=0
    while t<H//4 and rm[t]<10: t+=1
    b=H-26  # 아래 오른쪽 표시 자름
    while b>H*3//4 and rm[b-1]<10: b-=1
    return im.crop((0,t,W,b))
made=0
for r in rows:
    fp=f'{G}/{r["id"]}.jpg'
    if r['out']:
        gx=fp.replace('/img/g/','/img/gx/')
        if os.path.exists(fp): os.replace(fp,gx)
        if not os.path.exists(gx):
            old='/home/claude/cbsr/img/g/'+r['id']+'.jpg'
            if os.path.exists(old): Image.open(old).save(gx,quality=80)
            elif r['id'][:3] in SRC:
                s=SRC[r['id'][:3]]; n=int(r['id'][4:]); rgb=[p for p in sorted(glob.glob(f'raw3/{s}-*.png')) if Image.open(p).mode=='RGB']
                im=crop(Image.open(rgb[n-1]).convert('RGB')); im=im.resize((960,round(im.height*960/im.width))); im.save(gx,quality=75)
        continue
    if not os.path.exists(fp):
        if r['id']=='g11_04': Image.open('redo/g11_04.jpg').save(fp,quality=82)
        else:
            s=SRC[r['id'][:3]]; n=int(r['id'][4:])
            rgb=[p for p in sorted(glob.glob(f'raw3/{s}-*.png')) if Image.open(p).mode=='RGB']
            im=crop(Image.open(rgb[n-1]).convert('RGB'))
            if im.width>1280: im=im.resize((1280,round(im.height*1280/im.width)),Image.LANCZOS)
            im.save(fp,quality=80,optimize=True); made+=1
    w,h=Image.open(fp).size
    r.update(u=f'img/g/{r["id"]}.jpg',w=w,h=h,set=r['sets'][0])
P=[{k:r[k] for k in ('id','u','w','h','tags','pl','mood','fx','set','sets','scope','refs','kw','memo','deny','role')} for r in rows if not r['out']]
json.dump(P,open('/home/claude/rj/ux/photos.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(rows,open('master.json','w'),ensure_ascii=False); json.dump(rows,open('/home/claude/rj/ux/photos_master.json','w'),ensure_ascii=False)
print('made',made,'photos',len(P),'out',sum(1 for r in rows if r['out']), 'files',len(os.listdir(G)))
