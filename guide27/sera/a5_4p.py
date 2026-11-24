# 세라핌 묵상지 A5 4쪽(가이드북 글자 크기) → A4 가로 양면 한 장 (11-24 목사님)
# 앞면: 1쪽(①오늘의 흐름 ②성경 읽기 ③눈여겨볼 것) | 2쪽(④본문 관찰)   뒷면: 3쪽(⑤하나님의 성품) | 4쪽(⑥해설 ⑦기도, 대림절은 ⑦성경 전체로 ⑧기도)
# 말뜻은 뺍니다. 양면 인쇄는 '짧은 쪽으로 넘기기'.
# 쓰는 법: python3 a5_4p.py 출력.pdf w1124 [w1201 ...]
import sys, os, asyncio, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a5
from playwright.async_api import async_playwright
CSS2 = '''@page{size:297mm 210mm;margin:0}
.x2{display:flex;width:297mm;height:210mm;page-break-after:always;overflow:hidden}
.x2 .p5,.x2 .p5.r{padding:9mm 10mm 10mm 10mm;page-break-after:auto;flex:none}
.x2 .p5 .pn{left:10mm}.x2 .p5.r .pn{left:auto;right:10mm}
.b1{display:block!important}
.x2 .bx5{height:191mm}
.x2 .pn,.x2 .rn{bottom:4mm}'''
async def main(out, mods):
    body = ''
    for m in mods:
        w = importlib.import_module(m).W
        P = a5.four(w); run = f'{w.get("season","")} · {w["title"]}'.strip(' ·')
        st = f'--c:{w["color"]};--l:{w["light"]};--hl:{w.get("hl","#F3E6A0")}'
        pg = [f'<section class="p5 p4{" r" if i%2 else ""}" style="{st}"><div class="bx5{" b1" if i==0 else ""}">{h}</div><span class="pn sans">{i+1}</span><span class="rn sans">{run}</span></section>' for i, h in enumerate(P)]
        body += f'<div class="x2">{pg[0]}{pg[1]}</div><div class="x2">{pg[2]}{pg[3]}</div>'
    doc = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{a5.CSS}{CSS2}</style></head><body>{body}</body></html>'
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(doc); await pg.wait_for_timeout(400)
        bad = await pg.evaluate('''()=>[...document.querySelectorAll('.p5')].map((p,i)=>{const b=p.firstElementChild;return [i, Math.round((b.scrollHeight-b.clientHeight)*25.4/96)]}).filter(x=>x[1]>0)''')
        print('넘침(쪽 순번, mm):', bad or '없음')
        await pg.pdf(path=out, width='297mm', height='210mm', print_background=True)
        await pg.set_viewport_size({'width': 1123, 'height': 794})
        for i, el in enumerate(await pg.query_selector_all('.x2')): await el.screenshot(path=f'{os.path.splitext(out)[0]}_{i+1}.png')
        await b.close()
if __name__ == '__main__': asyncio.run(main(sys.argv[1], sys.argv[2:]))
