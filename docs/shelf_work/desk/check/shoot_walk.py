import sys, subprocess, time
from playwright.sync_api import sync_playwright
OUT='/home/claude/shelf-desk/check/dlg/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd='/tmp/shelftest', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
errs=[]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for tag, vw, vh in (('phone', 390, 800), ('tablet', 820, 1180)):
            pg = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=1, has_touch=True).new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            sh = lambda n: pg.screenshot(path=OUT + 'n_%s_%s.png' % (tag, n))
            pg.goto('http://localhost:8765/index.html?today=40'); pg.click('#go'); pg.wait_for_timeout(1000)
            if pg.locator('#cbsrShelf .dg.me').count(): sh('0mono'); pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(800)
            sh('1hello')
            pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(600); sh('2free')
            pg.click('#cbsrShelf .zone[data-s=ot]'); pg.wait_for_timeout(800); sh('3walk'); pg.wait_for_timeout(1400); sh('4sec')
            pg.evaluate("document.querySelectorAll('#cbsrShelf .gl button')[0].click()"); pg.wait_for_timeout(1500); sh('5press')
            pg.go_back(); pg.wait_for_timeout(1900); pg.go_back(); pg.wait_for_timeout(1900)
            pg.click('#cbsrShelf .zone.e'); pg.wait_for_timeout(2600); sh('6etc')
            pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(3000); sh('7dark')
            pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(2000)
            pg.click('#cbsrShelf .lbc'); pg.wait_for_timeout(700)
            pg.click('#cbsrShelf .dg .dgc button:nth-child(3)'); pg.wait_for_timeout(2300); pg.click('#cbsrShelf .plh button:nth-of-type(1)'); pg.wait_for_timeout(400); sh('8plan')
            pg.click('#cbsrShelf .bk'); pg.wait_for_timeout(800)
            pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(1200); sh('9guide'); pg.wait_for_timeout(4200); sh('10book')
            pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(2900); sh('11cover')
            pg.evaluate("document.querySelector('#cbsrShelf .nv [data-a=next]').click()"); pg.wait_for_timeout(700); sh('11b_p2')
            pg.evaluate("document.querySelector('#cbsrShelf .nv [data-a=next]').click()"); pg.wait_for_timeout(700); sh('11c_p3')
            pg.click('#cbsrShelf .bj'); pg.wait_for_timeout(500); sh('12card')
            pg.click('#cbsrShelf .nv .mid'); pg.wait_for_timeout(700); pg.go_back(); pg.wait_for_timeout(1900); pg.go_back(); pg.wait_for_timeout(1900)
            pg.click('#cbsrShelf .dg .dgc button:nth-child(4)') if pg.locator('#cbsrShelf .dg .dgc button').count() else (pg.click('#cbsrShelf .lbc'), pg.wait_for_timeout(600), pg.click('#cbsrShelf .dg .dgc button:nth-child(4)'))
            pg.wait_for_timeout(450); sh('13move'); pg.wait_for_timeout(3000); sh('14fan')
        b.close()
finally:
    srv.terminate()
print('오류:', errs or '없음')
from PIL import Image
def sheet(names, out, h=800):
    ims=[Image.open(OUT+n+'.png').convert('RGB') for n in names]
    ims=[im.resize((round(im.width*h/im.height), h), Image.LANCZOS) for im in ims]
    S=Image.new('RGB',(sum(i.width for i in ims)+8*(len(ims)-1),h),(60,60,60)); x=0
    for im in ims: S.paste(im,(x,0)); x+=im.width+8
    S.save(OUT+out)
sheet(['n_phone_1hello','n_phone_2free','n_phone_3walk','n_phone_4sec','n_phone_5press'],'n_s1.png')
sheet(['n_phone_6etc','n_phone_7dark','n_phone_8plan','n_phone_10book','n_phone_11cover'],'n_s2.png')
sheet(['n_phone_12card','n_phone_14fan','n_tablet_1hello','n_tablet_6etc','n_tablet_8plan'],'n_s3.png')
sheet(['n_phone_9guide','n_phone_11b_p2','n_phone_11c_p3','n_phone_13move','n_tablet_14fan','n_tablet_11cover'],'n_s4.png')
