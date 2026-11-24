import sys, subprocess, time
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='/home/claude/shelf-desk/check/dlg/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd='/tmp/shelftest', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
errs=[]
def run(tag, vw, vh):
    pg = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=1, has_touch=True).new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8765/index.html?today=40'); pg.click('#go'); pg.wait_for_timeout(1000)
    if pg.locator('#cbsrShelf .dg.me').count(): pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(800)
    sh=lambda n: pg.screenshot(path=OUT+'s_%s_%s.png'%(tag,n))
    sh('0hello')
    pg.click('#cbsrShelf .dg .dgc button:nth-child(2)'); pg.wait_for_timeout(900); sh('1p0')
    pg.click('#cbsrShelf .pad .mu'); pg.wait_for_timeout(430); sh('2mid'); pg.wait_for_timeout(1000); sh('3p1')
    pg.keyboard.press('KeyW'); pg.wait_for_timeout(430); sh('4mid'); pg.wait_for_timeout(1000); sh('5p2')
    pg.keyboard.press('ArrowUp'); pg.wait_for_timeout(2600); sh('6etc')
    pg.click('#cbsrShelf .dg .dgc button:nth-child(1)'); pg.wait_for_timeout(2000); sh('7back')
    pg.keyboard.press('KeyS'); pg.wait_for_timeout(1500); sh('8p1')
    pg.keyboard.press('KeyA'); pg.wait_for_timeout(2300); sh('9ot')
    return pg
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        run('phone',390,800); run('tablet',820,1180)
        b.close()
finally:
    srv.terminate()
print('오류:', errs or '없음')
def sheet(names, out, h=700):
    ims=[Image.open(OUT+n+'.png').convert('RGB') for n in names]; ims=[im.resize((round(im.width*h/im.height),h)) for im in ims]
    S=Image.new('RGB',(sum(i.width for i in ims)+8*(len(ims)-1),h),(60,60,60)); x=0
    for im in ims: S.paste(im,(x,0)); x+=im.width+8
    S.save(OUT+out)
sheet(['s_phone_1p0','s_phone_2mid','s_phone_3p1','s_phone_4mid','s_phone_5p2'],'s_a.png')
sheet(['s_phone_6etc','s_phone_7back','s_phone_8p1','s_phone_9ot','s_phone_0hello'],'s_b.png')
sheet(['s_tablet_1p0','s_tablet_3p1','s_tablet_5p2','s_tablet_6etc'],'s_c.png')
