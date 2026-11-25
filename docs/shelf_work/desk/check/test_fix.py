# GPT 감수(11-24)에서 맞다고 본 오류들을 고친 뒤의 시험
import sys, subprocess, time, os, json
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd='/tmp/shelftest', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
errs = []; ok = []
def chk(name, cond, extra=''):
    ok.append((name, bool(cond))); print(('  통과 ' if cond else '  실패 ') + name, '·', extra)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for tag, vw, vh in (('phone', 390, 800), ('tablet', 820, 1180)):
            cx = b.new_context(viewport={'width': vw, 'height': vh}, has_touch=True)
            pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            txt = lambda sel: pg.evaluate('(s)=>{const e=document.querySelector(s);return e?e.innerText:null}', sel)
            ovs = lambda: pg.evaluate('window.__ovs()')
            store = lambda: json.loads(pg.evaluate('localStorage.getItem("cbsr_shelf_qa")||"{}"'))
            inside = lambda: pg.evaluate('(()=>{const r=document.querySelector("#cbsrShelf");return !!r&&r.contains(document.activeElement)})()')
            print(tag)
            pg.goto('http://localhost:8765/index.html?today=19'); pg.click('#go'); pg.wait_for_timeout(900)
            for _i in range(4):
                if not (pg.locator('#cbsrShelf .dg button.dgb').count() and not pg.locator('#cbsrShelf .dgc').count()): break
                pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(700)
            pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(5200)
            chk('시편은 150편', '시편, 150편입니다' in (txt('#cbsrShelf .dg .dgb') or ''), txt('#cbsrShelf .dg .dgb'))
            pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(2800)
            chk('시편 표지도 150편', '150편' in (txt('#cbsrShelf .bv main') or '') and '150장' not in (txt('#cbsrShelf .bv main') or ''))
            lv = ovs()
            n = pg.evaluate('document.querySelectorAll("#cbsrShelf .bv .pr i").length')
            for _ in range(n - 1): pg.click('#cbsrShelf .nv [data-a=next]'); pg.wait_for_timeout(60)
            pg.wait_for_timeout(400)
            chk('적는 곳 안내에 안심 문구가 없음', '비워 두어도' not in (txt('#cbsrShelf .bv main') or '') and '도장이 찍힙니다' in (txt('#cbsrShelf .bv main') or ''))
            pg.click('#cbsrShelf .cdl button:nth-child(1)'); pg.wait_for_timeout(300); pg.fill('#cbsrQa', '다윗과 여러 사람이 지은 노래'); pg.click('#cbsrShelf [data-a=ans]'); pg.wait_for_timeout(800)
            chk('적으면 도장', pg.locator('#cbsrShelf .cdl i.on').count() == 1)
            pg.click('#cbsrShelf .cdl button:nth-child(1)'); pg.wait_for_timeout(300); pg.fill('#cbsrQa', ''); pg.click('#cbsrShelf [data-a=cardback]'); pg.wait_for_timeout(500)
            chk('다 지우고 돌아오면 빈칸으로 남음(되살아나지 않음)', pg.locator('#cbsrShelf .cdl i.on').count() == 0 and (store().get('psa') or {}).get('who', {}).get('v') == '', str((store().get('psa') or {}).get('who')))
            pg.click('#cbsrShelf .cdl button:nth-child(2)'); pg.wait_for_timeout(300); pg.fill('#cbsrQa', '쓰다가 다른 앱으로')
            pg.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true}); document.dispatchEvent(new Event('visibilitychange')); Object.defineProperty(document,'hidden',{value:false,configurable:true});")
            chk('쓰다가 화면이 가려져도 저장됨', (store().get('psa') or {}).get('when', {}).get('v') == '쓰다가 다른 앱으로')
            pg.focus('#cbsrQa'); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            chk('글 쓰는 중 Esc: 자판만 내려가고 책에 그대로', ovs() == lv and pg.locator('#cbsrQa').count() == 1 and pg.evaluate('document.activeElement.id') != 'cbsrQa', 'ovs %s' % ovs())
            pg.keyboard.press('Escape'); pg.wait_for_timeout(700)
            chk('Esc 한 번에 한 단계만(책 → 서가)', ovs() == lv - 1 and pg.locator('#cbsrShelf .sp').count() > 3, 'ovs %s → %s' % (lv, ovs()))
            pg.keyboard.press('Escape'); pg.wait_for_timeout(1900)
            chk('Esc 한 번에 한 단계만(서가 → 구역)', ovs() == lv - 2 and pg.locator('#cbsrShelf .gl button').count() == 4, 'ovs %s' % ovs())
            outs = 0
            for i in range(24):
                pg.keyboard.press('Tab'); outs += 0 if inside() else 1
            for i in range(8):
                pg.keyboard.press('Shift+Tab'); outs += 0 if inside() else 1
            chk('Tab을 서른두 번 눌러도 초점이 서고 안에 있음', outs == 0, '밖으로 나간 횟수 %d' % outs)
            pg.keyboard.press('Escape'); pg.wait_for_timeout(1900); pg.keyboard.press('Escape'); pg.wait_for_timeout(900)
            chk('서고를 닫으면 초점이 서고를 연 단추로', pg.locator('#cbsrShelf').count() == 0 and pg.evaluate('document.activeElement.id') == 'go', pg.evaluate('document.activeElement.id||document.activeElement.tagName'))
            cx.close()
        b.close()
finally:
    srv.terminate()
print('오류:', errs or '없음'); bad = [n for n, c in ok if not c] + (['페이지 오류 %d건' % len(errs)] if errs else []); print('실패:', bad or '없음', '(%d가지)' % len(ok))
