import asyncio, math
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter, Transformation
S='../sera/'
rows=[('12월 1일','대림절 1 · 소망','이사야 7–12장','흑암에 비치는 큰 빛'),('12월 8일','대림절 2 · 약속','이사야 32–35장','광야에 난 거룩한 길'),('12월 15일','대림절 3 · 준비','이사야 40–43장','광야에 길을 내시는 하나님'),('12월 22일','대림절 4 · 도래','미가 4–7장','작은 베들레헴에서 나올 목자'),('12월 25일','성탄절','마태복음 1–3장','약속대로 오신 왕'),('12월 29일','송구영신','이사야 60–62장','새 이름으로 부르시는 하나님')]
tr=''.join(f'<tr><td class="d">{a}</td><td class="s">{b}</td><td><b>{c}</b><br><span>{d}</span></td></tr>' for a,b,c,d in rows)
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A5;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"Noto Sans CJK KR",sans-serif;color:#222;-webkit-print-color-adjust:exact}}
.pg{{width:148mm;height:210mm;padding:22mm 16mm 14mm;position:relative}}
.k{{font-size:9pt;color:#5B3E8A;font-weight:700;letter-spacing:.1em}}
h1{{font-size:20pt;margin:2mm 0 1mm;font-weight:700}}
.sub{{font-size:9.5pt;color:#555;margin-bottom:8mm}}
table{{width:100%;border-collapse:collapse;font-size:9pt}}
td{{border-bottom:.25mm solid #ccc;padding:2.2mm 1mm;vertical-align:top}}
td.d{{width:20mm;font-weight:700}} td.s{{width:28mm;color:#5B3E8A}} td span{{color:#666;font-size:8.4pt}}
.how{{margin-top:8mm;font-family:"Noto Serif CJK KR",serif;font-size:9pt;line-height:1.75;color:#333}}
.how b{{font-family:"Noto Sans CJK KR",sans-serif}}
.ft{{position:absolute;bottom:9mm;left:16mm;font-size:7.5pt;color:#999}}</style></head><body><div class="pg">
<p class="k">부록</p><h1>대림절과 송구영신 묵상</h1><p class="sub">세라핌 청년 기도회에서 함께 쓰는 묵상지입니다</p>
<table>{tr}</table>
<div class="how"><p>한 회는 네 쪽입니다. <b>첫 쪽</b>에서 오늘의 흐름을 읽고, 성경을 펴서 표시하며 읽습니다. <b>펼친 두 쪽</b>에서 본문 관찰과 하나님의 성품을 하나 이상 골라 그 아래에 적습니다. 같은 번호를 고르면 관찰이 성품으로 이어집니다. <b>마지막 쪽</b>에서 해설과 성경 전체로를 읽고 함께 기도합니다.</p>
<p style="margin-top:3mm">대림절 네 주 동안 이사야와 미가에서 "길"이 어떻게 이어지는지 눈여겨보십시오.</p></div>
<p class="ft">부록</p></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(); await pg.set_content(H); await pg.wait_for_timeout(300)
        await pg.pdf(path='axtitle.pdf',format='A5',print_background=True); await b.close()
asyncio.run(main())
w=PdfWriter()
def add(f):
    for pgo in PdfReader(f).pages: w.add_page(pgo)
add('body.pdf'); add('axtitle.pdf')
A5=(419.53,595.28)
for k in ['1201','1208','1215','1222','1225','1229']:
    for pgo in PdfReader(S+f'세라핌_{k}.pdf').pages:
        s=A5[0]/float(pgo.mediabox.width)
        pgo.add_transformation(Transformation().scale(s,s)); pgo.mediabox.upper_right=(float(pgo.mediabox.width)*s,float(pgo.mediabox.height)*s)
        pgo.cropbox=pgo.mediabox
        w.add_page(pgo)
n=len(w.pages)+1
for _ in range((4-n%4)%4): add('blank.pdf')
add('back.pdf')
w.write('2026_체험판_12월_대림절.pdf'); print('쪽수',len(w.pages))
