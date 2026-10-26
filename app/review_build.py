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
for k in sorted([k for k in _SC if not k.startswith('_')],key=int):
    o=_SC[k]; pl=P365[int(k)-1]
    li=''.join("<li><b>%s</b> %s</li>"%(_h.escape(c.get('lab') or c.get('k')),_h.escape(_re.sub(r'\*\*|__','',_first(c))[:90])) for c in o['cards'])
    kq=_KQ.get(k,{}).get('q','')
    _rows.append("<section data-day='%s'><h2>%s일 · %s <small>%s</small></h2><p class='sp'>%s</p><ol>%s</ol><p class='kq'>나의 생각거리: %s</p><div class='act'><a href='v2.html?day=%s' target='_blank'>카드로 보기 ›</a><button data-ok>승인</button><textarea placeholder='고칠 점 (이 기기에 저장)'></textarea></div></section>"%(k,k,_h.escape(pl['spec']),_TN.get(o.get('type',''),o.get('type','—')),_h.escape(o.get('spine','(중심 한 줄 없음)')),li,_h.escape(kq),k))
_CSS="body{font:15px/1.6 system-ui,sans-serif;margin:0 auto;max-width:760px;padding:16px;background:#f7f4ee;color:#222}h1{font-size:22px}section{background:#fff;border:1px solid #e3dccf;border-radius:12px;padding:14px 16px;margin:12px 0}section.ok{border-color:#2e7d4f;background:#f3faf5}h2{font-size:17px;margin:0 0 6px}h2 small{font-weight:400;color:#8a6d3b;margin-left:6px}.sp{font-weight:700;color:#5a3d12;margin:4px 0 8px}ol{margin:0;padding-left:22px}li{margin:2px 0;font-size:14px}li b{color:#8a6d3b;font-weight:600;margin-right:4px}.kq{font-size:14px;color:#555}.act{display:flex;gap:8px;align-items:flex-start;flex-wrap:wrap}.act a{padding:7px 10px}.act button{padding:7px 14px;border-radius:8px;border:1px solid #2e7d4f;background:#fff;color:#2e7d4f;font-weight:700}section.ok .act button{background:#2e7d4f;color:#fff}textarea{flex:1;min-width:220px;min-height:38px;border:1px solid #ddd;border-radius:8px;padding:6px}#bar{position:sticky;top:0;background:#f7f4ee;padding:8px 0;display:flex;gap:8px;align-items:center}#bar button{padding:8px 12px;border-radius:8px;border:0;background:#5a3d12;color:#fff;font-weight:700}"
_JS="""const K="cbsr-review",S=(()=>{try{return JSON.parse(localStorage.getItem(K)||"{}")}catch(e){return{}}})(),sv=()=>{try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}};
const cnt=()=>{const n=document.querySelectorAll("section").length,o=document.querySelectorAll("section.ok").length;document.getElementById("cnt").textContent="승인 "+o+" / "+n;};
document.querySelectorAll("section").forEach(s=>{const d=s.dataset.day,r=S[d]||{},t=s.querySelector("textarea"),b=s.querySelector("[data-ok]");t.value=r.n||"";if(r.ok)s.classList.add("ok");
b.onclick=()=>{r.ok=!r.ok;S[d]=r;s.classList.toggle("ok",r.ok);sv();cnt();};t.oninput=()=>{r.n=t.value;S[d]=r;sv();};});
document.getElementById("cp").onclick=()=>{const L=Object.entries(S).filter(([d,r])=>r.ok||r.n).map(([d,r])=>d+"일: "+(r.ok?"승인":"수정")+(r.n?" — "+r.n:"")).join("\\n");navigator.clipboard.writeText(L||"(메모 없음)").then(()=>alert("복사했습니다. 대화에 붙여 넣어 주세요."));};cnt();"""
open(OUT+'/review.html','w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>이야기 카드 검토</title><meta name="robots" content="noindex"><style>'+_CSS+'</style></head><body><h1>이야기 카드 검토</h1><p>날마다 중심 한 줄과 카드 흐름을 보고 승인하거나 고칠 점을 적습니다. 다 본 뒤 \'메모 복사\'를 눌러 대화에 붙여 넣어 주세요.</p><div id="bar"><span id="cnt"></span><button id="cp">메모 복사</button></div>'+''.join(_rows)+'<script>'+_JS+'</script></body></html>')
