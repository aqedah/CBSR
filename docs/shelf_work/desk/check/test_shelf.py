from playwright.sync_api import sync_playwright
from PIL import Image
import sys
errs=[]; S='/tmp/shelftest/shots/'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=b.new_context(viewport={'width':390,'height':846},device_scale_factor=1,has_touch=True)
    pg=cx.new_page()
    pg.on('console',lambda m: errs.append(m.text) if m.type in('error',) or m.text.startswith('TOAST') else None)
    pg.on('pageerror',lambda e: errs.append('PAGEERROR '+str(e)))
    pg.goto('http://127.0.0.1:8765/index.html'); pg.click('#go'); pg.wait_for_timeout(900); pg.wait_for_function("!document.querySelector('#cbsrShelf.ent')")
    pg.screenshot(path=S+'1_hall.png'); print('hall zones',pg.locator('#cbsrShelf .zone').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="etc"]'); pg.wait_for_timeout(900); pg.screenshot(path=S+'2_etc.png'); print('warn:',pg.inner_text('.wn').replace('\n',' / ')[:120])
    pg.click('.wn button'); pg.wait_for_timeout(500); print('back to hall zones',pg.locator('.zone').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="ot"]'); pg.wait_for_timeout(1100); pg.screenshot(path=S+'3_ot.png'); print('ot groups',[x.inner_text().replace('\n',' ') for x in pg.locator('.gl button').all()])
    pg.click('.gl button[data-g="역사서"]'); pg.wait_for_timeout(900); pg.screenshot(path=S+'4_press_his.png'); print('spines',pg.locator('.sp').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.sp[data-b="1sa"]'); pg.wait_for_timeout(900); pg.screenshot(path=S+'5_open.png'); pg.wait_for_timeout(1700); pg.screenshot(path=S+'6_cover.png')
    n=int(pg.inner_text('.nv span').split('/')[1]); print('pages',n,'ovs',pg.evaluate('__ovs()'))
    names=[]
    for i in range(1,n):
        pg.click('.nv button[data-a="next"]'); pg.wait_for_timeout(120); k=pg.inner_text('main .k'); names.append(k)
        if i in (1,2,5,6,9): pg.screenshot(path=S+'7_p%d.png'%i)
    print('page labels',names)
    pg.screenshot(path=S+'8_end.png')
    pg.go_back(); pg.wait_for_timeout(400); print('after phone back → press?',pg.locator('.sp').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.bk'); pg.wait_for_timeout(500); print('‹ → sec?',pg.locator('.gl button').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.gl button[data-g="선지서"]'); pg.wait_for_timeout(800); pg.screenshot(path=S+'9_press_pro.png'); print('pro spines',pg.locator('.sp').count())
    pg.go_back(); pg.wait_for_timeout(300); pg.go_back(); pg.wait_for_timeout(600); print('hall again zones',pg.locator('.zone').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="nt"]'); pg.wait_for_timeout(1000); pg.screenshot(path=S+'10_nt.png')
    pg.click('.gl button[data-g="사도행전"]'); pg.wait_for_timeout(700); print('acts direct:',pg.inner_text('main h1'),'| back label:',pg.inner_text('.bb'))
    pg.click('.bb'); pg.wait_for_timeout(400); pg.click('.gl button[data-g="바울서신"]'); pg.wait_for_timeout(700); pg.click('.sp[data-b="gal"]'); pg.wait_for_timeout(2700)
    for i in range(4): pg.click('.nv button[data-a="next"]'); pg.wait_for_timeout(100)
    pg.screenshot(path=S+'11_gal_bg.png'); print('gal page:',pg.inner_text('main').replace('\n',' / ')[:200])
    for i in range(4): pg.go_back(); pg.wait_for_timeout(300)
    print('closed?',pg.evaluate('!CBSR_SHELF.isOpen()'),'ovs',pg.evaluate('__ovs()'))
    b.close()
print('errors:',errs)
order=sys.argv[1:] or ['1_hall','3_ot','4_press_his','5_open','6_cover']
ims=[Image.open(S+n+'.png') for n in order]
sh=Image.new('RGB',(400*len(ims)+10,866),(60,60,60))
for i,im in enumerate(ims): sh.paste(im,(10+i*400,10))
sh=sh.resize((sh.width*56//100,sh.height*56//100)); sh.save(S+'sheet.png'); print(sh.size)
