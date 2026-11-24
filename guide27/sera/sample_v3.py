# 세라핌 새 틀 견본(11-24 밤 목사님 지시 + GPT 감수 반영) — 11/24 사도행전 12:25–14:28
# 1쪽 ① 흐름 ② 성경 읽기 → 읽고 나서 마음에 남은 말씀 / 2쪽 ③ 눈여겨볼 것 ④ 본문 관찰(한 물음, 이유)
# 3쪽 ⑤ 하나님의 성품(근거 구절 → 성품 → 그 앞의 나) → 적용 → 나의 기도 / 4쪽 ⑥ 해설 ⑦ 함께 드리는 기도
import sys, os, asyncio, re
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import a5, a5_4p
from w1124 import W
from playwright.async_api import async_playwright
inl = a5.inl
L = lambda n: '<div class="ln"></div>' * n
S = dict(
 keep='읽으며 마음에 남은 말씀을 적고, 그 이유를 짧게 남겨 보세요.',
 obs_ref='14:22–23',
 obs='돌에 맞았던 바울은 더베에서 복음을 전한 뒤, 박해받았던 성들로 돌아갑니다(14:20–21). 사도들은 제자들을 격려하고 장로들을 세운 뒤, **왜 금식 기도 하며 그들을 주께 맡겼다고 생각합니까?**',
 obs_hint='본문을 살피며 이유를 적어 보세요.',
 god_ref='14:23, 27',
 god_fact='사도들은 떠나면서 제자들을 "그들이 믿는 주께" 맡깁니다. 그리고 돌아와 "하나님이 함께 행하신 모든 일"을 보고합니다.',
 god='하나님은 자기 백성과 함께 일하시고, 사람이 떠난 뒤에도 그들을 신실하게 돌보시는 분이십니다.',
 god_q='지금 내가 책임지고 있는 사람이나 일을 떠올려 보세요. 그것을 주님께 맡긴다는 말씀 앞에서 내 마음에는 무엇이 드러납니까?',
 ap_lead='사도들은 제자들을 돌보고, 기도하며 주께 맡겼습니다(14:22–23). **앞에서 떠올린 사람이나 일을 주께 맡기며, 내가 감당할 한 가지는 무엇입니까?**',
 ap_fu='이번 주 언제, 어떻게 하겠습니까?',
 pray='오늘 마음에 남은 말씀과 내 응답을 하나님께 말씀드립니다.',
)
CSS3 = '''
.kp{border:.4mm solid var(--c);border-radius:1.4mm;padding:2mm 3mm 1mm;margin-top:2.4mm;background:#fff}
.kp .kh{font-size:8.6pt;font-weight:700;color:var(--c);display:flex;justify-content:space-between}
.kp .kh small{font-weight:400;color:#777}
.kp .kq{margin:.6mm 0 .4mm}
.kp .kl{font-size:7.6pt;color:#888;margin-top:1mm}
.kp .ln{height:7mm}
.ref{display:inline-block;font-size:8pt;font-weight:700;color:var(--c);border:.3mm solid var(--c);border-radius:.8mm;padding:0 1.4mm;margin-right:1.6mm}
.oq{margin:1mm 0 .6mm;text-align:justify}.oh{font-size:8.4pt;color:#666;margin-bottom:.4mm}
.gf{font-size:9pt;color:#444;margin:.8mm 0 .4mm;text-align:justify}
.gs{background:var(--l);border-left:1mm solid var(--c);padding:1.4mm 2.6mm;margin:.8mm 0 1mm;font-weight:700}
.sub{display:flex;align-items:center;gap:1.6mm;margin:2.6mm 0 .6mm;font-size:9.4pt;font-weight:700;color:var(--c);border-top:.3mm solid #ccc;padding-top:1.8mm}
.sub i{font-style:normal;font-size:7.6pt;color:#fff;background:var(--c);border-radius:.8mm;padding:.2mm 1.4mm}
.lab4{display:flex;align-items:center;gap:1.8mm;font-size:10pt;font-weight:700;margin:3.4mm 0 .8mm;color:#222}
.lab4 b{display:inline-flex;width:4.6mm;height:4.6mm;border:.35mm solid var(--c);color:var(--c);border-radius:.8mm;align-items:center;justify-content:center;font-size:8pt}
.lab4 small{font-weight:400;font-size:7.8pt;color:#777;margin-left:auto}
.p4 .ans{flex:none}
'''
def pages():
    A, O, G, D = a5.blocks(W)
    i3 = next(k for k, x in enumerate(A) if '눈여겨볼 것' in x)
    p1 = [x for x in A[:i3] if 'class="wd' not in x and 'class="map' not in x]
    svg = open(os.path.join(H, W['map'])).read()
    i = next(k for k, x in enumerate(p1) if '오늘의 흐름' in x)
    p1.insert(i + 1, f'<div class="map mf">{svg}<div class="mcap sans">{inl(W["mapcap"])}</div></div>')
    p1.append(f'<div class="kp"><div class="kh sans">읽고 나서 바로 · 마음에 남은 말씀<small>③을 읽기 전에 씁니다</small></div><div class="kq">{S["keep"]}</div>'
              f'<div class="kl sans">장절과 말씀</div>{L(2)}<div class="kl sans">마음에 남은 이유</div>{L(2)}</div>')
    lab = lambda n, t, sm='': f'<div class="lab4 sans"><b>{n}</b>{t}{"<small>"+sm+"</small>" if sm else ""}</div>'
    p2 = ''.join(A[i3:]) + (f'<div class="sh sans"><span class="n">4</span>나의 묵상</div>' + lab(1, '본문 관찰', '오늘 본문을 더 살펴보는 한 길') +
          f'<div class="oq"><span class="ref sans">{S["obs_ref"]}</span>{inl(S["obs"])}</div><div class="oh sans">{S["obs_hint"]}</div><div class="ans">{L(4)}</div>')
    p3 = (f'<div class="sh sans" style="margin-top:0"><span class="n">4</span>나의 묵상<small>이어서</small></div>' + lab(2, '하나님의 성품', '본문이 보여 주는 하나님 앞에서 지금의 나') +
          f'<div class="gf"><span class="ref sans">{S["god_ref"]}</span>{inl(S["god_fact"])}</div><div class="gs">{inl(S["god"])}</div><div class="oq">{inl(S["god_q"])}</div><div class="ans">{L(4)}</div>'
          + lab(3, '적용') + f'<div class="oq">{inl(S["ap_lead"])}</div><div class="oq">→ {inl(S["ap_fu"])}</div><div class="ans">{L(3)}</div>'
          + lab(4, '나의 기도') + f'<div class="oh sans">{S["pray"]}</div><div class="ans">{L(3)}</div>')
    pr = ('<div class="pr4"><div class="sh sans"><span class="n">6</span>함께 드리는 기도</div><h4 class="sans">청년부 기도제목</h4>' + '<div class="pln"></div>' * 5
          + '<h4 class="sans">교회 기도제목</h4>' + '<div class="pln"></div>' * 3 + '</div>')
    D = [D[0].replace('<span class="n">6</span>해설', '<span class="n">5</span>쓴 뒤에 읽기 · 해설')] + D[1:]
    p4 = ''.join(D[:-1]) + pr
    return [''.join(p1), p2, p3, p4]
async def main(out):
    P = pages(); st = f'--c:{W["color"]};--l:{W["light"]};--hl:#F3E6A0'; run = W['title']
    pg = [f'<section class="p5 p4{" r" if i%2 else ""}" style="{st}"><div class="bx5{" b1" if i in (0,1) else ""}">{h}</div><span class="pn sans">{i+1}</span><span class="rn sans">{run}</span></section>' for i, h in enumerate(P)]
    doc = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{a5.CSS}{a5_4p.CSS2}{CSS3}</style></head><body><div class="x2">{pg[0]}{pg[1]}</div><div class="x2">{pg[2]}{pg[3]}</div></body></html>'
    async with async_playwright() as p:
        b = await p.chromium.launch(); g = await b.new_page(); await g.set_content(doc); await g.wait_for_timeout(400)
        await g.evaluate('()=>{' + open(os.path.join(H, 'fit4.js')).read() + '; const x=document.querySelectorAll(".x2"); fit4(x[0].querySelector(".p5"), x[1].querySelectorAll(".p5")[1]); }')
        bad = await g.evaluate('''()=>[...document.querySelectorAll('.p5')].map((p,i)=>{const b=p.firstElementChild;return [i+1, Math.round((b.scrollHeight-b.clientHeight)*25.4/96)]}).filter(x=>x[1]>0)''')
        print('넘침:', bad or '없음')
        await g.pdf(path=out, width='297mm', height='210mm', print_background=True)
        await g.set_viewport_size({'width': 1123, 'height': 794})
        for i, el in enumerate(await g.query_selector_all('.x2')): await el.screenshot(path=f'{os.path.splitext(out)[0]}_{i+1}.png')
        await b.close()
asyncio.run(main(sys.argv[1]))
