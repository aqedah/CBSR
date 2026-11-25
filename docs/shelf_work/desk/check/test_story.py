# 서고 이야기(11-25): 1막(처음), 2–5막(열린 막을 한 번), 물건, 아침, 촛불 덤, 고비의 한마디
import sys, subprocess, time
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='/home/claude/shelf-desk/check/dlg/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd='/tmp/shelftest', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
errs=[]; fails=[]; n=0
def chk(name, ok):
    global n
    n+=1; print(('  통과 ' if ok else '  실패 ')+name)
    if not ok: fails.append(name)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        cx = b.new_context(viewport={'width': 390, 'height': 800}, has_touch=True)
        def start(q, sh=None):
            pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://localhost:8765/index.html?'+q); pg.click('#go'); pg.wait_for_timeout(1000); return pg
        T = lambda pg: (pg.locator('#cbsrShelf .dg .dgb span').first.inner_text() if pg.locator('#cbsrShelf .dg .dgb span').count() else '').replace('\n',' ')
        who = lambda pg: pg.locator('#cbsrShelf .dg .dgb b').first.inner_text() if pg.locator('#cbsrShelf .dg .dgb b').count() else ''
        def tap(pg): pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(700)
        # 1막
        pg = start('today=40'); lines=[]
        for i in range(3): lines.append((who(pg),T(pg))); pg.screenshot(path=OUT+'st_1_%d.png'%i); tap(pg)
        chk('1막: 나 → 나(문 위의 글) → 사서(늘 밤) %s' % [l[1][:14] for l in lines], lines[0][0]=='나' and '119' not in lines[1][1] and '등이요' in lines[1][1] and lines[2][0]=='사서' and '늘 밤' in lines[2][1])
        chk('1막 뒤 인사와 선택지', '무엇을 찾으십니까' in T(pg) and pg.locator('#cbsrShelf .dgc button').count()>=2)
        pg.close()
        # 다시 들어오면 보통 인사, 막 없음 → 물건 없음
        pg = start('today=40'); chk('두 번째: 보통 인사', '오셨습니까' in T(pg) and pg.locator('#cbsrShelf .itm').count()==0); pg.close()
        # 2막 열림
        pg = start('today=40&acts=2'); t1=T(pg); tap(pg); pg.screenshot(path=OUT+'st_2_key.png'); clue=pg.locator('#cbsrShelf .clue img').count(); t2=T(pg); tap(pg); t3=T(pg); tap(pg)
        chk('2막: 열쇠 장면(물건을 크게) %s' % [t1[:10],t2[:12],t3[:10]], '보이지 않는다' in t1 and clue==1 and '탔다' in t2 and who(pg)=='사서')
        pg.click('#cbsrShelf .dgc button:nth-child(2)'); pg.wait_for_timeout(800)
        chk('2막 뒤 통로에 열쇠가 놓임', pg.locator('#cbsrShelf .itm[data-a="itm:key"]').count()==1)
        pg.click('#cbsrShelf .itm[data-a="itm:key"]'); pg.wait_for_timeout(400); pg.screenshot(path=OUT+'st_2_item.png')
        chk('열쇠를 누르면 나의 혼잣말', '열쇠' in pg.locator('#cbsrShelf .lbx').first.inner_text() and '나' in pg.locator('#cbsrShelf .lbx b').first.inner_text())
        pg.close()
        pg = start('today=40&acts=2'); chk('2막은 한 번만', '오셨습니까' in T(pg)); pg.close()
        # 3·4막 차례로(둘 다 열려 있으면 앞의 것 먼저)
        pg = start('today=40&acts=2,3,4'); pg.screenshot(path=OUT+'st_3_ledger.png'); s3='장부' in T(pg); tap(pg); tap(pg); tap(pg); pg.close()
        pg = start('today=40&acts=2,3,4'); s4='그을린 서가' in T(pg); pg.screenshot(path=OUT+'st_4_book.png'); tap(pg); tap(pg); pg.close()
        chk('3막 다음 들어올 때 4막', s3 and s4)
        pg = start('today=40&acts=2,3,4'); pg.click('#cbsrShelf .dgc button:nth-child(2)'); pg.wait_for_timeout(700)
        pg.click('#cbsrShelf .pad .mu'); pg.wait_for_timeout(1300); a=pg.locator('#cbsrShelf .itm[data-a="itm:ledger"]').count(); pg.screenshot(path=OUT+'st_p1.png')
        pg.click('#cbsrShelf .pad .mu'); pg.wait_for_timeout(1300); c=pg.locator('#cbsrShelf .itm[data-a="itm:book"]').count(); pg.screenshot(path=OUT+'st_p2.png')
        chk('장부는 통로 가운데, 책은 그을린 서가', a==1 and c==1); pg.close()
        # 5막 아침
        pg = start('today=40&acts=2,3,4,5'); pg.wait_for_timeout(200); tap(pg); m0=pg.evaluate('document.querySelector("#cbsrShelf .hallv").classList.contains("morn")'); tap(pg); tap(pg); pg.wait_for_timeout(2400); pg.screenshot(path=OUT+'st_5_morn.png'); tap(pg)
        chk('5막: "아침입니다"부터 서고가 밝아짐', m0 and pg.evaluate('document.querySelector("#cbsrShelf .hallv").classList.contains("morn")'))
        pg.close(); pg = start('today=40&acts=2,3,4,5'); chk('5막 뒤로는 늘 아침', pg.evaluate('document.querySelector("#cbsrShelf .hallv").classList.contains("morn")') and '오셨습니까' in T(pg)); pg.close()
        # 촛불 덤
        pg = start('today=40&fin=1,2,3'); pg.click('#cbsrShelf .dgc button:nth-child(2)'); pg.wait_for_timeout(700); pg.click('#cbsrShelf .zone[data-s=ot]'); pg.wait_for_timeout(1900)
        pg.click('#cbsrShelf .gl button >> nth=0'); pg.wait_for_timeout(1800); pg.screenshot(path=OUT+'st_fin.png')
        chk('다 읽은 책(창·출·레)에 작은 촛불 셋', pg.locator('#cbsrShelf .fin').count()==3); pg.close()
        cx.close()
        # 고비의 한마디: 새 기기에서(1막을 이미 본 것으로)
        for q, word, name in (('ot=1','구약을 다 지나','구약 마침'),('nb=5','신명기입니다','새 책'),):
            cx = b.new_context(viewport={'width': 390, 'height': 800}, has_touch=True); pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://localhost:8765/index.html'); pg.evaluate('localStorage.setItem("cbsr_shelf_qa",JSON.stringify({_s:{met:{v:"1",t:1}}}))')
            pg.goto('http://localhost:8765/index.html?today=40&'+q); pg.click('#go'); pg.wait_for_timeout(1300)
            chk('한마디(%s): %s' % (name, T(pg)), word in T(pg))
            pg.close(); pg = cx.new_page(); pg.goto('http://localhost:8765/index.html?today=40&'+q); pg.click('#go'); pg.wait_for_timeout(1300)
            chk('한마디(%s)는 한 번' % name, word not in T(pg)); pg.close(); cx.close()
        cx = b.new_context(viewport={'width': 390, 'height': 800}, has_touch=True); pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8765/index.html'); pg.evaluate('localStorage.setItem("cbsr_shelf_qa",JSON.stringify({_s:{met:{v:"1",t:1},last:{v:"2027-01-10",t:1}}}))')
        pg.goto('http://localhost:8765/index.html?today=40&td=2027-02-01'); pg.click('#go'); pg.wait_for_timeout(1300)
        chk('오랜만에: '+T(pg), '다시 오셨군요' in T(pg)); pg.close(); cx.close()
        b.close()
finally:
    srv.terminate()
def sheet(names, out, h=640):
    ims=[Image.open(OUT+x+'.png').convert('RGB') for x in names]; ims=[im.resize((round(im.width*h/im.height),h)) for im in ims]
    S=Image.new('RGB',(sum(i.width for i in ims)+8*(len(ims)-1),h),(60,60,60)); x=0
    for im in ims: S.paste(im,(x,0)); x+=im.width+8
    S.save(OUT+out)
sheet(['st_1_1','st_1_2','st_2_key','st_2_item','st_3_ledger','st_4_book'],'st_a.png'); sheet(['st_p1','st_p2','st_5_morn','st_fin'],'st_b.png')
print('오류:', errs or '없음'); print('실패:', (fails+(['페이지 오류 %d건'%len(errs)] if errs else [])) or '없음', '(%d가지)' % n)
