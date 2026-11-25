# 하루에 여러 권을 읽는 날의 안내, 걸음 단추 첫 안내
import sys, subprocess, time
from playwright.sync_api import sync_playwright
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
        for tag, vw, vh in (('phone',390,800),('tablet',820,1180)):
            cx = b.new_context(viewport={'width': vw, 'height': vh}, has_touch=True)
            def start(q):
                pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.goto('http://localhost:8765/index.html?'+q); pg.click('#go'); pg.wait_for_timeout(1000)
                if pg.locator('#cbsrShelf .dg.me').count(): pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(800)
                return pg
            txt = lambda pg, s: pg.locator(s).first.inner_text() if pg.locator(s).count() else ''
            # 두 권 읽는 날(사무엘상·하)
            pg = start('today=9&todays=9,10')
            pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(900)
            c = pg.locator('#cbsrShelf .dg .dgc button'); t = txt(pg, '#cbsrShelf .dg .dgb span')
            chk(tag+' 두 권: 사서가 두 책을 보여 줌 · '+t.replace('\n',' '), c.count()==2 and '두 권' in t and '사무엘상' in c.nth(0).inner_text() and '사무엘하' in c.nth(1).inner_text())
            pg.screenshot(path=OUT+'m_%s_two.png'%tag)
            c.nth(1).click(); pg.wait_for_timeout(700)
            chk(tag+' 두 권: 고른 책으로 안내', '사무엘하' in txt(pg, '#cbsrShelf .dg .dgb span'))
            pg.wait_for_timeout(5200)
            chk(tag+' 두 권: 그 책이 있는 서가까지 감', pg.evaluate('window.__ovs()')>=2 and '사무엘하' in (pg.locator('#cbsrShelf').inner_text()))
            pg.close()
            # 세 권 읽는 날(요한이서·요한삼서·유다서)
            pg = start('today=63&todays=63,64,65')
            pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(900)
            c = pg.locator('#cbsrShelf .dg .dgc button')
            r = pg.evaluate('(()=>{const b=document.querySelector("#cbsrShelf .dg .sf").getBoundingClientRect(),c=document.querySelector("#cbsrShelf .dg .dgc").getBoundingClientRect();return [b.top+b.height*.53,c.top]})()')
            chk(tag+' 세 권: 세 책, 사서 얼굴이 선택지 위', c.count()==3 and '세 권' in txt(pg, '#cbsrShelf .dg .dgb span') and r[0] <= r[1])
            pg.mouse.click(vw/2, vh*0.12); pg.wait_for_timeout(700)
            chk(tag+' 세 권: 빈 곳을 누르면 둘러보기', pg.locator('#cbsrShelf .pad').count()==1)
            # 걸음 단추 첫 안내: 기기마다 한 번
            chk(tag+' 걸음 단추 첫 안내가 위쪽에 나옴', '화살표' in txt(pg, '#cbsrShelf .lbx.tmp.up'))
            pg.screenshot(path=OUT+'m_%s_hint.png'%tag)
            pg.click('#cbsrShelf .pad .mu'); pg.wait_for_timeout(1300)
            chk(tag+' 한 걸음 뒤에는 안내가 없음', pg.locator('#cbsrShelf .lbx.tmp.up').count()==0)
            pg.close()
            pg = start('today=40'); pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(800)
            chk(tag+' 다시 열면 안내가 나오지 않음', pg.locator('#cbsrShelf .lbx.tmp.up').count()==0 and pg.locator('#cbsrShelf .pad').count()==1)
            pg.close(); cx.close()
        b.close()
finally:
    srv.terminate()
print('오류:', errs or '없음'); print('실패:', (fails + (['페이지 오류 %d건' % len(errs)] if errs else [])) or '없음', '(%d가지)' % n)
