# 움직임 줄이기를 켠 기기와, 다음 자리 그림이 오지 않을 때에도 서고가 조작되는지
import sys, subprocess, time
from playwright.sync_api import sync_playwright
OUT='/home/claude/shelf-desk/check/dlg/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd='/tmp/shelftest', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
errs=[]; res=[]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        # 1) 움직임 줄이기
        pg = b.new_context(viewport={'width': 390, 'height': 800}, reduced_motion='reduce', has_touch=True).new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8765/index.html?today=40'); pg.click('#go'); pg.wait_for_timeout(900)
        for _i in range(4):
            if not (pg.locator('#cbsrShelf .dg button.dgb').count() and not pg.locator('#cbsrShelf .dgc').count()): break
            pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(500)
        pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(500)
        P = lambda: pg.evaluate('+document.querySelector("#cbsrShelf .hl[data-p]").getAttribute("data-p")')
        pg.click('#cbsrShelf .pad .mu'); pg.wait_for_timeout(150); res.append(('줄이기: 앞으로 바로 바뀜', P()==1 and pg.locator('#cbsrShelf .hl').count()==1))
        pg.keyboard.press('KeyW'); pg.wait_for_timeout(150); pg.keyboard.press('KeyW'); pg.wait_for_timeout(700)
        res.append(('줄이기: 끝에서 경고', pg.locator('#cbsrShelf .wn.up').count()==1))
        pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(500); pg.keyboard.press('KeyA'); pg.wait_for_timeout(500)
        res.append(('줄이기: 구약 목록', pg.locator('#cbsrShelf .gl button').count()>=4))
        # 2) 다음 자리 그림이 안 올 때
        cx = b.new_context(viewport={'width': 390, 'height': 800}, has_touch=True); pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/hall_1.webp*', lambda r: r.abort())
        pg.goto('http://localhost:8765/index.html?today=40'); pg.click('#go'); pg.wait_for_timeout(900)
        for _i in range(4):
            if not (pg.locator('#cbsrShelf .dg button.dgb').count() and not pg.locator('#cbsrShelf .dgc').count()): break
            pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(500)
        pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(600)
        pg.click('#cbsrShelf .pad .mu'); pg.wait_for_timeout(1300); pg.screenshot(path=OUT+'x_noimg.png')
        res.append(('그림이 안 와도 걸음 단추는 남음', pg.locator('#cbsrShelf .pad button').count()==4))
        b.close()
finally:
    srv.terminate()
for r in res: print(('  통과 ' if r[1] else '  실패 ')+r[0])
print('오류:', errs or '없음')
print('실패:', ([r[0] for r in res if not r[1]] + (['페이지 오류 %d건' % len(errs)] if errs else [])) or '없음', '(%d가지)' % len(res))
