from playwright.sync_api import sync_playwright
from PIL import Image
errs=[]; S='/tmp/shelftest/shots/'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=b.new_context(viewport={'width':412,'height':699},device_scale_factor=2,has_touch=True)
    pg=cx.new_page(); pg.on('pageerror',lambda e: errs.append('PAGEERROR '+str(e)[:200]))
    pg.goto('http://127.0.0.1:8765/index.html'); pg.click('#go'); pg.wait_for_timeout(1000); pg.screenshot(path=S+'e1.png')
    pg.click('.zone[data-s="etc"]'); pg.wait_for_timeout(700); pg.screenshot(path=S+'e2.png'); print('경고장:',pg.inner_text('.wn').replace('\n',' / '),'| ovs',pg.evaluate('__ovs()'))
    pg.click('.wn button[data-a="enter"]'); pg.wait_for_timeout(2600); pg.screenshot(path=S+'e3.png'); print('열람 뒤 혼잣말:',pg.inner_text('.mono'),'| ovs',pg.evaluate('__ovs()'))
    pg.click('.mono'); pg.wait_for_timeout(500)
    box=pg.evaluate("(()=>{const z=document.querySelector('.zone.e span').getBoundingClientRect(),im=document.querySelector('.hl img').getBoundingClientRect();return [(z.left-im.left)/im.width,(z.top-im.top)/im.height,getComputedStyle(document.querySelector('.zn')).opacity]})()"); print('돌아오는 중 팻말의 그림 안 자리:',[round(float(x),3) for x in box])
    pg.wait_for_timeout(1500); box=pg.evaluate("(()=>{const z=document.querySelector('.zone.e span').getBoundingClientRect(),im=document.querySelector('.hl img').getBoundingClientRect();return [(z.left-im.left)/im.width,(z.top-im.top)/im.height,getComputedStyle(document.querySelector('.zn')).opacity]})()"); print('다 돌아온 뒤:',[round(float(x),3) for x in box]); print('서고로 →',pg.locator('.zone').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="etc"]'); pg.wait_for_timeout(500); pg.click('.wn button[data-a="back"]'); pg.wait_for_timeout(500); print('돌아가기 →',pg.locator('.zone').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="etc"]'); pg.wait_for_timeout(500); pg.mouse.click(20,650); pg.wait_for_timeout(500); print('빈 곳 →',pg.locator('.zone').count(),'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="nt"]'); pg.wait_for_timeout(2200); print('신약 서가:',pg.locator('.gl button').count()); pg.go_back(); pg.wait_for_timeout(1700); pg.go_back(); pg.wait_for_timeout(400); print('닫힘',pg.evaluate('!CBSR_SHELF.isOpen()'),pg.evaluate('__ovs()'))
    b.close()
print('errors',errs)
ims=[Image.open(S+n+'.png') for n in ('e1','e2','e3')]
sh=Image.new('RGB',(834*3+40,1418),(200,60,60))
for i,im in enumerate(ims): sh.paste(im,(10+i*844,10))
sh=sh.resize((sh.width*40//100,sh.height*40//100)); sh.save(S+'sheet_etc.png'); print(sh.size)
Image.open(S+'e1.png').crop((180,150,650,470)).save(S+'crop_tablet.png')
