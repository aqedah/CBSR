import asyncio
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
rows=[('12월 1일','대림절 1 · 소망','이사야 7–12장','흑암에 비치는 큰 빛',70),('12월 8일','대림절 2 · 약속','이사야 32–35장','광야에 난 거룩한 길',74),('12월 15일','대림절 3 · 준비','이사야 40–43장','광야에 길을 내시는 하나님',78),('12월 22일','대림절 4 · 도래','미가 4–7장','작은 베들레헴에서 나올 목자',82),('12월 25일','성탄절','마태복음 1–3장','약속대로 오신 왕',86),('12월 29일','송구영신','이사야 60–62장','새 이름으로 부르시는 하나님',90)]
tr=''.join(f'<tr><td class="d">{a}</td><td class="s">{b}</td><td><b>{c}</b><br><span>{d}</span></td><td class="pg">{p}</td></tr>' for a,b,c,d,p in rows)
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:148mm 210mm;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"Noto Sans CJK KR",sans-serif;color:#111;-webkit-print-color-adjust:exact}}
.p{{width:148mm;height:210mm;padding:22mm 18mm 14mm 10mm;position:relative;page-break-after:always}} .p.r{{padding:22mm 10mm 14mm 18mm}}
.k{{font-size:9pt;color:#5B3E8A;font-weight:700;letter-spacing:.1em}}
h1{{font-size:19pt;margin:2mm 0 1mm}} .sub{{font-size:9.4pt;color:#555;margin-bottom:8mm}}
table{{width:100%;border-collapse:collapse;font-size:9.2pt}} td{{border-bottom:.25mm solid #ccc;padding:2.4mm 1mm;vertical-align:top}}
td.d{{width:19mm;font-weight:700}} td.s{{width:27mm;color:#5B3E8A}} td span{{color:#666;font-size:8.6pt}} td.pg{{width:8mm;text-align:right;color:#777}}
h2{{font-size:11pt;margin:0 0 3mm;color:#5B3E8A}}
.t{{font-family:"Noto Serif CJK KR",serif;font-size:9.6pt;line-height:1.75;text-align:justify;margin-bottom:3mm}} .t b{{font-family:"Noto Sans CJK KR",sans-serif}}
ol{{font-family:"Noto Serif CJK KR",serif;font-size:9.6pt;line-height:1.7;padding-left:5mm;margin-bottom:4mm}} li{{margin-bottom:1.4mm}}
.gil{{background:#EEE9F5;border-left:.8mm solid #5B3E8A;padding:2.4mm 3mm;font-family:"Noto Serif CJK KR",serif;font-size:9.2pt;line-height:1.7}}
.pn{{position:absolute;bottom:5.5mm;left:10mm;font-size:8pt;color:#777}} .p.r .pn{{left:auto;right:10mm}}</style></head><body>
<div class="p"><p class="k">부록</p><h1>대림절과 송구영신 묵상</h1><p class="sub">세라핌 청년 기도회에서 함께 쓰는 묵상지입니다</p><table>{tr}</table><span class="pn">68</span></div>
<div class="p r"><h2>이렇게 씁니다</h2><p class="t">한 회는 네 쪽입니다. 앞의 하루 지면과 같은 걸음으로 갑니다.</p>
<ol><li><b>읽기</b> 오늘의 흐름과 본문 구조를 보고, 성경을 펴서 표시하며 읽습니다.</li>
<li><b>마음에 남은 말씀</b> 읽고 나서 바로, 마음에 남은 말씀과 그 이유를 적습니다. 궁금하거나 걸리는 말씀도 좋습니다.</li>
<li><b>나의 묵상</b> 눈여겨볼 것을 확인한 뒤 본문 관찰, 하나님의 성품, 적용, 나의 기도를 차례로 적습니다. 관찰 물음은 오늘 본문을 더 살펴보는 한 길입니다.</li>
<li><b>쓴 뒤에 읽기</b> 해설과 성경 전체로를 읽고, 내 묵상과 비교해 봅니다.</li>
<li><b>함께 드리는 기도</b> 청년부와 교회의 기도제목을 적고 함께 기도합니다.</li></ol>
<div class="gil">대림절 네 주 동안 이사야와 미가에서 <b>"길"</b>이 어떻게 이어지는지 눈여겨보십시오. 남은 자를 위한 "큰 길"(사 11:16)에서 시작해, 광야에 난 거룩한 "대로"(35:8), "광야에 길을" 내시는 하나님(43:19), "그의 길로 행하리라"는 열방(미 4:2)을 지나, 성탄절에는 "주의 길을 준비하라"는 요한의 외침(마 3:3)에 이릅니다. 송구영신에는 "백성이 올 길을 닦으라"(사 62:10)는 부름을 듣습니다.</div>
<span class="pn">69</span></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(); await pg.set_content(H); await pg.wait_for_timeout(300)
        await pg.pdf(path='axtitle.pdf',width='148mm',height='210mm',print_background=True); await b.close()
asyncio.run(main())
w=PdfWriter(); pages=[]
for f in ['body.pdf','axtitle.pdf','appx_a5.pdf']: pages+=list(PdfReader(f).pages)
blank=PdfReader('blank.pdf').pages[0]; back=PdfReader('back.pdf').pages[0]
n=len(pages)+1
pages+= [blank]*((4-n%4)%4) + [back]
for x in pages: w.add_page(x)
w.write('2026_체험판_12월_대림절_A5.pdf'); N=len(pages); print('A5 쪽수',N)
# 스프링 제본: A4 가로에 두 쪽씩(작업실의 '스프링 제본'과 같은 차례). 양면은 짧은 쪽 넘김, 찍은 뒤 가운데를 자르고 왼쪽 묶음을 오른쪽 묶음 위에 얹음
S=N//4; order=[]
for k in range(1,S+1): order+= [(2*k-1,2*S+2*k-1),(2*S+2*k,2*k)]
A5w,A5h=float(pages[0].mediabox.width),float(pages[0].mediabox.height)
sw=PdfWriter()
for a,bb in order:
    sh=PageObject.create_blank_page(width=A5w*2,height=A5h)
    for i,pn in enumerate((a,bb)):
        sh.merge_transformed_page(pages[pn-1],Transformation().translate(i*A5w,0))
    sw.add_page(sh)
sw.write('2026_체험판_12월_대림절_스프링제본_A4.pdf'); print('A4 면',len(order),'장',len(order)//2)
