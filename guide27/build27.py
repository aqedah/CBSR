import re,json,sys
css=open('css.css').read()+open('extra.css').read()
DIST=open('dist.js').read()
def vs(t): return re.sub(r'(?<=\()([^()]*\d+:\d+[^()]*)(?=\))',r'<span class="vs">\1</span>',t)
def vsm(t): return re.sub(r'(?<![\d:>])(\d+:\d+(?:–\d+)?(?:(?:, |; )(?:\d+:)?\d+(?:–\d+)?)*)(?=에서|까지|과 |와 )',r'<span class="vs">\1</span>',vs(t))
WDN={'월':'월요일','화':'화요일','수':'수요일','목':'목요일','금':'금요일','토':'토요일','일':'일요일'}
def page(D,pn=22):
    date=D['date'].split(' (')[0]; wd=WDN[D['date'].split('(')[1][0]]
    pic=D.get('pic')
    look=''.join(f'<div class="i">{"<span class=ck>✓</span>" if x["ck"] else ""}<span class="chip">{x["tool"]}</span>{vs(x["text"])}</div>' for x in D['looks'])
    lookblk=(f'<div class="two"><div class="c1"><div class="box lk">{look}</div></div><div class="c2"><div class="pic"><div class="im"><img src="{pic[0]}" alt=""></div><div class="cap">{pic[1]}</div></div></div></div>' if pic else f'<div class="box lk">{look}</div>')
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
days=json.load(open(sys.argv[1]))
out=''.join(page(D,20+2*i) for i,D in enumerate(days))
ZOOM="<script>(function(){function z(){const sp=document.querySelector('.spread');if(!sp)return;document.body.style.zoom=1;const w=sp.getBoundingClientRect().width;document.body.style.zoom=Math.min(1,(innerWidth-8)/w);}z();addEventListener('resize',z);})();</script>"
open(sys.argv[2],'w').write('<!doctype html><html><head><meta charset="utf-8"><title>2027 새 틀 1권</title><style>'+css+'</style></head><body>'+out+'<script>'+DIST+'</script>'+ZOOM+'</body></html>')
