#!/usr/bin/env python3
"""평면도 여정·공간 탐색 인용 검사기 (2026-11-11, GPT 4차 검수 반영)

무엇을 검사하나
 - ux/plans/*.js 의 모든 장면(scene)과 공간 탐색 사건(event)을 node로 실제 등록해 모읍니다.
 - 장면마다 q(인용) 또는 say(인물의 말) 가운데 **정확히 하나**가 있어야 합니다. 둘 다 있으면 중복, 둘 다 없으면 누락.
   인용이 필요 없는 장면은 noq:1 로 밝혀야 통과합니다. 공간 탐색 사건은 q와 r이 반드시 있어야 합니다.
 - 인용은 개역개정 원문(bible.b64)과 '공백 정규화 뒤' 글자 그대로 일치해야 합니다.
   원문의 일부만 인용하면 part 가 생략 자리에 맞게 pre/mid/post 여야 하고, 전체 일치인데 part 가 있으면 실패.
   여러 절을 이어 인용하면 re(끝 절)가 있어야 하며, re 는 r 보다 크고 그 장 안에 있어야 하고 인용이 끝 절의 내용을 담아야 합니다.
 - r(책,장,절)은 양의 정수이고 실제 범위 안이어야 합니다.
 - 수집 범위: 파일마다 원본의 장면 수(+사건 수)와 수집 수를 대조해 하나라도 다르면 실패.
 - 자기 시험: 올바른 자료를 일부러 망가뜨린 9가지(T1–T9)로 검사기 자신이 제대로 실패·통과하는지 확인. 하나라도 어긋나면 실패.
종료 코드 1이면 build_site.py 가 빌드를 멈춥니다.
"""
import json,base64,zlib,subprocess,sys,os,glob,re,copy
H=os.path.dirname(os.path.abspath(__file__)); A=os.path.dirname(H)
B=json.loads(zlib.decompress(base64.b64decode(open(os.path.join(A,'bible.b64')).read().strip()),16+zlib.MAX_WBITS).decode())
def verse(b,c,v):
    """책·장·절이 모두 1 이상의 정수이고 범위 안일 때만 본문, 아니면 None (음수 인덱스 금지)"""
    if not all(isinstance(x,int) and x>=1 for x in (b,c,v)): return None
    if b>len(B) or c>len(B[b-1]) or v>len(B[b-1][c-1]): return None
    return B[b-1][c-1][v-1]
def nverses(b,c):
    try: return len(B[b-1][c-1])
    except Exception: return 0
norm=lambda s:' '.join((s or '').split())

JS=r"""
const fs=require('fs'); const out=[]; let cur='';
global.esc=s=>s; global.PLANS={}; global.SPACES={}; global.document={addEventListener(){}}; global.window={};
const reg=sp=>{ for(const sc of sp.scenes) out.push({f:cur,id:sp.id,s:sc.s,kind:'scene',q:sc.q||null,say:sc.say||null,noq:!!sc.noq,r:sc.r||null,re:sc.re||null,part:sc.part||null}); return sp; };
const sreg=sp=>{ for(const p of sp.places) for(const e of (p.ev||[])) out.push({f:cur,id:sp.id,s:p.n+' · '+e.t,kind:'ev',q:e.q||null,say:null,noq:false,r:e.r||null,re:e.re||null,part:e.part||null}); return sp; };
Object.defineProperty(global,'planReg',{get:()=>reg,set(){}}); Object.defineProperty(global,'spaceReg',{get:()=>sreg,set(){}});
for(const f of process.argv.slice(1)){ cur=f; let src=fs.readFileSync(f,'utf8');
  src=src.replace(/^const (PLANS|PLAN_K|SPACES)=/mg,'var $1_=').replace(/\bfunction (planReg|spaceReg)\(/g,'function $1_orig(').replace(/^function (planCard|planHere|planOpen|spaceCard|spaceHere|spaceOpen)\(/mg,'var $1=function(');
  new Function(src)(); }
process.stdout.write(JSON.stringify(out));
"""

def collect(files):
    return json.loads(subprocess.check_output(['node','-e',JS,*files]).decode())

def source_count(src):
    """원본 글에서 장면 수(+사건 수)를 셈: {s:" 직접 쓴 장면 + SUP/CROSS_DARK/BURIAL 도우미 호출 + E(" 사건"""
    return len(re.findall(r'\{s:"',src))+len(re.findall(r'^\s+(?:SUP|CROSS_DARK|BURIAL)\(',src,re.M))+len(re.findall(r'\bE\("',src))

def check_item(it):
    """한 장면/사건을 검사해 문제 글귀 목록을 돌려줌(비어 있으면 통과)"""
    E=[]; where=f'{it["id"]} {it["s"]}'
    q,say=it['q'],it['say']
    if it['kind']=='scene':
        if q and say: E.append(f'중복: q와 say가 둘 다 있음 — {where}'); return E
        if not q and not say:
            if it['noq']: return E
            E.append(f'누락: q도 say도 없음(인용 없는 장면이면 noq:1) — {where}'); return E
        if it['noq']: E.append(f'noq인데 인용이 있음 — {where}'); return E
    else:
        if not q: E.append(f'사건에 q 없음 — {where}'); return E
    text=norm(q or say); r=it['r']
    if not (isinstance(r,list) and len(r)==3): E.append(f'r 없음/모양 틀림 — {where}'); return E
    t=verse(*r)
    if t is None: E.append(f'r 범위 밖 {r} — {where}'); return E
    re_=it['re']
    if re_ is not None:
        if not (isinstance(re_,int) and re_>r[2]): E.append(f're({re_})는 r의 절({r[2]})보다 커야 함 — {where}'); return E
        if re_>nverses(r[0],r[1]): E.append(f're({re_})가 장의 마지막 절({nverses(r[0],r[1])})을 넘음 — {where}'); return E
        last=norm(verse(r[0],r[1],re_))
        t=norm(' '.join(verse(r[0],r[1],v) for v in range(r[2],re_+1)))
        # 인용이 끝 절의 내용을 담아야 함(끝 절 앞 12자 이상이 인용 안에 있어야)
        if last[:12] not in text: E.append(f're({re_}) 절의 내용이 인용에 없음 — {where}'); return E
    t=norm(t)
    if text==t:
        if it['part']: E.append(f'전체 일치인데 part 표시 — {where}')
        return E
    i=t.find(text)
    if i>=0:
        want='mid' if (i>0 and i+len(text)<len(t)) else ('pre' if i>0 else 'post')
        if it['part']!=want: E.append(f'부분 인용 표시 틀림: {it["part"]} → {want} — {where}')
        return E
    # re 없이 여러 절을 이은 경우를 안내(어쨌든 실패)
    j=t
    for k in range(1,4):
        n=verse(r[0],r[1],r[2]+k)
        if n is None: break
        j=norm(j+' '+n)
        if text==j or text in j: E.append(f'여러 절 인용인데 re 없음(re:{r[2]+k}) — {where}'); return E
    E.append(f'원문과 다름 — {where} | q: {text[:60]} | 원: {t[:60]}')
    return E

def run(files,quiet=False):
    items=collect(files); errs=[]
    for f in files:
        exp=source_count(open(f,encoding='utf-8').read()); got=sum(1 for it in items if it['f']==f)
        if not quiet: print(f'{os.path.basename(f)}: 원본 장면 {exp} · 수집 {got}')
        if exp!=got: errs.append(f'수집 누락: {os.path.basename(f)} 원본 {exp} ≠ 수집 {got}')
    for it in items: errs+=check_item(it)
    return items,errs

def selftest(items):
    """올바른 자료를 일부러 망가뜨려 검사기가 실패하는지(T1–T8), 그대로면 통과하는지(T9)"""
    good=[it for it in items if not check_item(it)]
    def pick(pred):
        for it in good:
            if pred(it): return copy.deepcopy(it)
        return None
    T={}
    # T1 장 마지막 절의 q를 틀리게(다음 절이 없어 for…else 결함이 나던 자리)
    it=pick(lambda x:x['kind']=='scene' and x['q'] and x['re'] is None and x['r'][2]==nverses(x['r'][0],x['r'][1])) or pick(lambda x:x['kind']=='scene' and x['q'] and x['re'] is None)
    it['r']=[it['r'][0],it['r'][1],nverses(it['r'][0],it['r'][1])]; it['q']='이것은 성경에 없는 문장입니다'; it['part']=None; T['T1 마지막 절의 틀린 인용']=bool(check_item(it))
    it=pick(lambda x:x['kind']=='scene' and x['q']); it['say']='아무 말'; T['T2 q와 say 둘 다']=bool(check_item(it))
    it=pick(lambda x:x['kind']=='scene' and x['q']); it['q']=None; T['T3 인용 삭제']=bool(check_item(it))
    it=pick(lambda x:x['part']=='pre') or pick(lambda x:x['part']=='mid'); it['part']='post'; T['T4 part 자리 틀림']=bool(check_item(it))
    it=pick(lambda x:x['q'] and not x['part']); it['part']='pre'; T['T5 전체 일치에 part']=bool(check_item(it))
    it=pick(lambda x:x['kind']=='scene' and x['q'] and not x['part'] and x['re'] is None and verse(x['r'][0],x['r'][1],x['r'][2]+1)); it['q']=it['q']+' '+verse(it['r'][0],it['r'][1],it['r'][2]+1); T['T6 두 절 인용에 re 없음']=bool(check_item(it))
    it=pick(lambda x:x['kind']=='scene' and x['q'] and not x['part'] and x['re'] is None and verse(x['r'][0],x['r'][1],x['r'][2]+2)); it['q']=it['q']+' '+verse(it['r'][0],it['r'][1],it['r'][2]+1); it['re']=it['r'][2]+2; T['T7 실제와 다른 re']=bool(check_item(it))
    it=pick(lambda x:x['q']); it['r']=[it['r'][0],it['r'][1],0]; T['T8 r에 0']=bool(check_item(it))
    T['T9 올바른 자료 통과']=all(not check_item(x) for x in good) and len(good)==len(items)
    return T

if __name__=='__main__':
    files=sorted(glob.glob(os.path.join(H,'plans','*.js')))
    items,errs=run(files)
    for e in errs: print('  !!',e)
    T=selftest(items); fails=[k for k,v in T.items() if not v]
    print('자기 시험:',' · '.join(f'{k} {"✓" if v else "✗"}' for k,v in T.items()))
    npart=sum(1 for it in items if it['part'])
    print(f'-- 장면·사건 {len(items)}개, 문제 {len(errs)}개 (부분 인용 {npart}개), 자기 시험 실패 {len(fails)}개')
    sys.exit(1 if (errs or fails) else 0)
