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
const CF=()=>{try{const o=JSON.parse(localStorage.getItem("v2:cbsr-cardfb")||"{}");return Object.keys(o).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true})).map(k=>{const r=o[k],m=k.match(/^(rj:)?(\\d+)([AB]?)#(.+)$/);if(!m)return"";const n=+m[2];return (m[1]?"리딩지저스 "+(Math.floor((n-1)/7)+1)+"주차 "+((n-1)%7+1)+"일째":"365 "+n+"일"+(m[3]==="A"?" 2027판":m[3]==="B"?" 2028판":""))+" · "+(m[4]==="qt"?"QT":(+m[4]+1)+"번째 카드")+(r.lab?" ("+r.lab+")":"")+": "+r.n}).filter(Boolean)}catch(e){return[]}};
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

# 리딩지저스 이야기 카드 검토 페이지 (rj.html): story_rj.json, 날 번호 = (주-1)*7+요일+1
_SRJ=json.load(open('ux/story_rj.json')) if os.path.exists('ux/story_rj.json') else {}
_SRJ={k:v for k,v in _SRJ.items() if not k.startswith('_')}
_RP=json.load(open('plan.json'))['plan']; _rr=[]
for k in sorted(_SRJ,key=int):
    n=int(k)-1; w,d=n//7+1,n%7; lab=_RP[w-1][d]['label'] if w-1<len(_RP) and d<len(_RP[w-1]) else ''
    o=_SRJ[k]; inner=_pvhtml(k,'',o,(o.get('kwq') or {}).get('q',''))
    inner=inner.replace("v2.html?p=365&review=1&day="+k,"v2.html?p=rj&review=1&day="+k)
    _rr.append("<section data-day='%s'><h2>%s주차 %s일째 · %s</h2>%s</section>"%(k,w,d+1,_h.escape(lab),inner))
open(OUT+'/rj.html','w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>리딩지저스 이야기 카드 검토</title><meta name="robots" content="noindex"><style>'+_CSS+'</style></head><body><h1>리딩지저스 45주 이야기 카드 검토</h1><p>36–45주차(사도행전–요한계시록). \'카드로 보기\'로 실제 화면을 열고, ✎로 카드에 바로 메모합니다. 다 본 뒤 \'메모 복사\'를 눌러 대화에 붙여 넣어 주세요.</p><div id="bar"><span id="cnt"></span><span id="cnt2"></span><button id="cp">메모 복사</button></div>'+''.join(_rr)+'<script>'+_JS+'</script></body></html>')

# 그림 목록 페이지 (gallery.html): ux/photos_master.json — 태그·쓰는 자리·뺀 이유를 한눈에
_PM=json.load(open('ux/photos_master.json')) if os.path.exists('ux/photos_master.json') else []
_PU=json.load(open('ux/photos_use.json')) if os.path.exists('ux/photos_use.json') else {}
_FULL=json.load(open('plan.json'))['full']
_SETN={1:'자연·하늘',2:'족장',3:'애굽·출애굽',4:'광야·성막',5:'정착·사사',6:'왕국',7:'분열·포로',8:'시·지혜·일상',9:'복음서',10:'사도행전·서신',11:'원역사(창 1–11)'}
def _refs(rs): return ', '.join(_FULL[b-1]+' '+(str(a) if a==z else '%d–%d'%(a,z))+'장' for b,a,z in rs)
exec(open('photo_cats.py').read().split("if __name__")[0])
_CAT=build(_PM)
_gc=[]
for r in _PM:
    RL={'scene':'사건 장면','setting':'장소·생활 배경','object':'소품·동작','landscape':'자연·지형','symbolic':'비유·환상·상징'}
    kind='뺌' if r['out'] else ('특정 장면' if r['scope']=='s' else '두루 쓰는 배경')
    src=('img/gx/' if r['out'] else 'img/g/')+r['id']+'.jpg'
    info=[]
    if r['out']: info.append("<b class='x'>뺀 이유: %s</b>"%_h.escape(r['out']))
    if r['scope']=='s' and not r['out']:
        if r['refs']: info.append('쓰는 장(표지 카드에서만, 다른 카드는 아래 말이 있어야 함): '+_h.escape(_refs(r['refs'])))
        if r['kw']: info.append('카드 글에 이 말이 있으면: '+_h.escape(' · '.join(k.rstrip('~') for k in r['kw'])))
    else: info.append('시대: '+_h.escape(', '.join(_SETN.get(x,str(x)) for x in r['sets'])))
    if r.get('deny'): info.append('이 말이 있으면 쓰지 않음: '+_h.escape(' · '.join(r['deny'])))
    if r.get('role'): info.append('용도: '+RL.get(r['role'],r['role']))
    _c=_CAT.get(r['id'],{}); info.insert(0,'<b>분류:</b> '+_h.escape(_c.get('f',''))+((' · 때: '+_c['t']) if _c.get('t') else '')+((' · '+_c['w']) if _c.get('w') else ''))
    info.append('태그: '+_h.escape(', '.join(r['tags'])))
    if not r['out']:
        U=_PU.get(r['id'],[])
        if U:
            li=''.join("<li><a target='_blank' href='v2.html?p=%s%s&review=1&day=%d&card=%d'>%s · %s · %d번째 카드</a>%s</li>"%(pl,('&pv='+pv) if pv else '',no,i,('리딩지저스 %d주차 %d일째'%((no-1)//7+1,(no-1)%7+1)) if pl=='rj' else ('365 %d일 %s'%(no,'2027판' if pv=='A' else '2028판')),_h.escape(dl),i+1,(' — '+_h.escape(cl)) if cl else '') for pl,pv,no,i,dl,cl in U)
            info.append("<details><summary>쓰인 카드 %d장 보기</summary><ul class='use'>%s</ul></details>"%(len(U),li))
        else: info.append('지금 쓰인 카드: 없음')
    _gc.append(("<figure data-cf='%s' data-ct='%s' data-cw='%s' "%(_h.escape(_c.get('f','')),_c.get('t',''),_c.get('w','')))+"data-k='%s' data-id='%s'><img loading='lazy' src='%s' alt=''><figcaption><span class='gid'>%s</span> <span class='kd'>%s</span><b>%s</b><small>%s</small><div class='act'>%s<button data-act='del' data-id='%s'>삭제</button></div><textarea data-fb='%s' placeholder='이 그림 메모(이유)'></textarea></figcaption></figure>"%(kind,r['id'],src,r['id'],kind,_h.escape(r['memo']),'<br>'.join(info),("<button data-act='back' data-id='%s'>되살리기</button>"%r['id']) if r['out'] else ("<button data-act='keep' data-id='%s'>빼서 보관</button>"%r['id']),r['id'],r['id']))
import collections as _co
_act=[r for r in _PM if not r['out']]
_cf=_co.Counter(_CAT[r['id']]['f'] for r in _act); _ct=_co.Counter(_CAT[r['id']]['t'] for r in _act if _CAT[r['id']]['t']); _cw=_co.Counter(_CAT[r['id']]['w'] for r in _act if _CAT[r['id']]['w'])
_ALLF=[f for f,_,_ in RULES+PEOPLE+OBJ+PLACE]
def _tree():
    top=_co.OrderedDict()
    for f in _ALLF+sorted(k for k in _cf if k not in _ALLF):
        a=f.split(' › '); top.setdefault(a[0],[]).append(f)
    h=''
    for t,fs in top.items():
        n=sum(_cf.get(f,0) for f in _cf if f.startswith(t))
        if t=='성경 장면':
            eras=_co.OrderedDict()
            for f in sorted(fs,key=lambda f:(list(SETN.values()).index(f.split(' › ')[1]) if f.split(' › ')[1] in SETN.values() else 99,f)): eras.setdefault(f.split(' › ')[1],[]).append(f)
            inner=''.join("<div class='ce'><button data-cf='%s'>%s <i>%d</i></button>%s</div>"%(_h.escape('성경 장면 › '+e),_h.escape(e),sum(_cf.get(f,0) for f in v),''.join("<button class='sm' data-cf='%s'>%s <i>%d</i></button>"%(_h.escape(f),_h.escape(f.split(' › ')[-1]) if f.count(' › ')>1 else '(책 없음)',_cf.get(f,0)) for f in v)) for e,v in eras.items())
        else:
            mids=_co.OrderedDict()
            for f in fs: a=f.split(' › '); mids.setdefault(a[1] if len(a)>2 else '',[]).append(f)
            inner=''.join("<div class='ce'>%s%s</div>"%(("<b>%s</b>"%_h.escape(m)) if m else '',''.join("<button class='sm%s' data-cf='%s'>%s <i>%d</i></button>"%(' low' if _cf.get(f,0)<=2 else '',_h.escape(f),_h.escape(f.split(' › ')[-1]),_cf.get(f,0)) for f in v)) for m,v in mids.items())
        h+="<details class='ct'><summary><button data-cf='%s'>%s <i>%d</i></button></summary>%s</details>"%(_h.escape(t),_h.escape(t),n,inner)
    return h
_TN=['새벽·아침','한낮','저녁·노을','밤']; _WN=['봄·꽃','추수·가을','겨울·눈·서리','폭풍·비','가뭄·마른 땅']
_books=set(FULL[r['refs'][0][0]-1] for r in _act if r['scope']=='s' and r.get('refs'))
_nobook=[b for b in FULL if b not in _books]
_low=[f for f in _ALLF if _cf.get(f,0)<=2]
_CATHTML=("<section id='cat'><h2>분류</h2><p class='cn'>그림을 누르면 그 분류만 보입니다. <b class='lowk'>붉은 칸</b>은 2장 이하로 모자란 분류입니다. 자연·사람·물건·장소는 어느 날에나 두루 쓰는 그림만 세고, 특정 장면 그림은 '성경 장면'에 시대·책별로 모았습니다. 때·계절은 모든 그림을 셉니다. 사진을 누르면 크게 보이고, 화살표 키로 넘깁니다.</p>"+_tree()+
 "<div class='cx'><b>때</b> "+''.join("<button class='sm%s' data-ct='%s'>%s <i>%d</i></button>"%(' low' if _ct.get(t,0)<=3 else '',t,t,_ct.get(t,0)) for t in _TN)+"</div>"+
 "<div class='cx'><b>계절·날씨</b> "+''.join("<button class='sm%s' data-cw='%s'>%s <i>%d</i></button>"%(' low' if _cw.get(t,0)<=3 else '',t,t,_cw.get(t,0)) for t in _WN)+"</div>"+
 "<details class='gap'><summary>모자란 곳 한눈에 보기</summary><p><b>2장 이하인 분류 %d곳:</b> %s</p><p><b>장면 그림이 한 장도 없는 책 %d권:</b> %s</p></details>"%(len(_low),_h.escape(', '.join(f.replace('자연 › ','').replace(' › ','/') for f in _low)),len(_nobook),_h.escape(', '.join(_nobook)))+
 "<p id='cf_on'></p></section>")
_GFB=''.join(l+'\n' for l in tags.split('\n') if 'bible.js' not in l)
_GCSS="#lb{position:fixed;inset:0;background:rgba(0,0,0,.88);display:none;align-items:center;justify-content:center;z-index:99}#lb.on{display:flex}#lb figure{margin:0;max-width:92vw;text-align:center;background:none;box-shadow:none}#lb img{max-width:92vw;max-height:84vh;border-radius:6px;display:block;margin:0 auto}#lb figcaption{color:#eee;font-size:14px;margin-top:8px}#lb small{color:#bbb}#lb button{position:absolute;background:rgba(255,255,255,.12);color:#fff;border:0;border-radius:50%;width:48px;height:48px;font-size:28px;cursor:pointer}#lbp{left:16px;top:50%}#lbn{right:16px;top:50%}#lbx{right:16px;top:16px;font-size:20px!important}#cat{background:#fff;border-radius:12px;padding:12px 14px;margin:10px 0 14px}#cat h2{font-size:17px;margin:0 0 4px}.cn{margin:0 0 8px;font-size:13px;color:#555}.ct{border-top:1px solid #eee;padding:6px 0}.ct summary{cursor:pointer;list-style:none}.ct summary::-webkit-details-marker{display:none}.ct summary button{font-weight:700}.ce{margin:6px 0 6px 12px;display:flex;flex-wrap:wrap;gap:5px;align-items:center}.ce b{font-size:12.5px;color:#666;margin-right:4px}#cat button{border:1px solid #ccc;background:#fafafa;border-radius:14px;padding:4px 10px;font-size:13px;cursor:pointer}#cat button i{font-style:normal;color:#888;margin-left:2px}#cat button.low{border-color:#e3a08f;background:#fdeee9}#cat button.on{background:#333;color:#fff}#cat button.on i{color:#ddd}.lowk{color:#c0563f}.cx{margin:8px 0;display:flex;flex-wrap:wrap;gap:5px;align-items:center}.cx b{font-size:13px;margin-right:4px}.gap{margin-top:8px;font-size:13.5px}.gap summary{cursor:pointer;font-weight:700}#cf_on{margin:6px 0 0;font-size:13px;color:#333}body{font-family:system-ui,sans-serif;margin:0;padding:16px;background:#f6f3ee;color:#222}h1{font-size:20px}#gf{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 14px}#gf button{border:1px solid #bbb;background:#fff;border-radius:16px;padding:6px 12px}#gf button.on{background:#333;color:#fff}#gq{padding:6px 10px;border:1px solid #bbb;border-radius:8px;flex:1;min-width:140px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}figure{margin:0;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px #0002}figure img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}figcaption{padding:8px 10px;font-size:13px;line-height:1.5}figcaption b{display:block;font-size:14px;margin:2px 0}figcaption small{color:#555;display:block}.gid{color:#888;font-size:12px}.kd{font-size:12px;background:#eee;border-radius:6px;padding:1px 6px}figure[data-k='뺌'] .kd{background:#f6d5d0}b.x{color:#a33;display:inline;font-size:13px}textarea{width:100%;box-sizing:border-box;margin-top:6px;font:inherit;font-size:13px;min-height:34px;border:1px solid #ddd;border-radius:6px}#bar{position:sticky;top:0;background:#f6f3eeee;padding:6px 0;z-index:2}#cp{padding:6px 12px}details summary{cursor:pointer;color:#05a;margin-top:2px}ul.use{margin:4px 0 0;padding-left:18px;max-height:260px;overflow:auto}ul.use li{margin:3px 0}ul.use a{color:#05a}.act{display:flex;gap:6px;margin-top:6px}.act button{flex:1;border:1px solid #bbb;background:#fff;border-radius:8px;padding:6px 0;font-size:13px;cursor:pointer}.act button.on{color:#fff}.act button[data-act=keep].on{background:#b07a1c;border-color:#b07a1c}.act button[data-act=del].on{background:#a33;border-color:#a33}.act button[data-act=back].on{background:#2f6b4f;border-color:#2f6b4f}figure.marked{outline:3px solid #b07a1c}figure.marked-del{outline:3px solid #a33}figure.marked-del img{opacity:.45}#adm{background:#fff;border:1px solid #ddd;border-radius:10px;padding:8px 10px;font-size:13.5px;margin:8px 0}#adm input{padding:5px 8px;border:1px solid #bbb;border-radius:6px}#adm button{padding:5px 10px}#help{font-size:13px;color:#555;margin:4px 0 0}figure{position:relative}.bdg{position:absolute;left:8px;top:8px;background:#222d;color:#fff;font-size:12.5px;font-weight:700;padding:4px 9px;border-radius:999px;z-index:1}figure.marked-del .bdg{background:#a33}#tst{position:fixed;left:50%;bottom:18px;transform:translate(-50%,20px);max-width:92vw;background:#222;color:#fff;font-size:14px;line-height:1.5;padding:10px 14px;border-radius:12px;opacity:0;transition:.25s;z-index:9;pointer-events:none}#tst.on{opacity:1;transform:translate(-50%,0)}"
_GJS="""const K='gallery-fb';let M={};try{M=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
document.querySelectorAll('textarea[data-fb]').forEach(t=>{t.value=M[t.dataset.fb]||'';t.oninput=()=>{M[t.dataset.fb]=t.value;if(!t.value)delete M[t.dataset.fb];try{localStorage.setItem(K,JSON.stringify(M))}catch(e){};cnt()}});
const AL={keep:'빼서 보관',del:'삭제',back:'되살리기'},DONE={keep:'빼서 보관함',del:'삭제함',back:'되살리기로 정함'};
let A={},ADM=false,BUSY=false;
function paint(){document.querySelectorAll('.grid figure').forEach(f=>{const a=A[f.dataset.id];let bd=f.querySelector('.bdg');if(a){if(!bd){bd=document.createElement('span');bd.className='bdg';f.prepend(bd)}bd.textContent=DONE[a]+(a==='back'?' · 다음 사이트 갱신 때 돌아옴':' · 앱에서 빠짐')}else if(bd)bd.remove();f.classList.toggle('marked',a==='keep'||a==='back');f.classList.toggle('marked-del',a==='del');f.querySelectorAll('[data-act]').forEach(b=>b.classList.toggle('on',a===b.dataset.act))})}
function toast(t){let e=document.getElementById('tst');if(!e){e=document.createElement('div');e.id='tst';document.body.appendChild(e)}e.textContent=t;e.classList.add('on');clearTimeout(e._h);e._h=setTimeout(()=>e.classList.remove('on'),4200)}
function cnt(){document.getElementById('cnt').textContent='메모 '+Object.keys(M).length+'개 · 정한 그림 '+Object.keys(A).length+'장'}
function admBar(){const b=document.getElementById('adm');if(!b)return;if(!window.SYNC||!SYNC.available){b.innerHTML='<span>연결할 수 없습니다. 인터넷을 확인해 주세요.</span>';return}
 if(ADM){b.innerHTML='<b>관리자로 들어와 있습니다.</b> 단추를 누르면 바로 반영됩니다. <button id="admOut">나가기</button>';document.getElementById('admOut').onclick=async()=>{await SYNC.admin.logout();ADM=false;admBar()};return}
 b.innerHTML='관리자 비밀번호를 넣으면 단추가 바로 반영됩니다. <input id="admPw" type="password" placeholder="관리자 비밀번호" autocomplete="current-password"> <button id="admIn">들어가기</button> <span id="admMsg"></span>';
 document.getElementById('admIn').onclick=async()=>{const m=document.getElementById('admMsg');m.textContent='확인 중…';try{await SYNC.admin.login(document.getElementById('admPw').value);const st=await SYNC.admin.state();ADM=!!st.ok;m.textContent=ADM?'':'관리자 명단에 없는 계정입니다.';admBar()}catch(e){m.textContent='비밀번호가 맞지 않습니다.'}}}
document.querySelectorAll('[data-act]').forEach(b=>b.onclick=async()=>{const id=b.dataset.id,a=b.dataset.act;if(!ADM){toast('먼저 맨 위에서 관리자 비밀번호를 넣어 주세요.');document.getElementById('admPw')?.focus();return}if(BUSY)return;BUSY=true;const nv=A[id]===a?null:a;
 try{await SYNC.photos.set(id,nv);if(nv)A[id]=nv;else delete A[id];paint();cnt();toast(nv?(id+' 그림을 '+DONE[nv]+(nv==='back'?'. 다음 사이트 갱신 때 다시 쓰입니다.':'. 앱에서는 바로 빠지고, 파일은 다음 사이트 갱신 때 정리됩니다.')):(id+' 정한 것을 취소했습니다.'))}catch(e){toast('반영하지 못했습니다: '+(e.code||e.message||e))}BUSY=false});
(async()=>{cnt();admBar();if(!window.SYNC||!SYNC.available)return;try{A=await SYNC.photos.get()||{};paint();cnt()}catch(e){}try{const st=await SYNC.admin.state();ADM=!!st.ok}catch(e){}admBar()})();
document.getElementById('cp').onclick=()=>{const ids=Object.keys(M).sort();const t=ids.map(k=>'그림 '+k+': '+M[k]).join('\\n')||'(메모 없음)';navigator.clipboard.writeText(t).then(()=>{document.getElementById('cp').textContent='복사했습니다'},()=>prompt('복사해 주세요',t))};
(function(){const lb=document.createElement('div');lb.id='lb';lb.innerHTML='<button id="lbp" aria-label="앞 그림">‹</button><figure><img alt=""><figcaption></figcaption></figure><button id="lbn" aria-label="다음 그림">›</button><button id="lbx" aria-label="닫기">✕</button>';document.body.appendChild(lb);let cur=null;
 const vis=()=>[...document.querySelectorAll('.grid figure')].filter(f=>f.style.display!=='none');
 const show=f=>{cur=f;const im=f.querySelector('img');lb.querySelector('img').src=im.src;lb.querySelector('figcaption').innerHTML='<b>'+f.dataset.id+'</b> '+(f.querySelector('figcaption b')||{}).textContent+'<br><small>'+(f.dataset.cf||'')+'</small>';lb.classList.add('on')};
 const step=d=>{const L=vis(),i=L.indexOf(cur);if(i<0)return;show(L[(i+d+L.length)%L.length])};
 document.querySelectorAll('.grid figure img').forEach(im=>{im.style.cursor='zoom-in';im.onclick=()=>show(im.closest('figure'))});
 lb.onclick=e=>{if(e.target===lb||e.target.id==='lbx'){lb.classList.remove('on');cur=null}};document.getElementById('lbp').onclick=e=>{e.stopPropagation();step(-1)};document.getElementById('lbn').onclick=e=>{e.stopPropagation();step(1)};
 document.addEventListener('keydown',e=>{if(!lb.classList.contains('on'))return;if(e.key==='Escape'){lb.classList.remove('on');cur=null}if(e.key==='ArrowRight')step(1);if(e.key==='ArrowLeft')step(-1)})})();
let F='all',CF=null;const q=document.getElementById('gq');function ap(){const s=q.value.trim();let n=0;document.querySelectorAll('.grid figure').forEach(f=>{const okc=!CF||(CF[0]==='cf'?(f.dataset.cf===CF[1]||f.dataset.cf.startsWith(CF[1]+' › ')):f.dataset[CF[0]]===CF[1]);const ok=(F==='all'||f.dataset.k===F)&&okc&&(!s||f.textContent.includes(s));f.style.display=ok?'':'none';if(ok)n++});document.getElementById('cf_on').innerHTML=CF?'<b>'+CF[1]+'</b> '+n+'장 보는 중 · <a href="#" id="cfx">모두 보기</a>':'';const x=document.getElementById('cfx');if(x)x.onclick=e=>{e.preventDefault();CF=null;document.querySelectorAll('#cat button').forEach(b=>b.classList.remove('on'));ap()}}
document.querySelectorAll('#cat button').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();const k=b.dataset.cf!==undefined?'cf':b.dataset.ct!==undefined?'ct':'cw',v=b.dataset[k];CF=CF&&CF[0]===k&&CF[1]===v?null:[k,v];document.querySelectorAll('#cat button').forEach(x=>x.classList.toggle('on',!!CF&&x===b));ap();if(CF)document.getElementById('bar').scrollIntoView({behavior:'smooth'})});
document.querySelectorAll('#gf button').forEach(b=>b.onclick=()=>{F=b.dataset.f;document.querySelectorAll('#gf button').forEach(x=>x.classList.toggle('on',x===b));ap()});q.oninput=ap;"""
open(OUT+'/gallery.html','w').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>이야기 카드 그림 목록</title><meta name="robots" content="noindex">'+_GFB+'<style>'+_GCSS+'</style></head><body><h1>이야기 카드 그림 목록</h1><p>쓰는 그림 %d장, 뺀 그림 %d장. <b>특정 장면</b> 그림은 카드 글에 그 장면의 말이 있을 때만 나옵니다(표지 카드는 그 장을 읽는 날이면 나옴). 그림마다 「이 말이 있으면 쓰지 않음」을 두어 다른 사건과 섞이지 않게 했습니다. <b>두루 쓰는 배경</b> 중 자연 풍경은 시대가 맞는 날에 나오고, 장소·소품 그림은 카드와 이어지는 말이 있을 때만 나옵니다. 고칠 점은 그림 아래에 적고 \'메모 복사\'를 눌러 대화에 붙여 넣어 주세요.</p><p id="help">관리자로 들어오면 단추가 <b>바로 반영</b>됩니다. <b>빼서 보관</b>: 카드에는 더 나오지 않고 파일은 남겨 둡니다(뺀 그림 목록에서 되살릴 수 있음). <b>삭제</b>: 파일까지 지웁니다. <b>되살리기</b>: 뺀 그림을 다시 씁니다. 한 번 더 누르면 취소됩니다.</p><div id="adm"></div><div id="bar"><div id="gf"><button data-f="all" class="on">전체</button><button data-f="특정 장면">특정 장면</button><button data-f="두루 쓰는 배경">두루 쓰는 배경</button><button data-f="뺌">뺀 그림</button><input id="gq" placeholder="찾기: 언약궤, 출애굽기, g15…"></div><span id="cnt"></span> <button id="cp">메모 복사</button></div><div class="grid">'%(sum(1 for r in _PM if not r['out']),sum(1 for r in _PM if r['out']))+''.join(_gc)+'</div><script>'+_GJS+'</script></body></html>')
_gp=open(OUT+'/gallery.html').read().replace('<div id="bar">',_CATHTML+'<div id="bar">',1); open(OUT+'/gallery.html','w').write(_gp)
