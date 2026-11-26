import sys, subprocess, time, json
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8766', '--bind', '127.0.0.1'], cwd='/tmp/cbsr_build_app/site', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
errs=[]; ok=[]
def chk(n,c,x=''): ok.append((n,bool(c))); print(('  통과 ' if c else '  실패 ')+n, x)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_context(viewport={'width': 1440, 'height': 900}, service_workers='block').new_page()
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8766/shelf_edit.html'); pg.wait_for_timeout(2500)
        rows = pg.evaluate("[...document.querySelectorAll('#rows .row')].length"); etc = pg.evaluate("!!document.querySelector('.gh.etc')")
        chk('목록: 66권 + 그을린 서가 19칸 ' + str(rows), rows == 85 and etc)
        pg.click('#rows .row[data-id=rom]'); pg.wait_for_timeout(3500)
        fr = pg.frame_locator('#apv')
        t = fr.locator('#cbsrShelf').inner_text() if fr.locator('#cbsrShelf').count() else ''
        chk('미리보기에 로마서 표지', '로마서' in t, t[:40].replace('\n',' '))
        pg.screenshot(path='/home/claude/shelf-desk/check/dlg/pv_1.png')
        ta = pg.locator('#f-line'); ta.fill('미리보기 시험 문장입니다.'); pg.wait_for_timeout(2200)
        t2 = fr.locator('#cbsrShelf').inner_text()
        chk('고치면 미리보기가 바뀜', '미리보기 시험 문장' in t2)
        pg.evaluate("document.getElementById('apv').contentDocument.querySelector('#cbsrShelf .nv [data-a=next]').click()"); pg.wait_for_timeout(900)
        ta.fill('미리보기 시험 문장입니다 둘.'); pg.wait_for_timeout(2200)
        st = pg.evaluate("document.getElementById('apv').contentWindow.CBSR_SHELF.state()")
        chk('고쳐도 보던 쪽에 머묾 ' + str(st), st and st['p'] == 1)
        pg.screenshot(path='/home/claude/shelf-desk/check/dlg/pv_2.png')
        ta.fill(pg.evaluate("''")); pg.locator('#f-line').fill(''); 
        pg.click('#rows .row[data-id=tob]'); pg.wait_for_timeout(2500)
        m=pg.locator('#edit').inner_text(); chk('그을린 서가 칸(토빗기) 편집 화면', '토빗기' in m and '아직 나오지 않습니다' in m, m[:80].replace(chr(10),' ')); pg.screenshot(path='/home/claude/shelf-desk/check/dlg/pv_3.png')
        j = pg.evaluate("(()=>{ let s=''; const o=URL.createObjectURL; return null })()")
        b.close()
finally: srv.terminate()
print('오류:', errs or '없음'); print('실패:', [n for n,c in ok if not c] or '없음')
