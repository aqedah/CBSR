# 카드 검토 페이지(review.html): build_site.py 안에서 exec로 실행 (OUT, P365, _SC, json 사용)
import html as _h, re as _re
_TN={'T1':'되풀이 장면형','T2':'가운데 꺾임형','T3':'열쇠말 추적형','T4':'말과 판정 대조형','T5':'뒤집힘형','T6':'두 사람 나란히형','T7':'패턴과 이탈형','T8':'눈덩이형','T9':'기로형','T10':'길·세대형','T11':'기다림·시험형','T12':'먼저 찾아오심형'}
def _first(c):
    if c.get('k')=='cover': return (c.get('h','')+' / '+c.get('sub','')).replace('\n',' ')
    for x in c.get('b',[]) or []:
        if isinstance(x,str): return _re.split(r'(?<=[.?!])\s+',x)[0]
    return c.get('h','') or c.get('big','') or c.get('note','')
_KQ=json.load(open('ux/kwq.json'))
_rows=[]
import hashlib as _hl
def _pvhtml(k,pv,o,kq):
    li=''.join("<li><b>%s</b> %s</li>"%(_h.escape(c.get('lab') or c.get('k')),_h.escape(_re.sub(r'\*\*|__','',_first(c))[:90])) for c in o['cards'])
    Q=o.get('qt') or {}; ob=Q.get('obs') or {}; gd=Q.get('guide') or {}
    qt=''
    if Q:
        qt="<details><summary>QT 묶음 보기</summary><dl>"+''.join("<dt>%s</dt><dd>%s</dd>"%(a,_h.escape(str(b))) for a,b in [('오늘 이야기',gd.get('today','')),('읽으면서 찾기',gd.get('find','')),('관찰 질문',ob.get('q','')),('살펴볼 절',' / '.join('%s %s'%(l.get('t',''),':'.join(str(x) for x in l.get('r',[])[1:])) for l in ob.get('look',[]))),('하나님의 성품',Q.get('god','')),('성경 전체로',Q.get('christ','—')),('한 줄 묵상',Q.get('apply','')),('기도',Q.get('pray',''))] if b)+"</dl></details>"
    hsh=_hl.sha1(json.dumps(o,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:8]
    lab={'A':'2027판','B':'2028판','':''}[pv]
    q=(o.get('kwq') or {}).get('q') or kq
    return "<div class='pv' data-id='%s%s:%s'><h3>%s <small>%s</small></h3><p class='sp'>%s</p><ol>%s</ol>%s<p class='kq'>나의 생각거리: %s</p><div class='act'><a href='v2.html?p=365&review=1&day=%s%s' target='_blank'>카드로 보기 ›</a><button data-ok>승인</button><textarea placeholder='고칠 점 (이 기기에 저장)'></textarea></div></div>"%(k,pv,hsh,lab,_TN.get(o.get('type',''),o.get('type','—')),_h.escape(o.get('spine','(중심 한 줄 없음)')),li,qt,_h.escape(q),k,('&pv='+pv) if pv else '')
for k in sorted([k for k in _SC if not k.startswith('_')],key=int):
    o=_SC[k]; pl=P365[int(k)-1]; kq=_KQ.get(k,{}).get('q','')
    if 'A' in o or 'B' in o: inner="<div class='two'>"+''.join(_pvhtml(k,pv,o[pv],kq) for pv in ('A','B') if pv in o)+"</div>"
    else: inner=_pvhtml(k,'',o,kq)
    _rows.append("<section data-day='%s'><h2>%s일 · %s</h2>%s</section>"%(k,k,_h.escape(pl['spec']),inner))
_CSS=".two{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:700px){.two{grid-template-columns:1fr}}.pv{border-top:1px dashed #e3dccf;padding-top:8px}.pv.ok{background:#f3faf5}h3{font-size:15px;margin:4px 0}h3 small{font-weight:400;color:#8a6d3b}dl{font-size:13.5px;margin:6px 0}dt{font-weight:700;color:#5a3d12;margin-top:4px}dd{margin:0 0 0 8px}body{font:15px/1.6 system-ui,sans-serif;margin:0 auto;max-width:760px;padding:16px;background:#f7f4ee;color:#222}h1{font-size:22px}section{background:#fff;border:1px solid #e3dccf;border-radius:12px;padding:14px 16px;margin:12px 0}section.ok{border-color:#2e7d4f;background:#f3faf5}h2{font-size:17px;margin:0 0 6px}h2 small{font-weight:400;color:#8a6d3b;margin-left:6px}.sp{font-weight:700;color:#5a3d12;margin:4px 0 8px}ol{margin:0;padding-left:22px}li{margin:2px 0;font-size:14px}li b{color:#8a6d3b;font-weight:600;margin-right:4px}.kq{font-size:14px;color:#555}.act{display:flex;gap:8px;align-items:flex-start;flex-wrap:wrap}.act a{padding:7px 10px}.act button{padding:7px 14px;border-radius:8px;border:1px solid #2e7d4f;background:#fff;color:#2e7d4f;font-weight:700}.pv.ok .act button{background:#2e7d4f;color:#fff}textarea{flex:1;min-width:220px;min-height:38px;border:1px solid #ddd;border-radius:8px;padding:6px}#bar{position:sticky;top:0;background:#f7f4ee;padding:8px 0;display:flex;gap:8px;align-items:center}#bar button{padding:8px 12px;border-radius:8px;border:0;background:#5a3d12;color:#fff;font-weight:700}"
_JS="""const K="cbsr-review",S=(()=>{try{return JSON.parse(localStorage.getItem(K)||"{}")}catch(e){return{}}})(),sv=()=>{try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}};
const cnt=()=>{const n=document.querySelectorAll(".pv").length,o=document.querySelectorAll(".pv.ok").length;document.getElementById("cnt").textContent="승인 "+o+" / "+n;};
document.querySelectorAll(".pv").forEach(s=>{const d=s.dataset.id,r=S[d]||{},t=s.querySelector("textarea"),b=s.querySelector("[data-ok]");t.value=r.n||"";if(r.ok)s.classList.add("ok");
b.onclick=()=>{r.ok=!r.ok;S[d]=r;s.classList.toggle("ok",r.ok);sv();cnt();};t.oninput=()=>{r.n=t.value;S[d]=r;sv();};});
const CF=()=>{try{const o=JSON.parse(localStorage.getItem("v2:cbsr-cardfb")||"{}");return Object.keys(o).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true})).map(k=>{const r=o[k],m=k.match(/^(\\d+)([AB]?)#(.+)$/);if(!m)return"";return m[1]+"일"+(m[2]==="A"?" 2027판":m[2]==="B"?" 2028판":"")+" · "+(m[3]==="qt"?"QT":(+m[3]+1)+"번째 카드")+(r.lab?" ("+r.lab+")":"")+": "+r.n}).filter(Boolean)}catch(e){return[]}};
document.getElementById("cnt2").textContent="카드 메모 "+CF().length+"개";
document.getElementById("cp").onclick=()=>{const L0=CF();const L=Object.entries(S).filter(([d,r])=>r.ok||r.n).map(([d,r])=>d.replace(/A:/,"일 2027판 ").replace(/B:/,"일 2028판 ").replace(/^(\\d+):/,"$1일 ")+": "+(r.ok?"승인":"수정")+(r.n?" — "+r.n:"")).join("\\n");const ALL=[L,L0.join("\\n")].filter(Boolean).join("\\n");navigator.clipboard.writeText(ALL||"(메모 없음)").then(()=>alert("복사했습니다. 대화에 붙여 넣어 주세요."));};cnt();"""
open(OUT+'/review.html','w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>이야기 카드 검토</title><meta name="robots" content="noindex"><style>'+_CSS+'</style></head><body><h1>이야기 카드 검토</h1><p>날마다 중심 한 줄과 카드 흐름, QT 묶음을 보고 승인하거나 고칠 점을 적습니다. 다 본 뒤 \'메모 복사\'를 눌러 대화에 붙여 넣어 주세요.</p><div id="bar"><span id="cnt"></span><span id="cnt2"></span><button id="cp">메모 복사</button></div>'+''.join(_rows)+'<script>'+_JS+'</script></body></html>')

# 시험 날(2027판·2028판) 묶음 페이지
_pr=[r for r in _rows if r.count("<div class='pv'")>=2]
open(OUT+'/pilot.html','w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>2027·2028 시험 날</title><meta name="robots" content="noindex"><style>'+_CSS+'</style></head><body><h1>2027판·2028판 시험 날</h1><p>같은 본문을 2027년(1년차)과 2028년(2년차)에 서로 다른 이야기와 QT로 읽게 하는 시험입니다. 날마다 두 판을 나란히 보고, \'카드로 보기\'로 실제 화면을 엽니다. 카드 위쪽 ✎를 누르면 읽던 그 카드에 바로 메모를 남깁니다. 카드를 다 넘긴 뒤 \'QT로 이어가기\'를 누르면 같은 관점의 QT가 이어집니다.</p><div id="bar"><span id="cnt"></span><span id="cnt2"></span><button id="cp">메모 복사</button></div>'+''.join(_pr)+'<script>'+_JS+'</script></body></html>')

# 2027판 달별 검토 페이지 (jan.html 1–31일, feb.html 32–59일)
for _fn,_lo,_hi,_mn in [('jan',1,31,'1월'),('feb',32,59,'2월'),('rest',301,365,'301–365일(2026년 남은 날)')]:
    _jr=[r for r in _rows if _re.search(r"data-day='(\d+)'",r) and _lo<=int(_re.search(r"data-day='(\d+)'",r).group(1))<=_hi]
    open(OUT+'/'+_fn+'.html','w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+_mn+' 검토</title><meta name="robots" content="noindex"><style>'+_CSS+'</style></head><body><h1>'+(_mn if _fn=='rest' else '2027판 '+_mn+'('+str(_lo)+'–'+str(_hi)+'일)')+' 검토</h1><p>날마다 중심 물음과 카드 흐름, QT 묶음을 봅니다. \'카드로 보기\'를 누르면 실제 화면이 열리고, 카드 위쪽 ✎로 그 카드에 바로 메모합니다. 카드를 다 넘긴 뒤 \'QT로 이어가기\'로 QT까지 확인합니다. 다 본 뒤 \'메모 복사\'를 눌러 대화에 붙여 넣어 주세요.</p><div id="bar"><span id="cnt"></span><span id="cnt2"></span><button id="cp">메모 복사</button></div>'+''.join(_jr)+'<script>'+_JS+'</script></body></html>')
