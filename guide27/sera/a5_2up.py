# 세라핌 묵상지를 가이드북(A5) 글자 크기로 짜서 A4 가로 한 면에 두 쪽씩 놓습니다. (11-24 목사님: A4 가로 양면으로 뽑아 씀, A4를 줄이면 글자가 작음)
# 한 회 = A5 8쪽 = A4 두 장(양면). 앞면 1·2쪽(읽기), 뒷면 3·4쪽(본문 관찰), 둘째 장 앞면 5·6쪽(하나님의 성품), 뒷면 7·8쪽(해설과 기도).
# 양면 인쇄는 '짧은 쪽으로 넘기기'.
# 쓰는 법: python3 a5_2up.py 출력.pdf w1124 [w1201 ...]
import sys, os, asyncio, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a5
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
out, mods = sys.argv[1], sys.argv[2:]
pages = []
with tempfile.TemporaryDirectory() as T:
    for m in mods:
        f = os.path.join(T, m + '.pdf'); asyncio.run(a5.main(f, 1, [m]))
        ps = list(PdfReader(f).pages)
        if len(ps) % 4: ps += [PageObject.create_blank_page(width=ps[0].mediabox.width, height=ps[0].mediabox.height)] * (4 - len(ps) % 4)
        pages += ps
w = PdfWriter(); W, H = float(pages[0].mediabox.width), float(pages[0].mediabox.height)
for i in range(0, len(pages), 2):
    sh = PageObject.create_blank_page(width=W * 2, height=H)
    for j, p in enumerate(pages[i:i + 2]): sh.merge_transformed_page(p, Transformation().translate(j * W, 0))
    w.add_page(sh)
w.write(out); print('A4 가로', len(w.pages), '면 =', len(w.pages) // 2, '장')
