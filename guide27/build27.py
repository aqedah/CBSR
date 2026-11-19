import re,json,sys
css=open('css.css').read()+open('extra.css').read()
DIST=open('../a5fit/dist.js').read()
MAPFIT="""(function(){document.querySelectorAll('.wmap .mfr svg').forEach(s=>{
 const v0=(s.dataset.v0||s.getAttribute('viewBox')).split(/[ ,]+/).map(Number);s.dataset.v0=v0.join(' ');
 const r=s.parentNode.getBoundingClientRect();if(!r.width||!r.height)return;const fa=r.width/r.height,ma=v0[2]/v0[3];
 let x=v0[0],y=v0[1],w=v0[2],h=v0[3];
 if(fa<ma){h=w/fa;y=v0[1]-(h-v0[3])/2}else{w=h*fa;x=v0[0]-(w-v0[2])/2}
 s.setAttribute('viewBox',[x,y,w,h].map(n=>n.toFixed(2)).join(' '));
 const bg=s.querySelector('rect');if(bg){bg.setAttribute('x',x);bg.setAttribute('y',y);bg.setAttribute('width',w);bg.setAttribute('height',h);}
});})();"""

def vs(t): return re.sub(r'(?<=\()([^()]*\d+:\d+[^()]*)(?=\))',r'<span class="vs">\1</span>',t)
def vsm(t): return re.sub(r'(?<![\d:>])(\d+:\d+(?:–\d+)?(?:(?:, |; )(?:\d+:)?\d+(?:–\d+)?)*)(?=에서|까지|과 |와 )',r'<span class="vs">\1</span>',vs(t))
import base64,os
_TC={}
def tile(m):
    p=m.group(1)
    if p not in _TC:
        f='/home/claude/cbsr/app/'+p
        _TC[p]=('data:image/webp;base64,'+base64.b64encode(open(f,'rb').read()).decode()) if os.path.exists(f) else ''
    return 'href="'+_TC[p]+'"'
WDN={'월':'월요일','화':'화요일','수':'수요일','목':'목요일','금':'금요일','토':'토요일','일':'일요일'}
def page(D,pn=22):
    date=D['date'].split(' (')[0]; wd=WDN[D['date'].split('(')[1][0]]
    pic=D.get('pic'); mp=MAPS.get(str(D['no']),{}).get('html') if not D.get('nomap') else None
    if mp: mp=re.sub(r'<button class="mplay".*?</button>','',mp,flags=re.S)
    if mp: mp=re.sub(r'<svg([^>]*?) width="[^"]*" height="[^"]*" preserveAspectRatio="[^"]*"',r'<svg\1 preserveAspectRatio="xMidYMid meet" data-vb0="1"',mp,count=1)
    if mp: mp=re.sub(r'(<svg.*?</svg>)',r'<div class="mfr">\1</div>',mp,count=1,flags=re.S)
    if mp: mp=re.sub(r'href="https://aqedah\.github\.io/CBSR/([^"]+)"',tile,mp)
    look=''.join(f'<div class="i">{"<span class=ck>✓</span>" if x["ck"] else ""}<span class="chip">{x["tool"]}</span>{vs(x["text"])}</div>' for x in D['looks'])
    if mp: lookblk=f'<div class="two wmap"><div class="c1"><div class="box lk">{look}</div></div><div class="c2">{mp}</div></div>'
    elif pic: lookblk=f'<div class="two"><div class="c1"><div class="box lk">{look}</div></div><div class="c2"><div class="pic"><div class="im"><img src="{pic[0]}" alt=""></div><div class="cap">{pic[1]}</div></div></div></div>'
    else: lookblk=f'<div class="box lk">{look}</div>'
    wordp=f'<p class="wd sans"><span class="wdl">말뜻</span><b>{D["word"][0]}</b> {vs(D["word"][1])}</p>' if D.get('word') and D['word'][0] else ''
    L=f'''<div class="pg q1">
<div class="hd2 sans"><div class="dd"><b>{date}</b><span>{wd} · {D["no"]}일째</span><span>{D["min"]}</span></div><div class="tb"><b>{D["t"]}</b><span>{D["sub"]}</span></div></div>
<p class="sec sans"><span class="n">1</span>오늘의 흐름</p>
<p class="b">{vs(D["today"])}</p>
{wordp}
<p class="sec sans go"><span class="n">2</span>성경 읽기<span class="scn">{''.join(f'<i>{x}</i>' for x in D["scenes"])}</span></p>
<div class="mk">{''.join(f'<div class="mi{" rep" if m["rep"] else ""}"><div><span class="chip{" rep" if m["rep"] else ""}">{m["tool"]}</span>{"<span class=star>대표</span>" if m["rep"] else ""} {vsm(m["text"])}</div></div>' for m in D["marks"])}</div>
<p class="sec sans"><span class="n">3</span>눈여겨볼 것</p>
{lookblk}
<p class="lab sans" style="margin-top:1.6mm">성경 전체로</p><p class="rd"><span class="chip">{D["christ"][0]}</span>{vs(D["christ"][1])}</p>
<div class="pn">{pn}</div></div>'''
    g=D['god']; ap=D['apply']
    R=f'''<div class="pg r q1">
<p class="sec sans" style="margin-top:0"><span class="n">4</span>나의 묵상</p>
<p class="lab sans"><span class="st">1</span>본문 관찰</p><p class="q">{vs(D["q"])}</p><div class="lnw"><div class="ln"></div><div class="ln"></div><div class="ln"></div></div>
<p class="lab sans"><span class="st">2</span>하나님의 성품</p><p class="q">{vs(g[0])} {g[1]}</p><div class="lnw"><div class="ln"></div><div class="ln"></div></div>
<p class="lab sans"><span class="st">3</span>적용</p><p class="q">{vs(ap["lead"])}{''.join(f' <b>→ {x}</b>' for x in ap["fu"])}</p><div class="lnw"><div class="ln"></div><div class="ln"></div><div class="ln"></div></div>
<p class="lab sans"><span class="st">4</span>오늘의 기도</p><div class="lnw"><div class="ln"></div><div class="ln"></div></div>
<div class="after"><p class="h sans"><span class="n">5</span>쓴 뒤에 읽기 — 해설과 기도<span class="stuck">해설은 정답이 아닙니다. 내 묵상과 비교해 보세요</span></p>
<p><span class="k">해설</span>{vs(D["note"])}</p><p><span class="k">기도</span>{D["pray"]}</p></div>
<div class="pn">{pn+1}</div></div>'''
    return f'<div class="spread" id="d{D["no"]}">{L}{R}</div>'
import os
MAPS=json.load(open('maps.json')) if os.path.exists('maps.json') else {}
days=json.load(open(sys.argv[1]))
out=''.join(page(D,18+2*D['no']) for D in days)
out=out.replace('〈','<span class="abl">〈</span>').replace('〉','<span class="abr">〉</span>')
ZOOM="<script>(function(){function z(){const sp=document.querySelector('.spread');if(!sp)return;document.body.style.zoom=1;const w=sp.getBoundingClientRect().width;document.body.style.zoom=Math.min(1,(innerWidth-8)/w);}z();addEventListener('resize',z);})();</script>"
open(sys.argv[2],'w').write('<!doctype html><html><head><meta charset="utf-8"><title>2027 새 틀 1권</title><style>'+css+'</style></head><body>'+out+'<script>'+DIST+MAPFIT+'</script>'+ZOOM+'</body></html>')
