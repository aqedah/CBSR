# 실제 빌드: Esc가 한 번에 한 단계만 물러나는지(앱의 Esc 처리와 겹치지 않는지), 초점이 서고 안에 머무는지
import sys, subprocess, time
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8766', '--bind', '127.0.0.1'], cwd='/tmp/cbsr_build_app/site', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
errs = []; ok = []
def chk(name, cond, extra=''):
    ok.append((name, bool(cond))); print(('  통과 ' if cond else '  실패 ') + name, '·', extra)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_context(viewport={'width': 1100, 'height': 820}, service_workers='block').new_page()
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
        pg.goto('http://127.0.0.1:8766/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(3500)
        pg.wait_for_timeout(1200); pg.evaluate("(()=>{const r=document.getElementById('sheetRoot'); if(r) r.innerHTML='';})()")
        has = lambda sel: pg.locator(sel).count() > 0
        pg.evaluate("document.querySelector('#rgShelf').click()"); pg.wait_for_timeout(1800)
        if has('#cbsrShelf .dg.me'): pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(700)
        pg.click('#cbsrShelf .dgc button:nth-child(2)'); pg.wait_for_timeout(500)
        pg.click('#cbsrShelf .zone[data-s=nt]'); pg.wait_for_timeout(1900)
        pg.evaluate("[...document.querySelectorAll('#cbsrShelf .gl button')].find(x=>x.innerText.includes('바울서신')).click()"); pg.wait_for_timeout(2600)
        chk('서가까지 들어감', pg.locator('#cbsrShelf .sp').count() == 13)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(1900)
        chk('Esc 한 번 → 구역(한 단계만)', has('#cbsrShelf .gl button') and not has('#cbsrShelf .sp') and has('#cbsrShelf'), '구역 목록 %d' % pg.locator('#cbsrShelf .gl button').count())
        pg.keyboard.press('Escape'); pg.wait_for_timeout(1900)
        chk('Esc 한 번 더 → 서고 첫 화면', has('#cbsrShelf .lbc'))
        outs = 0
        for i in range(20):
            pg.keyboard.press('Tab'); outs += 0 if pg.evaluate('document.querySelector("#cbsrShelf").contains(document.activeElement)') else 1
        chk('Tab 스무 번: 초점이 가려진 앱으로 나가지 않음', outs == 0, '나간 횟수 %d' % outs)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(900)
        chk('Esc 한 번 더 → 서고가 닫히고 초점은 서고 단추', not has('#cbsrShelf') and pg.evaluate('document.activeElement.id') == 'rgShelf', pg.evaluate('document.activeElement.id'))
        b.close()
finally:
    srv.terminate()
print('오류:', errs[:5] or '없음'); bad = [n for n, c in ok if not c]; print('실패:', bad or '없음', '(%d가지)' % len(ok))
