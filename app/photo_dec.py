# 그림 목록(웹)에서 관리자가 정한 보관·삭제·되살리기를 원본(ux/photos_master.txt)과 그림 파일에 반영하고 photos.json을 다시 만듭니다.
# deploy.sh가 빌드 전에 부릅니다. 인터넷이 안 되면 그냥 넘어갑니다.
import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
R=os.path.dirname(os.path.abspath(__file__)); M=R+'/ux/photos_master.txt'; G=R+'/site_src/img/'
try:
  import fetch_photo_dec; dec=fetch_photo_dec.get()
except Exception as e:
  print('그림 결정 읽기 실패(넘어감):',e); dec={}
L=open(M).read().split('\n'); out=[]; log=[]
for l in L:
  f=l.split('|')
  if len(f)==13 and not l.startswith('#') and f[0] in dec:
    a=dec[f[0]]
    if a=='del':
      for d in ('g/','gx/'):
        p=G+d+f[0]+'.jpg'
        if os.path.exists(p): os.remove(p)
      log.append(f[0]+' 삭제'); continue
    if a=='keep' and not f[10]:
      f[10]='뺌: 목사님이 빼서 보관'; s=G+'g/'+f[0]+'.jpg'
      if os.path.exists(s): os.replace(s,G+'gx/'+f[0]+'.jpg')
      log.append(f[0]+' 보관')
    if a=='back' and f[10]:
      f[10]=''; s=G+'gx/'+f[0]+'.jpg'
      if os.path.exists(s): os.replace(s,G+'g/'+f[0]+'.jpg')
      log.append(f[0]+' 되살림')
    l='|'.join(f)
  out.append(l)
open(M,'w').write('\n'.join(out))
if log: print('그림 반영:',', '.join(log))
def refs(s):
  o=[]
  for part in filter(None,s.split(';')):
    b,cs=part.split(':'); a,_,z=cs.partition('-'); o.append([int(b),int(a),int(z or a)])
  return o
rows=[]
for l in out:
  if l.startswith('#') or not l.strip(): continue
  id_,sc,rf,kw,tags,pl,sets,mood,fx,memo,o,deny,role=l.split('|')
  r=dict(id=id_,scope=sc,refs=refs(rf),kw=[k for k in kw.split('/') if k],tags=tags.split(','),pl=[pl] if pl else [],sets=[int(x) for x in sets.split(',')],mood=mood,fx=f'{fx}% 50%',memo=memo,out=o.replace('뺌: ',''),deny=[x for x in deny.split('/') if x],role=role)
  if not r['out']:
    fp=G+'g/'+id_+'.jpg'
    if not os.path.exists(fp): r['out']='그림 파일 없음'
    else:
      w,h=Image.open(fp).size; r.update(u=f'img/g/{id_}.jpg',w=w,h=h,set=r['sets'][0])
  rows.append(r)
P=[{k:r[k] for k in ('id','u','w','h','tags','pl','mood','fx','set','sets','scope','refs','kw','memo','deny','role')} for r in rows if not r['out']]
json.dump(P,open(R+'/ux/photos.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(rows,open(R+'/ux/photos_master.json','w'),ensure_ascii=False)
