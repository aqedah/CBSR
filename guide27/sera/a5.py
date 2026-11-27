# 세라핌·절기 묵상지를 가이드북(A5) 크기와 글자 크기로 다시 짭니다. (11-24 목사님: 12월 체험판을 스프링 제본해서 세라핌 기도회에서 씀 — 글자가 가이드북 본문과 같아야 함)
# 한 회 = 8쪽: 읽기(2) · 본문 관찰(2, 펼침면) · 하나님의 성품(2, 펼침면) · 해설과 기도(2). 왼쪽 쪽에서 시작해야 관찰과 성품이 마주 봅니다.
# 쓰는 법: python3 a5.py 출력.pdf 첫쪽번호 w1201 w1208 ...   (첫쪽번호는 짝수 = 왼쪽)
import sys, os, re, html, importlib, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import inl
from playwright.async_api import async_playwright

CSS = '''
@page{size:148mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Noto Serif CJK KR","Noto Serif KR",serif;color:#111;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sans{font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif}
.p5{width:148mm;height:210mm;padding:13mm 18mm 11mm 10mm;position:relative;overflow:hidden;page-break-after:always;font-size:9.6pt;line-height:1.55}
.p5.r{padding:13mm 10mm 11mm 18mm}
.bx5{height:186mm;display:flex;flex-direction:column;overflow:hidden}
.pn{position:absolute;bottom:5.5mm;left:10mm;font-size:8pt;color:#777}
.p5.r .pn{left:auto;right:10mm}
.rn{position:absolute;bottom:5.5mm;right:18mm;font-size:7.5pt;color:#999}
.p5.r .rn{right:auto;left:18mm}
.hd{display:grid;grid-template-columns:19mm 1fr;align-items:center;border-bottom:.5mm solid var(--c);padding-bottom:1.6mm}
.hd.q3{grid-template-columns:19mm 1fr 13mm}
.hd .sq{display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:4.8pt;line-height:1;color:#555}
.hd .sq svg{width:10mm;height:10mm;display:block}.hd .sq span{margin-top:.7mm;white-space:nowrap}
.dt{border-right:.3mm solid var(--c);line-height:1}
.dt b{font-size:22pt;font-weight:300;color:var(--c)}
.dt b i{font-style:normal;font-size:11pt;opacity:.75;margin-right:.4mm}
.dt small{display:block;font-size:7.5pt;color:#555;margin-top:1mm}
.tt{padding-left:3.4mm}
.tt .lb{font-size:7.8pt;color:var(--c);font-weight:700;line-height:1.4}
.tt b{display:block;font-size:14pt;font-weight:700;line-height:1.25}
.tt span{font-size:9pt;color:#555}
.st{margin-top:1.4mm;background:var(--l);padding:.8mm 2.4mm;font-size:7.8pt}
.sh{display:flex;align-items:center;gap:1.6mm;font-size:10pt;font-weight:700;border-bottom:.3mm solid #bbb;padding-bottom:.6mm;margin:3.2mm 0 1.8mm}
.sh .n{width:4.8mm;height:4.8mm;border-radius:50%;background:var(--c);color:#fff;font-size:8pt;display:inline-flex;align-items:center;justify-content:center}
.sh small{margin-left:auto;font-size:7.4pt;font-weight:400;color:#777}
.blk p{margin-bottom:1.4mm;text-align:justify}
.wd{border-left:.8mm solid var(--c);background:var(--l);padding:1.2mm 2.4mm;font-size:8.6pt;line-height:1.5;margin-top:1mm}
.wd .k{font-weight:700;color:var(--c);margin-right:1.6mm}
.wd div{margin:.3mm 0}
.map{flex-shrink:0;border:.3mm solid #bbb;border-radius:1mm;overflow:hidden;margin:1mm 0 1.6mm}
.map img,.map svg{display:block;width:100%}
.mcap{font-size:7.4pt;color:#555;line-height:1.4;padding:.8mm 1.6mm;border-top:.3mm solid #ddd}
.mf{float:right;width:44mm;margin:.6mm 0 1mm 3mm}
.mf .mcap{font-size:6.8pt;padding:.5mm 1mm}
.p4 .op{padding:1.2mm 0 .4mm}
.p4 .bx5{display:flex;flex-direction:column}
.p4 .sh{margin:1.9mm 0 1mm}
.p4 .bx5.b1{line-height:1.41}
.p4 .b1 .mk{margin-bottom:1mm}
.p4 .b1 .lk{margin-bottom:1mm}
.p4 .b1 .blk p{margin-bottom:.8mm}
.p4 .b1 .scn{margin-bottom:1mm;gap:.8mm}
.p4 .b1 .scn span{font-size:7pt;padding:0 1.2mm}
.p4 .b1 .hd{padding-bottom:1mm}
.p4 .note{padding:2mm 3mm;line-height:1.6}
.scn{display:flex;flex-wrap:wrap;gap:1.2mm;margin-bottom:2mm}
.scn span{font-size:7.6pt;border:.3mm solid var(--c);color:var(--c);border-radius:1mm;padding:.2mm 1.6mm}
.mk{margin-bottom:2mm;text-align:justify}
.chip{display:inline-block;font-size:7.4pt;font-weight:700;border:.3mm solid var(--c);color:var(--c);border-radius:.8mm;padding:0 1.2mm;margin-right:1.4mm;line-height:1.5;vertical-align:.3mm;white-space:nowrap;font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif}
.mk:has(.rp){background:color-mix(in srgb,var(--c) 10%,#fff);border-left:.8mm solid var(--c);padding:0 1.2mm;border-radius:.6mm} /* 11-26: 대표 표시를 나머지와 구별 */
.rp{font-size:7.2pt;color:var(--c);font-weight:700;margin-right:1mm;font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif}
.hl{background:linear-gradient(transparent 35%,var(--hl) 35%)}
.ci{border:.3mm solid #222;border-radius:50%/60%;padding:0 1mm;display:inline-block;font-size:.9em;line-height:1.22;vertical-align:baseline} /* 11-25: 윗줄에 겹치지 않게 */
.wv{text-decoration:underline wavy;text-decoration-thickness:.22mm;text-underline-offset:.9mm}
.br{font-weight:700}
.lk{display:grid;grid-template-columns:4mm 1fr;gap:0 .8mm;margin-bottom:1.8mm;text-align:justify}
.lk .ck{color:var(--c);font-weight:700}
.gd{font-size:8.2pt;color:#444;background:#f3f3f3;border-radius:1mm;padding:1.2mm 2.2mm;margin-bottom:.6mm}
.gd b{color:var(--c)}
.op{display:grid;grid-template-columns:6mm 1fr;gap:0 1.4mm;padding:1.8mm 0 .8mm;text-align:justify}
.op .bx{width:4.6mm;height:4.6mm;border:.35mm solid #666;border-radius:.8mm;margin-top:.6mm;display:flex;align-items:center;justify-content:center;font-size:7.5pt;font-weight:700;color:var(--c)}
.op .v{font-size:9pt;color:#444;margin-bottom:.4mm}
.ans{flex:1 1 0;min-height:0;overflow:hidden;border-bottom:.4mm solid #999;margin-bottom:1mm}
.ln{border-bottom:.22mm solid #bbb;height:7.6mm}
.note{background:var(--l);border-top:.6mm solid var(--c);padding:2.8mm 3.4mm;line-height:1.75;text-align:justify}
.wh{display:grid;grid-template-columns:auto 1fr;gap:0 1.6mm;margin-bottom:1.6mm;text-align:justify}
.wh .chip{margin-top:.6mm;align-self:start;justify-self:start}
.wh b{font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;font-size:8.4pt;color:var(--c);margin-right:1.2mm}
.pr4{margin-top:auto;padding-top:1mm;flex:none}
.pr4 h4{font-size:8.6pt;margin:1.2mm 0 .2mm;color:var(--c)}
.pr4 .pln{height:6.6mm;line-height:6.6mm;font-size:9pt;padding:0 1.4mm;overflow:hidden;white-space:nowrap}
.shw .n{display:none}
.cp{font-size:8.6pt;color:#555;margin:.4mm 0 0}
.cp b{color:var(--c)}
.cpl{margin-bottom:1.4mm}.cpl .ln{border-bottom:.22mm dashed #aaa}
.gq{margin-top:.4mm}
.ap{display:grid;grid-template-columns:auto 1fr;gap:0 2mm;padding:2mm 0 .4mm;border-top:.3mm solid #ccc;margin-top:1mm}
.apl{font-size:8pt;font-weight:700;color:#fff;background:var(--c);border-radius:.8mm;padding:.3mm 1.6mm;align-self:start;margin-top:.6mm}
.ap .fu{margin-top:.6mm;color:#333}
.pr{flex:1 1 auto;min-height:62mm;display:flex;flex-direction:column;overflow:hidden}
.pr h4{font-size:8.6pt;margin:2mm 0 .6mm;color:var(--c)}
.pr .ya{flex:3 1 0;min-height:0;overflow:hidden}.pr .ca{flex:2 1 0;min-height:0;overflow:hidden}
.prow{display:grid;grid-template-columns:20mm 1fr;border-bottom:.22mm solid #bbb;height:7.6mm}
.prow span{border-right:.22mm solid #ddd}
.pln{border-bottom:.22mm solid #bbb;height:7.6mm}
'''

# 11-27 목사님: 세라핌 묵상지 머리에 스토리 QR. 주소는 https://aqedah.github.io/CBSR/?sera=회 키(1201 …).
# 앱은 그 회 스토리가 있으면 스토리를, 없으면 그 회 묵상지(season.html)를 엽니다.
SERA_QR = {'1201', '1208', '1215', '1222', '1225', '1229'}
def seraQR(w):
    k = w.get('key', '')
    if k not in SERA_QR: return ''
    import segno
    q = segno.make(f'https://aqedah.github.io/CBSR/?sera={k}', error='m', micro=False)
    m = list(q.matrix); n = len(m)
    rects = ''.join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y, r in enumerate(m) for x, c in enumerate(r) if c)
    return f'<div class="sq"><svg viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><g fill="#000">{rects}</g></svg><span>스토리 보기</span></div>'
def blocks(w):
    m, d = re.match(r'(\d+)월 (\d+)일', w['date']).groups()
    wd = re.search(r'\((.)\)', w['date']).group(1)
    A = []
    sq = seraQR(w)
    A.append(f'''<div class="hd sans{' q3' if sq else ''}"><div class="dt"><b><i>{m}/</i>{d}</b><small>{wd}요일</small></div><div class="tt"><div class="lb">{w['label']} · {w.get('season','')}</div><b>{w['title']}</b><span>{w['sub']}</span></div>{sq}</div>
<div class="st sans">성경 읽기 약 <b>{round(w['vv']/7.5)}분</b></div>''')
    A.append('<div class="sh sans"><span class="n">1</span>오늘의 흐름</div>')
    for p in w['flow']: A.append(f'<div class="blk"><p>{inl(p)}</p></div>')
    if w.get('map'):
        svg = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), w['map'])).read()
        A.append(f'<div class="map">{svg}<div class="mcap sans">{inl(w.get("mapcap",""))}</div></div>')
    A.append('<div class="wd sans"><span class="k">말뜻</span>' + ''.join(f'<div><b>{inl(a)}</b> {inl(b)}</div>' for a, b in w['words']) + '</div>')
    A.append('<div class="sh sans"><span class="n">2</span>성경 읽기<small>성경책을 펴고 읽으며 표시합니다</small></div>')
    A.append('<div class="scn">' + ''.join(f'<span class="sans">{s}</span>' for s in w['scenes']) + '</div>')
    for k in w['marks']: A.append(f'<div class="mk"><span class="chip">{k["tool"]}</span>{"<span class=rp>대표</span>" if k.get("rep") else ""}{inl(k["text"])}</div>')
    A.append('<div class="sh sans"><span class="n">3</span>눈여겨볼 것<small>✓ ②에서 표시한 곳의 풀이</small></div>')
    for l in w['looks']: A.append(f'<div class="lk"><span class="ck">{"✓" if l["ck"] else ""}</span><span><span class="chip">{l["tool"]}</span>{inl(l["text"])}</span></div>')
    D = []
    D.append('<div class="sh sans" style="margin-top:0"><span class="n">6</span>해설<small>다 쓴 뒤에 읽고, 내 묵상과 비교해 봅니다</small></div>')
    D.append(f'<div class="note">{inl(w["note"])}</div>')
    if w.get('whole'):
        # 성경 전체로는 큰 번호를 달지 않습니다(11-24 목사님). 오늘의 기도가 7번.
        D.append(f'<div class="sh sans shw">성경 전체로<small>{w.get("whole_title","")}</small></div>')
        for x in w['whole']: D.append(f'<div class="wh"><span class="chip">{x["lab"]}</span><span><b>{x["ref"]}</b>{inl(x["text"])}</span></div>')
    D.append(prayer())
    O, G = qparts(w, 14, 3, split=True)
    return A, O, G, D

def prayer():
    return ('<div class="pr4"><div class="sh sans"><span class="n">7</span>오늘의 기도</div><h4 class="sans">청년부 기도제목</h4>'
            + '<div class="pln"></div>' * 5 + '<h4 class="sans">교회 기도제목</h4>' + '<div class="pln"></div>' * 3 + '</div>')

def josa(ref): return '를' if ref.strip()[-1] in '2459' else '을'
OG = '<b>가와 나 가운데 하나를 골라</b> 바로 아래 칸에 적습니다. 시간이 남으면 다른 하나도 적어 봅니다.'
GG = '본문 관찰에서 <b>고른 쪽과 같은 쪽을 고르면</b> 관찰이 성품으로 이어집니다. 성품을 적은 뒤 적용으로 넘어갑니다.'
def qparts(w, nans, ncopy, split):
    """관찰 가/나, 성품 가/나, 적용. split=True면 8쪽용(관찰 2쪽, 성품 2쪽), 아니면 4쪽용(관찰 1쪽, 성품과 적용 1쪽)."""
    L = lambda n: '<div class="ln"></div>' * n
    sh = lambda n, t, more: f'<div class="sh sans" style="margin-top:0"><span class="n">{n}</span>{t}{"<small>이어서</small>" if more else ""}</div>'
    op = lambda lab, body: f'<div class="op"><div class="bx sans">{lab}</div><div>{body}</div></div><div class="ans">{L(nans)}</div>'
    def gbody(g):
        if g.get('copy'):
            return f'<div class="cp sans"><b>{g["copy"]}</b>{josa(g["copy"])} 성경에서 찾아 옮겨 적어 보세요.</div><div class="cpl">{L(ncopy)}</div><div class="gq">{inl(g["q"])}</div>'
        return f'<div class="v">{inl(g["v"])}</div>{inl(g["q"])}'
    ob = [op(l, inl(q)) for l, q in zip('가나', w['obs'])]
    gb = [op(l, gbody(g)) for l, g in zip('가나', w['god'])]
    a = w.get('apply')
    ap = (f'<div class="ap"><div class="apl sans">적용</div><div>{inl(a["lead"])}<div class="fu">→ {inl(a["fu"])}</div></div></div><div class="ans">{L(nans)}</div>') if a else ''
    o0, g0 = sh(4, '본문 관찰', 0) + f'<div class="gd sans">{OG}</div>', sh(5, '하나님의 성품', 0) + f'<div class="gd sans">{GG}</div>'
    if split:
        return [o0 + ob[0], sh(4, '본문 관찰', 1) + ''.join(ob[1:])], [g0 + gb[0], sh(5, '하나님의 성품', 1) + ''.join(gb[1:]) + ap]
    return [o0 + ''.join(ob)], [g0 + ''.join(gb) + ap]

def four(w):
    """한 회 A5 4쪽: ①②③ 한 쪽, ④ 한 쪽, ⑤와 적용 한 쪽, ⑥(성경 전체로)⑦ 한 쪽. 말뜻은 뺍니다(11-24 목사님)."""
    A, O, G, D = blocks(w)
    p1 = [x for x in A if 'class="wd' not in x and 'class="map' not in x]
    if w.get('map'):
        svg = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), w['map'])).read()
        mp = f'<div class="map mf">{svg}<div class="mcap sans">{inl(w.get("mapcap",""))}</div></div>'
        i = next(k for k, x in enumerate(p1) if '오늘의 흐름' in x)
        p1.insert(i + 1, mp)
    O4, G4 = qparts(w, 8, 2, split=False)
    return [''.join(p1), O4[0], G4[0], ''.join(D)]

JS = r'''
(start)=>{
  const src=[...document.querySelectorAll('.src')]; const out=document.getElementById('out'); let pn=start;
  const mk=(w,run)=>{ const p=document.createElement('section'); p.className='p5'+(pn%2?' r':''); p.style.cssText=w.dataset.style;
    p.innerHTML=`<div class="bx5"></div><span class="pn sans">${pn}</span><span class="rn sans">${run}</span>`; out.appendChild(p); pn++; return p.firstElementChild; };
  const flow=(w,html,run,even)=>{ let box=mk(w,run); const n0=out.children.length;
    for(const h of html){ const t=document.createElement('template'); t.innerHTML=h; const el=t.content.firstElementChild; box.appendChild(el);
      if(box.scrollHeight>box.clientHeight+1 && box.children.length>1){ box.removeChild(el); const carry=[]; while(box.children.length>1 && /\b(sh|scn)\b/.test(box.lastElementChild.className)) carry.unshift(box.removeChild(box.lastElementChild));
        box=mk(w,run); carry.forEach(c=>box.appendChild(c)); box.appendChild(el); const f0=box.firstElementChild; if(f0.classList.contains('sh')||f0.classList.contains('note')) f0.style.marginTop='0'; } }
    if(even && (out.children.length-n0+1)%2){ const pr=box.querySelector(':scope > .pr4'); if(pr && box.children.length>1){ box.removeChild(pr); const b=mk(w,run); b.appendChild(pr); pr.firstElementChild.style.marginTop='0'; } else { const b=mk(w,run); b.innerHTML='<div class="sh sans" style="margin-top:0">메모</div><div class="ans" style="border-bottom:0">'+'<div class="ln"></div>'.repeat(30)+'</div>'; } } };
  const fixed=(w,pages,run)=>{ for(const h of pages){ const b=mk(w,run); b.innerHTML=h; } };
  for(const w of src){ const J=JSON.parse(w.dataset.j); const run=J.run;
    flow(w,J.A,run,true); fixed(w,J.O,run); fixed(w,J.G,run); flow(w,J.D,run,true); }
  /* 넘침 검사 */
  const bad=[]; out.querySelectorAll('.p5').forEach(p=>{const b=p.firstElementChild; if(b.scrollHeight>b.clientHeight+1 && !b.querySelector('.ans')) bad.push(p.querySelector('.pn').textContent)});
  return {pages:out.children.length,bad};
}
'''

async def main(out, start, mods):
    import json
    src = ''
    for m in mods:
        w = importlib.import_module(m).W
        A, O, G, D = blocks(w)
        mm, dd = re.match(r'(\d+)월 (\d+)일', w['date']).groups()
        run = f'{w.get("season","")} · {w["title"]}'
        src += f'<div class="src" hidden data-style="--c:{w["color"]};--l:{w["light"]};--hl:{w.get("hl","#F3E6A0")}" data-j="{html.escape(json.dumps(dict(A=A,O=O,G=G,D=D,run=run),ensure_ascii=False))}"></div>'
    doc = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{src}<div id="out"></div></body></html>'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(doc); await pg.wait_for_timeout(300)
        r = await pg.evaluate(JS, start)
        print('쪽', r['pages'], '넘침', r['bad'] or '없음')
        await pg.pdf(path=out, width='148mm', height='210mm', print_background=True)
        await pg.set_viewport_size({'width': 600, 'height': 900})
        els = await pg.query_selector_all('.p5')
        os.makedirs('a5shots', exist_ok=True)
        for i, el in enumerate(els): await el.screenshot(path=f'a5shots/{i+1:02d}.png')
        await b.close()

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1], int(sys.argv[2]), sys.argv[3:]))
