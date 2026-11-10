#!/usr/bin/env python3
# 평면도 여정·공간 탐색 인용 검사기(2026-11-11, GPT 3차 검수 P0 반영)
#  - ux/plans/*.js의 모든 q·say·공간 탐색 사건 인용을 bible.b64 원문과 대조
#  - 전체 일치 → OK / 원문의 일부 → part(pre|mid|post)가 실제 생략 자리와 맞아야 통과 / 그 밖에는 FAIL
#  - re(끝 절)가 있으면 r..re를 이어 붙인 원문과 대조(장을 넘기지 않음)
#  - 수집 범위 자체를 검사: 파일마다 등록된 여정·사건 수와 원본 글자 수(q:"/say:"/E( 수)를 대조해 한 건이라도 빠지면 실패
import json,base64,zlib,subprocess,sys,os,glob,re
H=os.path.dirname(os.path.abspath(__file__)); A=os.path.dirname(H)
B=json.loads(zlib.decompress(base64.b64decode(open(os.path.join(A,'bible.b64')).read().strip()),16+zlib.MAX_WBITS).decode())
def verse(b,c,v):
    try: return B[b-1][c-1][v-1]
    except Exception: return None
JS=r"""
const fs=require('fs'); const out=[]; const esc=s=>s; let cur='';
global.esc=esc; global.PLANS={}; global.SPACES={}; global.document={addEventListener(){}}; global.window={};
const reg=sp=>{ for(const sc of sp.scenes){ for(const k of ['q','say']){ if(sc[k]) out.push({f:cur,id:sp.id,s:sc.s,k,q:sc[k],r:sc.r,re:sc.re||null,part:sc.part||null}); } } return sp; };
const sreg=sp=>{ for(const p of sp.places) for(const e of (p.ev||[])) out.push({f:cur,id:sp.id,s:p.n+' · '+e.t,k:'ev',q:e.q,r:e.r,re:e.re||null,part:e.part||null}); return sp; };
Object.defineProperty(global,'planReg',{get:()=>reg,set(){}}); Object.defineProperty(global,'spaceReg',{get:()=>sreg,set(){}});
for(const f of process.argv.slice(1)){ cur=f; let src=fs.readFileSync(f,'utf8');
  /* 파일 안의 같은 이름 정의가 수집 함수를 덮지 못하게 이름을 바꿈 */
  src=src.replace(/^const (PLANS|PLAN_K|SPACES)=/mg,'var $1_=').replace(/\bfunction (planReg|spaceReg)\(/g,'function $1_orig(').replace(/^function (planCard|planHere|planOpen|spaceCard|spaceHere|spaceOpen)\(/mg,'var $1=function(');
  new Function(src)(); }
process.stdout.write(JSON.stringify(out));
"""
files=sorted(glob.glob(os.path.join(H,'plans','*.js')))
items=json.loads(subprocess.check_output(['node','-e',JS,*files]).decode())
norm=lambda s:' '.join(s.split())
bad=0; part=0
# 1) 수집 범위: 원본의 q:"·say:"·E( 수와 수집 수 대조
for f in files:
    src=open(f,encoding='utf-8').read()
    # 장면({s:"…") 하나에 인용 하나, 공간 탐색 사건(E(")) 하나에 인용 하나. 인용 없는 장면은 noq:1 로 밝혀야 함
    exp=len(re.findall(r'\{s:"',src))+len(re.findall(r'^\s+(?:SUP|CROSS_DARK|BURIAL)\(',src,re.M))-len(re.findall(r'noq:1',src))+len(re.findall(r'\bE\("',src))
    got=sum(1 for it in items if it['f']==f)
    print(f'{os.path.basename(f)}: 원본 {exp} · 수집 {got}')
    if exp!=got: print(f'  !! 수집 누락 — {exp-got}개'); bad+=1
# 2) 인용 대조
for it in items:
    r=it['r']; q=norm(it['q'])
    if not r: print('NOREF',it['id'],it['s']); bad+=1; continue
    t=verse(*r)
    if t is None: print('NOVERSE',it['id'],it['s'],r); bad+=1; continue
    if it['re']:
        vs=[verse(r[0],r[1],v) for v in range(r[2],it['re']+1)]
        if any(x is None for x in vs): print('NOVERSE(re)',it['id'],it['s'],r,it['re']); bad+=1; continue
        t=' '.join(vs)
    t=norm(t)
    if q==t:
        if it['part']: print('PART? 전체 일치인데 part 표시',it['id'],it['s'],r); bad+=1
        continue
    i=t.find(q)
    if i>=0:
        part+=1
        want='mid' if (i>0 and i+len(q)<len(t)) else 'pre' if i>0 else 'post'
        if it['part']!=want: print(f'PART {it["id"]} {it["s"]} {r} | 표시 {it["part"]} → 맞는 값 {want}'); bad+=1
        continue
    # re 없이 여러 절을 이어 쓴 경우 안내
    j=t
    for k in range(1,4):
        n=verse(r[0],r[1],r[2]+k)
        if not n: break
        j=norm(j+' '+n)
        if q==j or q in j: print(f'MULTI {it["id"]} {it["s"]} {r}: 여러 절 — re:{r[2]+k} 를 적을 것'); bad+=1; break
    else:
        print('FAIL ',it['id'],it['s'],r); print('   q:',q[:90]); print('   원:',t[:90]); bad+=1
print(f'-- {len(items)}개 인용 검사, 문제 {bad}개 (부분 인용 {part}개)')
sys.exit(1 if bad else 0)
