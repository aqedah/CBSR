# 그림 라이브러리 정책 층(GPT 설계 2026-10-30): 기존 photos_master(role·scope·refs·kw·deny)는 그대로 두고,
# 사람이 정한 분류·검수·사용 정책은 ux/photo_policy.json에만 적습니다. photos_master.txt를 다시 만들어도 정책은 사라지지 않습니다.
# 정책 기록이 없는 그림은 'legacy-unclassified'(옛 분류 그대로)이고, 기존 role에서 '제안' 분류만 계산합니다(확정 아님).
import json,os
R=os.path.dirname(os.path.abspath(__file__)); PF=R+'/ux/photo_policy.json'
KINDS=('scene','background','object','symbolic','reference')
DIRS=('D1','D2','D3','D4',None)
POLS=('strict','narrow','broad','free-bg','manual-only')
RELS=('event','object-place','figurative','illustrative','ambient')
STATS=('draft','reviewed','approved','restricted','hold','out')
KIND_KO={'scene':'본문 장면','background':'풍경·장소','object':'물건·소품','symbolic':'상징·환상','reference':'연구·설명 자료'}
STAT_KO={'draft':'초안','reviewed':'검토함','approved':'승인','restricted':'제한 승인','hold':'보류','out':'제외','legacy-unclassified':'미분류'}
def load():
  if not os.path.exists(PF): return {'schemaVersion':1,'assets':{}}
  return json.load(open(PF,encoding='utf-8'))
def save(P): json.dump(P,open(PF,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def propose(r):
  """기존 role·scope에서 계산한 '제안'(사람 검수 전). GPT 1절 초기 매핑"""
  ro,sc=r.get('role'),r.get('scope')
  if ro in ('landscape',): return dict(assetKind='background',directness='D4',assignmentPolicy='free-bg')
  if ro=='setting': return dict(assetKind='background',directness='D3',assignmentPolicy='broad')
  if ro=='object': return dict(assetKind='object',directness='D3',assignmentPolicy='narrow' if sc=='s' else 'broad')
  if ro=='symbolic': return dict(assetKind='symbolic',directness='D2' if sc=='s' else 'D3',assignmentPolicy='narrow' if sc=='s' else 'broad')
  if ro=='scene': return dict(assetKind='scene',directness='D2' if sc=='s' else 'D3',assignmentPolicy='narrow' if sc=='s' else 'broad')
  return dict(assetKind='background',directness='D4',assignmentPolicy='free-bg')
def effective(r,P):
  """그림 한 장의 실제 정책: 사람이 정한 값이 있으면 그것, 없으면 제안값 + 상태 legacy-unclassified. 옛 out은 언제나 쓰지 않음"""
  a=(P.get('assets') or {}).get(r['id']) or {}; pr=propose(r)
  e={k:a.get(k,pr[k]) for k in ('assetKind','directness','assignmentPolicy')}
  e['human']=sorted(k for k in ('assetKind','directness','assignmentPolicy') if k in a)
  st=a.get('reviewStatus')
  if r.get('out'): st=st if st in ('hold','out') else ('hold' if str(r['out']).startswith('보류') else 'out')
  e['reviewStatus']=st or 'legacy-unclassified'
  for k in ('verseAnchors','blockedUses','approvedUses','relation','eraLock'):
    if a.get(k): e[k]=a[k]
  return e
def validate(P,ids):
  err=[]
  for i,a in (P.get('assets') or {}).items():
    if i not in ids: err.append(f'{i}: 그림 목록에 없는 번호')
    if 'assetKind' in a and a['assetKind'] not in KINDS: err.append(f'{i}: assetKind {a["assetKind"]}')
    if 'directness' in a and a['directness'] not in DIRS: err.append(f'{i}: directness {a["directness"]}')
    if 'assignmentPolicy' in a and a['assignmentPolicy'] not in POLS: err.append(f'{i}: assignmentPolicy {a["assignmentPolicy"]}')
    if 'relation' in a and a['relation'] not in RELS: err.append(f'{i}: relation {a["relation"]}')
    if 'reviewStatus' in a and a['reviewStatus'] not in STATS: err.append(f'{i}: reviewStatus {a["reviewStatus"]}')
    for v in a.get('verseAnchors') or []:
      if not all(isinstance(v.get(k),int) for k in ('book','chapter','fromVerse','toVerse')): err.append(f'{i}: verseAnchors 숫자 아님')
  return err
def app_fields(e):
  """앱(공개 JS)에 싣는 가벼운 정책: 종류·허용 범위·상태·절 근거·막는 곳. 위험 메모·출처는 싣지 않음"""
  o={'ak':e['assetKind'][:3],'ap':e['assignmentPolicy'],'rs':e['reviewStatus']}
  if e.get('verseAnchors'): o['va']=[[v['book'],v['chapter'],v['fromVerse'],v['toVerse']] for v in e['verseAnchors']]
  if e.get('blockedUses'): o['bu']=[[b['book'],b.get('chapterFrom',1),b.get('chapterTo',999)] for b in e['blockedUses']]
  if e.get('approvedUses'): o['au']=e['approvedUses']
  if e.get('relation'): o['rl']=e['relation']
  if e.get('eraLock'): o['er']=e['eraLock']
  return o
