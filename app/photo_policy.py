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
ASSET_KEYS={'assetKind','directness','assignmentPolicy','reviewStatus','relation','eraLock','verseAnchors','blockedUses','approvedUses','fidelity','provenance','review','group','requireAny','allowChapters','note'}
TOP_KEYS={'schemaVersion','mode','notes','assets','groups'}
BASIS=('explicit','illustrative','interpretive')
ERAS={1:'자연·하늘',2:'족장',3:'애굽·출애굽',4:'광야·성막',5:'정착·사사',6:'왕국',7:'분열·포로',8:'시·지혜·일상',9:'복음서',10:'사도행전·서신',11:'원역사(창 1–11)'}
_BV=None
def bible_shape():
  """앱의 성경 데이터(bible.b64)로 책별 장 수·장별 절 수"""
  global _BV
  if _BV is None:
    import base64,gzip
    B=json.loads(gzip.decompress(base64.b64decode(open(R+'/bible.b64').read())).decode()); _BV=[[len(c) for c in b] for b in B]
  return _BV
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
  for k in ('verseAnchors','blockedUses','approvedUses','relation','eraLock','group','allowChapters'):
    if a.get(k): e[k]=a[k]
  rq=list(a.get('requireAny') or [])
  if a.get('group'): rq+=[w for w in (((P.get('groups') or {}).get(a['group']) or {}).get('requireAny') or []) if w not in rq]
  if rq: e['requireAny']=rq
  return e
def validate(P,ids):
  """정책 파일 검사. 오류가 하나라도 있으면 빌드가 멈춥니다(build_site.py)."""
  err=[]; BV=bible_shape(); G=P.get('groups') or {}
  for k in P:
    if k not in TOP_KEYS: err.append(f'(파일) 모르는 칸 {k}')
  def chk_rng(i,b,c1,c2,what):
    if not (isinstance(b,int) and 1<=b<=66): err.append(f'{i}: {what} 책 번호 {b}'); return
    n=len(BV[b-1])
    if not (isinstance(c1,int) and isinstance(c2,int) and 1<=c1<=c2<=n): err.append(f'{i}: {what} 장 범위 {b}:{c1}-{c2} (그 책은 {n}장)')
  def chk_rq(i,L):
    if not (isinstance(L,list) and L and all(isinstance(w,str) and w.strip() for w in L)): err.append(f'{i}: requireAny는 비지 않은 낱말 목록이어야 함')
    elif any(len(w.strip())<2 for w in L): err.append(f'{i}: requireAny에 한 글자 낱말(부분 일치 위험) {[w for w in L if len(w.strip())<2]}')
  for g,d in G.items():
    for k in d:
      if k not in ('label','requireAny','note'): err.append(f'(묶음 {g}) 모르는 칸 {k}')
    if 'requireAny' in d: chk_rq('묶음 '+g,d['requireAny'])
  for i,a in (P.get('assets') or {}).items():
    if i not in ids: err.append(f'{i}: 그림 목록에 없는 번호')
    for k in a:
      if k not in ASSET_KEYS: err.append(f'{i}: 모르는 칸 {k}')
    if 'assetKind' in a and a['assetKind'] not in KINDS: err.append(f'{i}: assetKind {a["assetKind"]}')
    if 'directness' in a and a['directness'] not in DIRS: err.append(f'{i}: directness {a["directness"]}')
    if 'assignmentPolicy' in a and a['assignmentPolicy'] not in POLS: err.append(f'{i}: assignmentPolicy {a["assignmentPolicy"]}')
    if 'relation' in a and a['relation'] not in RELS: err.append(f'{i}: relation {a["relation"]}')
    if 'reviewStatus' in a and a['reviewStatus'] not in STATS: err.append(f'{i}: reviewStatus {a["reviewStatus"]}')
    if 'eraLock' in a and not (isinstance(a['eraLock'],list) and a['eraLock'] and all(isinstance(x,int) and x in ERAS for x in a['eraLock'])): err.append(f'{i}: eraLock은 시대 번호(1–11) 목록이어야 함: {a["eraLock"]}')
    if 'group' in a and a['group'] not in G: err.append(f'{i}: 없는 묶음 {a["group"]}')
    if 'requireAny' in a: chk_rq(i,a['requireAny'])
    for c in a.get('allowChapters') or []:
      if not (isinstance(c,list) and len(c)==3): err.append(f'{i}: allowChapters 항목은 [책,시작장,끝장]'); continue
      chk_rng(i,c[0],c[1],c[2],'allowChapters')
    for v in a.get('verseAnchors') or []:
      if not all(isinstance(v.get(k),int) for k in ('book','chapter','fromVerse','toVerse')): err.append(f'{i}: verseAnchors 숫자 아님'); continue
      b,c,f,t=v['book'],v['chapter'],v['fromVerse'],v['toVerse']
      if not 1<=b<=66 or not 1<=c<=len(BV[b-1]): err.append(f'{i}: verseAnchors 없는 장 {b}:{c}'); continue
      n=BV[b-1][c-1]
      if not 1<=f<=t<=n: err.append(f'{i}: verseAnchors 절 범위 {b}:{c}:{f}-{t} (그 장은 {n}절)')
      if v.get('basis') not in (None,)+BASIS: err.append(f'{i}: verseAnchors basis {v.get("basis")}')
  return err
def app_fields(e):
  """앱(공개 JS)에 싣는 가벼운 정책: 종류·허용 범위·상태·절 근거·막는 곳. 위험 메모·출처는 싣지 않음"""
  o={'ak':e['assetKind'][:3],'ap':e['assignmentPolicy'],'rs':e['reviewStatus']}
  if e.get('verseAnchors'): o['va']=[[v['book'],v['chapter'],v['fromVerse'],v['toVerse'],{'explicit':'e','illustrative':'i','interpretive':'p'}.get(v.get('basis'),'')] for v in e['verseAnchors']]
  if e.get('blockedUses'): o['bu']=[[b['book'],b.get('chapterFrom',1),b.get('chapterTo',999)] for b in e['blockedUses']]
  if e.get('approvedUses'): o['au']=e['approvedUses']
  if e.get('relation'): o['rl']=e['relation']
  if e.get('eraLock'): o['er']=e['eraLock']
  if e.get('requireAny'): o['rq']=e['requireAny']
  if e.get('allowChapters'): o['ac']=e['allowChapters']
  if e.get('group'): o['gp']=e['group']
  return o
