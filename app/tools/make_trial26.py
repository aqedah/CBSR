# 체험판 작업대(site_src/trial26.html)를 2027 작업대(site_src/guide.html)에서 다시 만듭니다. (11-20)
# 두 작업대는 같은 코드이고, 체험판은 ED(판 설정·책머리 기본값)와 PLAN(317–365일 통독표) 두 줄만 다릅니다.
# guide.html을 고친 뒤: python3 tools/make_trial26.py
import json,os,sys
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site_src')
g=open(os.path.join(R,'guide.html'),encoding='utf8').read(); t=open(os.path.join(R,'trial26.html'),encoding='utf8').read()
pick=lambda s,p:[l for l in s.split('\n') if l.startswith(p)][0]
ed=pick(t,'const ED='); pre="const ED=Object.assign({key:'cbsr_guide_qt',gitkey:'cbsr_guide_git',path:'app/site_src/guide_qt.json',pub:'guide_qt.json',qlab:null,trial:false},"
assert ed.startswith(pre) and ed.endswith(');'), ed[:200]
E=json.loads(ed[len(pre):-2])
if len(sys.argv)>2 and sys.argv[1]=='--fdef':   # 체험판 책머리 기본값 고치기: --fdef 키 값
    E['fdef'][sys.argv[2]]=sys.argv[3]
n=g.replace(pick(g,'const ED='),pre+json.dumps(E,ensure_ascii=False)+');',1).replace(pick(g,'const PLAN='),pick(t,'const PLAN='),1)
open(os.path.join(R,'trial26.html'),'w',encoding='utf8').write(n); print('trial26.html', len(n))
