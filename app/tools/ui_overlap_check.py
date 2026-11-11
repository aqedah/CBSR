#!/usr/bin/env python3
"""여정 화면 겹침 검사기 (2026-11-12, 여정 화면 통일안 4단계)

평면도 여정(ux/plans/*.js)의 모든 장면과 대속죄일을 휴대폰 크기 두 가지로 열어,
장면이 시작되고 몇 초 뒤의 화면에서 다음 겹침을 찾습니다.
  A 이름표끼리 겹침(인물·장소 알약)            — 있어서는 안 됨
  B 이름표가 아래 카드 밑에 가림               — 있어서는 안 됨
  C 말풍선이 위 말씀 카드·아래 카드와 겹침      — 있어서는 안 됨
  D 안내 띠가 말풍선·인물 이름표와 겹침         — 있어서는 안 됨
  E 인물 이름표가 위 말씀 카드 밑에 가림        — 알림(말씀 카드는 읽는 동안만 떠 있음)
쓰는 법: (app/site 를 http://localhost:8931 로 띄운 뒤) python3 tools/ui_overlap_check.py [360x740,412x860]
GitHub Actions에는 브라우저가 없으므로 빌드에 넣지 않고, 화면을 고친 뒤 손으로 돌립니다.
"""
import asyncio,sys,json
from playwright.async_api import async_playwright
SIZES=[tuple(map(int,s.split('x'))) for s in (sys.argv[1] if len(sys.argv)>1 else '360x740,412x860').split(',')]
URL='http://localhost:8931/index.html'
MEASURE=r"""(()=>{ const el=document.querySelector('.atn'); if(!el) return null; const R=e=>{ const r=e.getBoundingClientRect(); return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}; };
 const vis=e=>{ for(let n=e;n&&n!==el;n=n.parentNode){ if(n.nodeType!==1) continue; if(n.classList&&n.classList.contains('hid')) return false; const o=n.getAttribute&&n.getAttribute('opacity'); if(o!=null&&+o===0) return false; const cs=getComputedStyle(n); if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<0.05) return false; } return true; };
 const pills=[...el.querySelectorAll('g.jp')].filter(vis).map(g=>({k:g.classList.contains('who')?'who':'place',n:g.textContent.trim(),...R(g)})).filter(p=>p.w>0);
 const card=el.querySelector('.bmtp'), cr=card?R(card):null; const cardTop=cr?cr.t+46:1e9; /* 아래 카드의 위 46px는 흐려지는 띠 */
 const nar=[...el.querySelectorAll(':scope>.mvnar.on')].map(R); const bub=[...el.querySelectorAll(':scope>.tvb.say:not(.old)')].map(R); const toast=[...el.querySelectorAll(':scope>.jtoast.on')].map(R);
 return {pills,cardTop,nar,bub,toast}; })()"""
def ov(a,b,m=1):
    w=min(a['r'],b['r'])-max(a['l'],b['l']); h=min(a['b'],b['b'])-max(a['t'],b['t'])
    return max(0,w-m)*max(0,h-m)
def judge(d):
    out=[]
    P=d['pills']
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            if ov(P[i],P[j],2)>0: out.append(('A',f"{P[i]['n']} × {P[j]['n']}"))
    for p in P:
        if p['b']>d['cardTop']+2: out.append(('B',p['n']))
        if p['k']=='who' and any(ov(p,n)>0.3*p['w']*p['h'] for n in d['nar']): out.append(('E',p['n']))
    for b in d['bub']:
        if any(ov(b,n)>0 for n in d['nar']): out.append(('C','말풍선 × 말씀 카드'))
        if b['b']>d['cardTop']+2: out.append(('C','말풍선 × 아래 카드'))
    for t in d['toast']:
        for b in d['bub']:
            if ov(t,b)>0: out.append(('D','안내 띠 × 말풍선'))
        for p in P:
            if p['k']=='who' and ov(t,p)>0: out.append(('D',f"안내 띠 × {p['n']}"))
    return out
async def one(b,W,H,jobs,res):
    pg=await b.new_page(viewport={'width':W,'height':H}); await pg.goto(URL,wait_until='load'); await pg.wait_for_timeout(2500)
    for kind,pid,s,n in jobs:
        await pg.evaluate("document.querySelector('.atn')?.remove();document.body.style.overflow=''")
        if kind=='plan': await pg.evaluate(f"planOpen('{pid}',{s})"); await pg.wait_for_timeout(250); await pg.evaluate("document.querySelector('.bmtgo0')?.click()")
        else:
            await pg.evaluate("(()=>{const b=document.createElement('button');b.dataset.atone=1;document.body.appendChild(b);b.click();b.remove();})()"); await pg.wait_for_timeout(250)
            await pg.evaluate("document.querySelector('.bmtgo0')?.click()")
            for _ in range(s): await pg.evaluate("document.querySelector('.atn [data-t=nextS]').click()"); await pg.wait_for_timeout(80)
        best=[]
        for wait in (2600,3400):   # 걷기가 끝나고 말씀·말풍선이 뜬 뒤를 두 번 봄
            await pg.wait_for_timeout(wait); d=await pg.evaluate(MEASURE)
            if d: best+=judge(d)
        res.append((pid,s,n,sorted(set(best))))
    await pg.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(); await pg.goto(URL,wait_until='load'); await pg.wait_for_timeout(2500)
        jobs=[('plan',k,i,t) for k,n,tt in await pg.evaluate("Object.values(PLANS).map(p=>[p.id,p.scenes.length,p.scenes.map(s=>s.t)])") for i,t in enumerate(tt)]
        jobs+=[('atone','atone',i,f'대속죄일 {i+1}') for i in range(10)]
        await pg.close(); report={}
        for W,H in SIZES:
            res=[]; k=4; chunks=[jobs[i::k] for i in range(k)]
            await asyncio.gather(*[one(b,W,H,c,res) for c in chunks])
            report[f'{W}x{H}']=res
            tot={}; [tot.__setitem__(x[0],tot.get(x[0],0)+1) for r in res for x in r[3]]
            print(f'== {W}x{H}: 장면 {len(res)}개 · 겹침', ' '.join(f'{k}{v}' for k,v in sorted(tot.items())) or '없음')
            for pid,s,n,o in sorted(res):
                o=[x for x in o if x[0]!='E']
                if o: print(f'  {pid} {s+1} {n[:22]}: '+' · '.join(f'{a}:{b}' for a,b in o[:6]))
        json.dump(report,open('/tmp/ui_overlap.json','w'),ensure_ascii=False)
        await b.close()
asyncio.run(main())
