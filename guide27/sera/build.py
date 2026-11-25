import sys, re, html, importlib, asyncio, os
from playwright.async_api import async_playwright
H = os.path.dirname(os.path.abspath(__file__))
def inl(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\{형:(.+?)\}', r'<span class="hl">\1</span>', s)
    s = re.sub(r'\{동:(.+?)\}', r'<span class="ci">\1</span>', s)
    s = re.sub(r'\{물:(.+?)\}', r'<span class="wv">\1</span>', s)
    s = re.sub(r'\{괄:(.+?)\}', r'<span class="br">[\1]</span>', s)
    return s
def lines(n, cls='ln'): return ''.join(f'<div class="{cls}"></div>' for _ in range(n))
CSS = '''
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Noto Serif CJK KR","Noto Serif KR",serif;color:#222;font-size:10.4pt;line-height:1.62;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sans{font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif}
.pg{width:210mm;height:297mm;padding:13mm 16mm 12mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column}
.ft{position:absolute;bottom:7mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:7.5pt;color:#999}
.hd{display:grid;grid-template-columns:26mm 1fr auto;align-items:center;height:20mm;border-bottom:.6mm solid var(--c)}
.dt{border-right:.3mm solid var(--c);height:100%;display:flex;flex-direction:column;justify-content:center}
.dt b{font-size:30pt;font-weight:300;line-height:1;color:var(--c)}
.dt b i{font-style:normal;font-size:15pt;opacity:.75;margin-right:.6mm}
.dt small{font-size:8.5pt;color:#555;margin-top:1.2mm}
.tt{padding-left:5mm}
.tt b{display:block;font-size:19pt;font-weight:700;line-height:1.2}
.tt span{font-size:10.5pt;color:#555}
.lb{text-align:right;font-size:8.5pt;color:#555;line-height:1.5}
.lb b{display:block;color:var(--c);font-size:10pt}
.st{margin-top:1.6mm;background:var(--l);padding:1.2mm 3mm;font-size:8.5pt;display:flex;justify-content:space-between}
.sec{margin-top:5mm}
.sh{display:flex;align-items:center;gap:2.4mm;font-size:12pt;font-weight:700;border-bottom:.3mm solid #bbb;padding-bottom:1.2mm;margin-bottom:2.4mm}
.sh .n{width:6.4mm;height:6.4mm;border-radius:50%;background:var(--c);color:#fff;font-size:9.5pt;display:inline-flex;align-items:center;justify-content:center}
.sh small{margin-left:auto;font-size:8pt;font-weight:400;color:#777}
.flow p{margin-bottom:1.6mm}
.fm{display:grid;grid-template-columns:1fr 72mm;gap:4mm;align-items:start}
.map{border:.3mm solid #bbb;border-radius:1mm;overflow:hidden}
.fm .wd span{white-space:normal}
.map img,.map svg{display:block;width:100%}
.mcap{font-size:7.6pt;color:#555;line-height:1.4;padding:1mm 1.6mm;background:#fff;border-top:.3mm solid #ddd}
.wd{margin-top:2mm;border-left:1mm solid var(--c);background:var(--l);padding:1.6mm 3mm;font-size:9pt;line-height:1.55}
.wd .k{font-weight:700;color:var(--c);margin-right:2mm}
.wd span{margin-right:3.4mm;white-space:nowrap}
.wd span b{font-weight:700}
.scn{display:flex;flex-wrap:wrap;gap:1.6mm;margin-bottom:2.6mm}
.scn span{font-size:8pt;border:.3mm solid var(--c);color:var(--c);border-radius:1mm;padding:.4mm 2mm}
.mk{padding:1.8mm 2.4mm;margin-bottom:1.4mm;border-radius:1mm}
.chip{display:inline-block;font-size:7.8pt;font-weight:700;border:.35mm solid var(--c);color:var(--c);border-radius:1mm;padding:0 1.4mm;margin-right:1.6mm;line-height:1.5;vertical-align:.3mm;white-space:nowrap}
.rp{font-size:7.5pt;color:var(--c);font-weight:700;margin-right:1mm}
.hl{background:linear-gradient(transparent 35%,var(--hl) 35%)}
.ci{border:.35mm solid #222;border-radius:50%/60%;padding:0 1.2mm}
.wv{text-decoration:underline wavy;text-decoration-thickness:.25mm;text-underline-offset:1mm}
.br{font-weight:700}
.lk{border:.3mm solid #ccc;border-radius:1.2mm;padding:3mm 3.6mm}
.lk p{margin-bottom:1.8mm;display:grid;grid-template-columns:5mm auto 1fr;align-items:start}
.lk p .chip{margin-top:.9mm}
.lk p:last-child{margin-bottom:0}
.ck{color:var(--c);font-weight:700}
.op{display:grid;grid-template-columns:8mm 1fr;gap:0 2mm;padding:2.6mm 0;border-bottom:.25mm dashed #ccc}
.op .bx{width:5.4mm;height:5.4mm;border:.4mm solid #666;border-radius:1mm;margin-top:1mm;display:flex;align-items:center;justify-content:center;font-size:8pt;font-weight:700;color:var(--c)}
.op .v{font-size:9.6pt;color:#444}
.guide{font-size:8.6pt;color:#666;margin-bottom:1.6mm}
.wr{margin-top:4mm;flex:1;overflow:hidden;min-height:0}
.wr .lab{font-size:8.6pt;color:#666;margin-bottom:1mm}
.ln{border-bottom:.25mm solid #bbb;height:9.2mm}
.note{background:var(--l);border-top:.8mm solid var(--c);padding:4mm 5mm;font-size:10.4pt;line-height:1.8;text-align:justify}
.note .end{font-weight:700}
.pr h4{font-size:10pt;margin:3mm 0 1mm;color:var(--c)}
.prow{display:grid;grid-template-columns:24mm 1fr;border-bottom:.25mm solid #bbb;height:8.4mm;align-items:end}
.prow span,.prow i,.pln{font-style:normal;font-size:9.4pt;line-height:8mm;height:8mm;white-space:nowrap;overflow:hidden;outline:none;padding:0 1.6mm;color:#222}
.prow span{border-right:.25mm solid #ddd}
.pln{border-bottom:.25mm solid #bbb;height:8.4mm;display:block}
[contenteditable]:focus{background:#fffbe6}
.qs{flex:1;display:flex;flex-direction:column;min-height:0}
.qs .op{border-bottom:0;padding:2mm 0 1mm}
.ans{flex:1 1 0;min-height:0;overflow:hidden;border-bottom:.45mm solid #999;margin-bottom:1mm}
.ans .ln{height:8.4mm}
.gd{font-size:8.8pt;color:#444;background:#f4f4f4;border-radius:1mm;padding:1.6mm 3mm;margin-bottom:.6mm}
.gd b{color:var(--c)}
.cp{font-size:9pt;color:#555}.cp b{color:var(--c)}
.cpl{margin-bottom:1.6mm}.cpl .ln{border-bottom:.25mm dashed #aaa;height:8.4mm}
.gq{margin-top:.6mm}
.ap{display:grid;grid-template-columns:auto 1fr;gap:0 2.4mm;padding:2.4mm 0 1mm;border-top:.3mm solid #ccc;margin-top:1mm}
.apl{font-size:8.4pt;font-weight:700;color:#fff;background:var(--c);border-radius:1mm;padding:.4mm 1.8mm;align-self:start;margin-top:.8mm}
.ap .fu{margin-top:.8mm;color:#333}
.pr{margin-top:auto}
.whole p{display:grid;grid-template-columns:auto 1fr;gap:0 2mm;font-size:9.3pt;line-height:1.6;margin-bottom:1.6mm;text-align:justify}
.whole p .chip{margin-top:.8mm;align-self:start;justify-self:start}
.whole p b{font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;font-size:8.6pt;color:var(--c);margin-right:1.4mm}
'''
def page1(w):
    m, d = re.match(r'(\d+)월 (\d+)일 \((.)\)', w['date']).groups()[:2]
    wd = re.search(r'\((.)\)', w['date']).group(1) + '요일'
    lab = f"<b>{w['label']}</b>{w.get('season','')}"
    hd = f'''<div class="hd sans"><div class="dt"><b><i>{m}/</i>{d}</b><small>{wd}</small></div><div class="tt"><b>{w['title']}</b><span>{w['sub']}</span></div><div class="lb">{lab}</div></div>
<div class="st sans"><span>성경 읽기 약 <b>{round(w['vv']/7.5)}분</b></span><span>{w.get('strip','')}</span></div>'''
    flow = ''.join(f'<p>{inl(p)}</p>' for p in w['flow'])
    wds = ''.join(f'<span><b>{inl(a)}</b> {inl(b)}</span> ' for a, b in w['words'])
    marks = ''.join(f'<div class="mk{" rep" if k.get("rep") else ""}"><span class="chip sans">{k["tool"]}</span>{"<span class=\"rp sans\">대표</span> " if k.get("rep") else ""}{inl(k["text"])}</div>' for k in w['marks'])
    looks = ''.join(f'<p><span class="ck">{"✓" if l["ck"] else ""}</span><span class="chip sans">{l["tool"]}</span><span>{inl(l["text"])}</span></p>' for l in w['looks'])
    scn = ''.join(f'<span class="sans">{s}</span>' for s in w['scenes'])
    wdb = f'<div class="wd sans"><span class="k">말뜻</span>{wds}</div>'
    mp = w.get('map')
    if mp:
        svg = open(os.path.join(H, mp)).read()
        flowmap = f'<div class="fm"><div>{flow}{wdb}</div><div class="map">{svg}<div class="mcap sans">{inl(w.get("mapcap",""))}</div></div></div>'
    else:
        flowmap = flow + wdb
    return f'''<section class="pg">{hd}
<div class="sec flow"><div class="sh sans"><span class="n">1</span>오늘의 흐름</div>{flowmap}</div>
<div class="sec"><div class="sh sans"><span class="n">2</span>성경 읽기<small>성경책을 펴고 읽으며 표시합니다</small></div><div class="scn">{scn}</div>{marks}</div>
<div class="sec"><div class="sh sans"><span class="n">3</span>눈여겨볼 것<small>✓ ②에서 표시한 곳의 풀이</small></div><div class="lk">{looks}</div></div>
<div class="ft sans"><span>{w['label']} · {w['date']}</span><span>1</span></div></section>'''
def josa(ref): return '를' if ref.strip()[-1] in '2459' else '을'
def op(lab, body, n=12): return f'<div class="op"><div class="bx sans">{lab}</div><div>{body}</div></div><div class="ans">{lines(n)}</div>'
def page2(w):
    ops = ''.join(op(l, inl(q)) for l, q in zip('가나', w['obs']))
    return f"""<section class="pg"><div class="sh sans"><span class="n">4</span>본문 관찰</div>
<div class="gd sans"><b>가와 나 가운데 하나를 골라</b> 바로 아래 칸에 적습니다. 시간이 남으면 다른 하나도 적어 봅니다.</div>
<div class="qs">{ops}</div><div class="ft sans"><span>{w['title']}</span><span>2</span></div></section>"""
def gbody(g):
    if g.get('copy'):
        return f'<div class="cp sans"><b>{g["copy"]}</b>{josa(g["copy"])} 성경에서 찾아 옮겨 적어 보세요.</div><div class="cpl">{lines(2)}</div><div class="gq">{inl(g["q"])}</div>'
    return f'<div class="v">{inl(g["v"])}</div>{inl(g["q"])}'
def page3(w):
    ops = ''.join(op(l, gbody(g)) for l, g in zip('가나', w['god']))
    a = w.get('apply')
    ap = f'<div class="ap"><div class="apl sans">적용</div><div>{inl(a["lead"])}<div class="fu">→ {inl(a["fu"])}</div></div></div><div class="ans">{lines(12)}</div>' if a else ''
    return f"""<section class="pg"><div class="sh sans"><span class="n">5</span>하나님의 성품</div>
<div class="gd sans">본문 관찰에서 <b>고른 쪽과 같은 쪽을 고르면</b> 관찰이 성품으로 이어집니다. 성품을 적은 뒤 적용으로 넘어갑니다.</div>
<div class="qs">{ops}{ap}</div><div class="ft sans"><span>{w['title']}</span><span>3</span></div></section>"""
def page4(w, edit=False):
    note = inl(w['note'])
    ce = ' contenteditable="true"' if edit else ''
    wh = w.get('whole'); whole = ''
    if wh:
        # 성경 전체로는 큰 번호를 달지 않습니다(11-24 목사님). 오늘의 기도가 7번.
        whole = f'<div class="sec whole"><div class="sh sans">성경 전체로<small>{w.get("whole_title","오늘 본문이 성경의 다른 자리와 이어집니다")}</small></div>' + ''.join(f'<p><span class="chip sans">{x["lab"]}</span><span><b>{x["ref"]}</b>{inl(x["text"])}</span></p>' for x in wh) + '</div>'
    yrows = ''.join(f'<div class="pln sans"{ce} data-k="y{i}"></div>' for i in range(5))
    crows = ''.join(f'<div class="pln sans"{ce} data-k="c{i}"></div>' for i in range(3))
    return f"""<section class="pg"><div class="sh sans"><span class="n">6</span>해설<small>다 쓴 뒤에 읽고, 내 묵상과 비교해 봅니다</small></div><div class="note">{note}</div>{whole}
<div class="sec pr"><div class="sh sans"><span class="n">7</span>오늘의 기도</div>
<h4 class="sans">청년부 기도제목</h4>{yrows}
<h4 class="sans">교회 기도제목</h4>{crows}
</div><div class="ft sans"><span>{w['title']}</span><span>4</span></div></section>"""
def doc(ws):
    body = ''
    for w in ws:
        body += f'<div style="--c:{w["color"]};--l:{w["light"]};--hl:{w.get("hl", "#F3E6A0")}">' + page1(w) + page2(w) + page3(w) + page4(w) + '</div>'
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
async def pdf(ws, out, shots=False):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc(ws)); await pg.wait_for_timeout(300)
        # 넘침 검사
        over = await pg.evaluate('''()=>[...document.querySelectorAll('.pg')].map((s,i)=>{const r=s.getBoundingClientRect();let m=0;s.querySelectorAll('*').forEach(e=>{if(e.classList.contains('ft'))return;const b=e.getBoundingClientRect();if(b.bottom>m)m=b.bottom});return [i+1,Math.round((m-r.bottom)*25.4/96)]}).filter(x=>x[1]>-10)''')
        print('쪽 아래 여유가 10mm 안 되는 쪽(mm 넘침이 양수):', over)
        await pg.pdf(path=out, format='A4', print_background=True)
        if shots:
            await pg.set_viewport_size({'width': 794, 'height': 1123})
            n = await pg.evaluate("document.querySelectorAll('.pg').length")
            for i in range(n):
                el = (await pg.query_selector_all('.pg'))[i]; await el.screenshot(path=f'{H}/shot_{i+1}.png')
        await b.close()
if __name__ == '__main__':
    mods = sys.argv[2:]; ws = [importlib.import_module(m).W for m in mods]
    asyncio.run(pdf(ws, sys.argv[1], shots=True))
