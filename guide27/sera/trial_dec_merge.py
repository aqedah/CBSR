# 체험판 12월·부록 책 묶기 (11-25): body.pdf(앞표지·책머리·하루 지면·부록 머리) + 세라핌 묵상지 원본 PDF(app/site_src/img/ax26/appx.pdf) + 뒤표지
# A5 한 권과, A4 가로에 두 쪽씩 놓은 스프링 제본판을 만듭니다.
import os,sys
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
AX=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','app','site_src','img','ax26','appx.pdf')
NAME='2026_체험판_12월_부록'
pages=list(PdfReader('body.pdf').pages)+list(PdfReader(AX).pages)
blank=PdfReader('blank.pdf').pages[0]; back=PdfReader('back.pdf').pages[0]
n=len(pages)+1
pages+=[blank]*((4-n%4)%4)+[back]
w=PdfWriter()
for x in pages: w.add_page(x)
w.write(NAME+'_A5.pdf'); N=len(pages); print('A5 쪽수',N)
S=N//4; order=[]
for k in range(1,S+1): order+=[(2*k-1,2*S+2*k-1),(2*S+2*k,2*k)]
A5w,A5h=float(pages[0].mediabox.width),float(pages[0].mediabox.height)
sw=PdfWriter()
for a,bb in order:
    sh=PageObject.create_blank_page(width=A5w*2,height=A5h)
    for i,pn in enumerate((a,bb)): sh.merge_transformed_page(pages[pn-1],Transformation().translate(i*A5w,0))
    sw.add_page(sh)
sw.write(NAME+'_스프링제본_A4.pdf'); print('A4 면',len(order),'장',len(order)//2)
