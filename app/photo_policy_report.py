# 그림 정책 관측 보고(observe): 앱 배정을 바꾸지 않고, 정책을 적용하면 무엇이 걸리는지 셉니다.
# 쓰는 법: python3 photo_policy_report.py  → ux/photo_policy_report.md (build_site.py 뒤에 실행하면 site/index.html의 실제 PHOTOS도 확인)
import json,os,re,collections as C,sys
R=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,R)
import photo_policy as pp
os.chdir(R)
M=json.load(open('ux/photos_master.json')); POL=pp.load(); E={r['id']:pp.effective(r,POL) for r in M}; MR={r['id']:r for r in M}
U=json.load(open('ux/photos_use.json')) if os.path.exists('ux/photos_use.json') else {}
FULL=json.load(open('plan.json'))['full']
def label_ch(lab):
  o=[]
  for part in re.split(r'[;,·]\s*',lab):
    m=re.match(r'\s*(\S+)\s+(\d+)(?:[–-](\d+))?[장편]',part)
    if m and m.group(1) in FULL: b=FULL.index(m.group(1))+1; o.append((b,int(m.group(2)),int(m.group(3) or m.group(2))))
  return o
L=[]; P=L.append
P('# 그림 정책 관측 보고 (observe)\n')
P('앱의 그림 배정은 바꾸지 않았습니다. 사람이 정한 값은 `ux/photo_policy.json`, 나머지는 기존 role·scope에서 계산한 **제안값**입니다(확정 아님).\n')
st=C.Counter(e['reviewStatus'] for e in E.values()); P('## 1. 상태\n'); P('| 상태 | 수 |\n|---|---|'); [P(f'| {pp.STAT_KO.get(k,k)} (`{k}`) | {v} |') for k,v in st.most_common()]
hum=sum(1 for i in E if i in (POL.get('assets') or {})); P(f'\n사람이 기록한 그림 {hum}장 / 전체 {len(E)}장.\n')
act=[i for i,e in E.items() if e['reviewStatus'] not in ('hold','out')]
kd=C.Counter((E[i]['assetKind'],E[i]['directness'],E[i]['assignmentPolicy']) for i in act)
P('## 2. 쓰는 그림의 분류 (제안 포함)\n'); P('| 종류 | 결속도 | 배정 범위 | 수 |\n|---|---|---|---|'); [P(f'| {pp.KIND_KO[k]} | {d} | {a} | {v} |') for (k,d,a),v in sorted(kd.items())]
# 3. 보류·제외가 앱에 남았는가
P('\n## 3. 안전장치 확인\n')
bad=[]
if os.path.exists('site/index.html'):
  t=open('site/index.html').read(); m=re.search(r'const PHOTOS=(\[.*?\]);\n',t); ids={p['id'] for p in json.loads(m.group(1))}
  bad=[i for i,e in E.items() if e['reviewStatus'] in ('hold','out') and i in ids]
  P(f'- 앱 그림 목록(PHOTOS) {len(ids)}장 가운데 보류·제외 그림: **{len(bad)}장** {"✓" if not bad else "✗ "+", ".join(bad)}')
fixed=[]
for f in ('ux/story_cards.json','ux/story_rj.json'):
  for m in re.finditer(r'"img":\s*"(g\d\d_\d\d)"',open(f).read()):
    i=m.group(1)
    if i in E and E[i]['reviewStatus'] in ('hold','out'): fixed.append((f.split('/')[-1],i))
P(f'- 원고에 그림 번호로 고정했는데 보류·제외된 자리: **{len(fixed)}곳**' + (' — '+', '.join(f'{a}:{b}' for a,b in C.Counter(fixed)) if fixed else ' ✓'))
P('  (이 자리는 앱이 자동 선택으로 대신합니다. 바꿀 그림을 정해 고정해 주세요.)' if fixed else '')
P(f'- 정책 파일 검사: {"오류 없음 ✓" if not pp.validate(POL,set(E)) else pp.validate(POL,set(E))}')
# 4. 관측: 정책을 강하게 적용하면 걸릴 사용처
P('\n## 4. 관측: 정책을 강제하면 다시 볼 자리 (지금은 바꾸지 않음)\n')
gs=[(i,len(U[i])) for i in U if i in E and E[i]['assetKind']=='scene' and MR[i]['scope']=='g']
P(f'### 4-1. 범용 \'사람 장면\' 그림 (scope g, role scene) — {len(gs)}장, 쓰인 카드 {sum(n for _,n in gs)}곳')
P('사람이 무엇을 하는 장면이 여러 본문에 두루 쓰입니다. GPT 기준으로는 `broad`라도 인물·사건이 다른 본문에 붙으면 안 되므로, 많이 쓰인 것부터 검수합니다.\n')
P('| 그림 | 설명 | 쓰인 곳 |\n|---|---|---|'); [P(f'| {i} | {MR[i]["memo"]} | {n} |') for i,n in sorted(gs,key=lambda x:-x[1])[:40]]
POET=set(range(18,23))|set(range(23,40))|{66}
sy=[]
for i,us in U.items():
  if i in E and E[i]['assetKind']=='symbolic':
    for u in us:
      ch=label_ch(u[4])
      if ch and not any(b in POET for b,_,_ in ch): sy.append((i,u[4],u[5]))
P(f'\n### 4-2. 상징·환상 그림이 이야기 본문(시·예언·계시 밖)에 쓰인 곳 — {len(sy)}곳\n'); P('| 그림 | 설명 | 날 | 카드 |\n|---|---|---|---|'); [P(f'| {i} | {MR[i]["memo"]} | {l} | {c} |') for i,l,c in sy[:60]]
out_ref=[]
for i,us in U.items():
  r=MR.get(i)
  if not r or r['scope']!='s' or not r['refs']: continue
  for u in us:
    ch=label_ch(u[4])
    if ch and not any(b==B and not(z<a2 or a>z2) for b,a,z in ch for B,a2,z2 in r['refs']): out_ref.append((i,u[4],u[5]))
P(f'\n### 4-3. 특정 장면 그림이 자기 장 밖의 날에 쓰인 곳 (인용으로 허용된 경우 포함) — {len(out_ref)}곳\n'); P('| 그림 | 설명 | 날 | 카드 |\n|---|---|---|---|'); [P(f'| {i} | {MR[i]["memo"]} | {l} | {c} |') for i,l,c in out_ref[:60]]
unused=[i for i in act if i not in U]
P(f'\n### 4-4. 지금 어느 카드에도 쓰이지 않은 그림 — {len(unused)}장 (예비)\n')
open('ux/photo_policy_report.md','w').write('\n'.join(L)+'\n'); print('\n'.join(L[:30])); print('…', len(sy), len(out_ref), len(fixed), bad)
