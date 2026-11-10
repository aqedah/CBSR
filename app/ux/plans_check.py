#!/usr/bin/env python3
# 평면도 여정 인용 검사기(2026-11-11, GPT 2차 검수 P1-4): ux/plans/*.js의 모든 q·say를 bible.b64 원문과 대조.
# 전체 일치 → OK, 원문의 일부(앞·뒤 생략) → PART(부분 인용 표시 필요), 아니면 FAIL. 종료 코드 1이면 빌드에서 막음.
import json,base64,zlib,subprocess,sys,os,glob
H=os.path.dirname(os.path.abspath(__file__)); A=os.path.dirname(H)
B=json.loads(zlib.decompress(base64.b64decode(open(os.path.join(A,'bible.b64')).read().strip()),16+zlib.MAX_WBITS).decode())
def verse(b,c,v):
    try: return B[b-1][c-1][v-1]
    except Exception: return None
JS=r'''
const fs=require('fs'); const out=[]; const esc=s=>s;
global.esc=esc; global.PLANS={}; global.planReg=sp=>{ for(const sc of sp.scenes){ for(const k of ['q','say']){ if(sc[k]) out.push({id:sp.id,s:sc.s,k,q:sc[k],r:sc.r,part:!!sc.part}); } } return sp; };
global.SPACES={}; global.spaceReg=sp=>{ for(const p of sp.places) for(const e of (p.ev||[])) out.push({id:sp.id,s:p.n,k:'ev',q:e.q,r:e.r,part:!!e.part}); return sp; };
global.document={addEventListener(){}}; global.window={};
for(const f of process.argv.slice(2)){ const src=fs.readFileSync(f,'utf8'); new Function(src.replace(/^const (PLANS|PLAN_K|SPACES)=/mg,'var $1=').replace(/^function (planReg|planCard|planHere|planOpen|spaceReg|spaceCard|spaceHere|spaceOpen)\(/mg,'global.$1=function $1(')) (); }
process.stdout.write(JSON.stringify(out));
'''
files=sorted(glob.glob(os.path.join(H,'plans','*.js')))
items=json.loads(subprocess.check_output(['node','-e',JS,*files]).decode())
norm=lambda s:' '.join(s.split())
bad=0; part=0
for it in items:
    r=it['r']; q=norm(it['q']); 
    if not r: print('NOREF',it['id'],it['s']); bad+=1; continue
    t=verse(*r)
    if t is None: print('NOVERSE',it['id'],it['s'],r); bad+=1; continue
    t=norm(t)
    if q==t: continue
    if q in t:
        part+=1
        if not it['part']: print('PART ',it['id'],it['s'],r,'| 원문 앞:',t[:len(t)-len(q)][:40] if t.endswith(q) else '(가운데)'); bad+=1
        continue
    # 여러 절 이어 붙인 경우: r절부터 이어서 확인
    joined=t
    for k in range(1,4):
        n=verse(r[0],r[1],r[2]+k)
        if not n: break
        joined=joined+' '+norm(n)
        if q==joined or q in joined: break
    if q==joined: print('MULTI',it['id'],it['s'],r,'(여러 절 — r에 끝 절 표시 권장)'); continue
    print('FAIL ',it['id'],it['s'],r); print('   q:',q[:90]); print('   원:',t[:90]); bad+=1
print(f'-- {len(items)}개 인용 검사, 문제 {bad}개 (부분 인용 {part}개)')
sys.exit(1 if bad else 0)
