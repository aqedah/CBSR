# 실제 빌드에서: 서고 단추 → 첫 만남 → 안내(오늘 읽는 책) → 적어 두기 → 앱 기록 저장 → 다시 들어옴
import sys, subprocess, time, json
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8766', '--bind', '127.0.0.1'], cwd='/tmp/cbsr_build_app/site', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
errs = []; S = '/home/claude/shelf-desk/check/dlg/'
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        cx = b.new_context(viewport={'width': 412, 'height': 820}, device_scale_factor=2, has_touch=True, service_workers='block')
        pg = cx.new_page()
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('CONSOLE ' + m.text[:160]) if m.type == 'error' and 'net::' not in m.text and 'Failed to load resource' not in m.text else None)
        T = lambda sel: pg.evaluate('(s)=>{const e=document.querySelector(s);return e?e.innerText.replace(/\\n/g," / "):null}', sel)
        pg.goto('http://127.0.0.1:8766/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(3500)
        print('오늘 화면의 본문:', (pg.evaluate("(()=>{const e=document.querySelector('.tdref,.todayref,[class*=ref]');return e?e.innerText.slice(0,40):''})()") or '').replace('\n', ' '))
        pg.evaluate("document.querySelector('#rgShelf').click()"); pg.wait_for_timeout(2000)
        print('1 처음:', T('#cbsrShelf .dg .dgb')); pg.screenshot(path=S + 'app_1.png')
        pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(700)
        print('2 사서:', T('#cbsrShelf .dg .dgb'), '|', T('#cbsrShelf .dg .dgc')); pg.screenshot(path=S + 'app_2.png')
        pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(700)
        print('3 안내:', T('#cbsrShelf .dg .dgb'))
        pg.wait_for_timeout(5000)
        print('4 책 앞:', T('#cbsrShelf .dg .dgb'), '| 강조된 책등', pg.locator('#cbsrShelf .sp.hi').count()); pg.screenshot(path=S + 'app_4.png')
        pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(2900)
        print('5 책:', (T('#cbsrShelf .bv main') or '')[:60])
        n = pg.evaluate('document.querySelectorAll("#cbsrShelf .bv .pr i").length')
        for _ in range(n - 1): pg.click('#cbsrShelf .nv [data-a=next]'); pg.wait_for_timeout(70)
        pg.wait_for_timeout(400); pg.click('#cbsrShelf .cdl button:nth-child(1)'); pg.wait_for_timeout(300)
        pg.fill('#cbsrQa', '바울이 로마에 있는 성도들에게 썼다.'); pg.click('#cbsrShelf [data-a=ans]'); pg.wait_for_timeout(900)
        print('6 도장:', pg.locator('#cbsrShelf .cdl i.on').count(), '|', (T('#cbsrShelf .cdl button:nth-child(1)') or '')[:40]); pg.screenshot(path=S + 'app_6.png')
        m = json.loads(pg.evaluate("localStorage.getItem('rjnote:y365')||'{}'")).get('shq') or {}
        print('7 앱 기록:', {k: {f: v.get('v') for f, v in x.items()} for k, x in m.items()})
        for i in range(4): pg.go_back(); pg.wait_for_timeout(700)
        print('8 뒤로 네 번 → 서고 닫힘', pg.evaluate("!document.getElementById('cbsrShelf')"), '| 앱 그대로', pg.locator('#rgShelf').count())
        pg.reload(wait_until='domcontentloaded'); pg.wait_for_timeout(3500)
        pg.evaluate("document.querySelector('#rgShelf').click()"); pg.wait_for_timeout(1800)
        print('9 다시 들어옴:', T('#cbsrShelf .dg .dgb')); pg.screenshot(path=S + 'app_9.png')
        pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(600)
        print('10 둘러보기: 팻말', pg.locator('#cbsrShelf .zn:not(.off) .zone').count(), '| 사서 단추', pg.locator('#cbsrShelf .lbc').count()); pg.screenshot(path=S + 'app_10.png')
        pg.click('#cbsrShelf .bk'); pg.wait_for_timeout(600); print('11 닫기 →', pg.evaluate("!document.getElementById('cbsrShelf')"))
        b.close()
finally:
    srv.terminate()
print('오류:', errs[:8] or '없음')
